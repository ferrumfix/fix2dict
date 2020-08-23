def meta_v1(fix_version):
    return {
        "schema": "1",
        "version": fix_version,
        "copyright": "Copyright (c) FIX Protocol Limited, all rights reserved",
        "fix2dict": {
            "version": __version__,
            "legal": LEGAL_INFO,
            "md5": "",
            "command": " ".join(sys.argv),
            "timestamp": iso8601_utc(),
        },
    }

