# Experimental IPv6 NAT configuration correction

Based on WildKernels/GKI_KernelSU_SUSFS R20, commit
`c5ed4038f6f759b70f051a4629de13a05650a501`.

Target: android12-5.10.136 / 2022-11, ReSukiSU. This is a TEST build,
not a certified device-compatible release.

Changes: disable CONFIG_IP6_NF_NAT, its dependent IPv6 MASQUERADE
target, and CONFIG_SYSVIPC in the real Kconfig input. SYSVIPC is also
forbidden by the Android 12 level-6 matrix on the target system;
disabling it affects containers depending on System V IPC.
Read the compiled Image's IKCONFIG
before packaging and fail if any remains enabled or KSU/SUSFS is missing.
The configuration verifier does not validate the built Image's release string;
the workflow separately checks the compiled banner when a release suffix is set.
No embedded configuration is rewritten.

ReSukiSU is kept at R20's 3c1882886dbbb54f4aae7ddf205f8ccde32c2a34
(UAPI 2, paired manager 35116). This does not make it compatible with the
newer UAPI 4 manager. R20's SUSFS, NoMount, kernel patch and DroidSpaces
revisions are retained. AnyKernel3 is pinned to the latest gki-2.0 commit
before R20's build. Android kernel sources are synced by the original dated
manifest; the actual source commit is recorded in the build metadata.

Only one target should be dispatched:

    kernel_build_version: 5.10.x-android12
    os_patch_level: 2022-11
    root_flavor: ReSukiSU
    commit_mode: verified
    use_cache: false
    bypass: false
    release_suffix: -android12-9-00021-g821df8f5bd36-ab9585204
    build_timestamp_utc: Thu Feb 9 13:08:46 UTC 2023
    release_type: Action

The change addresses a known kernel-config mismatch. Passing this static
check does not prove that all VINTF requirements pass or that hardware and
vendor modules work. Keep a matching stock boot image and verify on-device
before treating any resulting artifact as suitable for daily use.

The release suffix and build timestamp match the stock boot image from MIUI
V14.0.11.0.TLFCNXM. They are build metadata only: this experimental ReSukiSU
kernel is not the stock Xiaomi kernel, and matching strings do not establish
ABI or device compatibility.
