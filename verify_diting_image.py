"""Check actual rebuilt Image before any AK3 artifact is packaged. No rewriting."""
import hashlib
import pathlib
import re
import sys
import zlib


def verify(data):
    start = data.find(b"IKCFG_ST")
    if start < 0:
        raise ValueError("Compiled Image has no embedded IKCONFIG")
    decoder = zlib.decompressobj(31)
    config = decoder.decompress(data[start + 8:]).decode("utf-8")
    if not decoder.eof or not decoder.unused_data.startswith(b"IKCFG_ED"):
        raise ValueError("Invalid IKCONFIG gzip stream/end marker")
    for name in ("CONFIG_IP6_NF_NAT", "CONFIG_SYSVIPC"):
        if not re.search(r"^# " + name + r" is not set$", config, re.M):
            raise ValueError(name + " is not disabled in compiled Image")
    for name in ("CONFIG_KSU", "CONFIG_KSU_SUSFS"):
        if not re.search(r"^" + name + r"=y$", config, re.M):
            raise ValueError(name + " is not enabled")
    version = re.search(rb"Linux version 5\\.10\\.136-android12[^\\x00\\n]*", data)
    if not version:
        raise ValueError("Unexpected compiled kernel version / KMI family")
    return config, version.group().decode("ascii", errors="replace")


if __name__ == "__main__":
    path = pathlib.Path(sys.argv[1])
    data = path.read_bytes()
    config, version = verify(data)
    path.with_name("diting-verified.config").write_text(config, encoding="utf-8")
    print(version)
    masq = next(
        (line for line in config.splitlines() if "CONFIG_IP6_NF_TARGET_MASQUERADE" in line),
        "CONFIG_IP6_NF_TARGET_MASQUERADE absent",
    )
    print("MASQUERADE state:", masq)
    print("PASS: target VINTF requirements IP6_NF_NAT=n and SYSVIPC=n; KSU/SUSFS enabled")
    print("Image SHA256:", hashlib.sha256(data).hexdigest())
    print("Static verification only. No claim of device boot or complete VINTF compatibility.")
