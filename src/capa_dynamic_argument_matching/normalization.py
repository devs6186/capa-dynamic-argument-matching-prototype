from __future__ import annotations

from typing import Dict

API_ARG_MAP: Dict[str, Dict[str, Dict[int, str]]] = {
    "CreateFileW": {
        "cape": {
            0: "lpFileName",
            1: "dwDesiredAccess",
            2: "dwShareMode",
            3: "lpSecurityAttributes",
            4: "dwCreationDisposition",
            5: "dwFlagsAndAttributes",
            6: "hTemplateFile",
        },
        "drakvuf": {
            0: "lpFileName",
            1: "dwDesiredAccess",
            2: "dwShareMode",
            3: "lpSecurityAttributes",
            4: "dwCreationDisposition",
            5: "dwFlagsAndAttributes",
            6: "hTemplateFile",
        },
    }
}


def normalize_argument_name(backend: str, api: str, arg_name: str, arg_index: int) -> str:
    backend_map = API_ARG_MAP.get(api, {}).get(backend.lower(), {})

    if arg_name.startswith("Arg") and arg_name[3:].isdigit():
        index = int(arg_name[3:])
        return backend_map.get(index, arg_name)

    return backend_map.get(arg_index, arg_name)
