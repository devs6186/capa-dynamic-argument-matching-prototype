from __future__ import annotations

from typing import Dict, Union

# API_ARG_MAP maps: api_name -> backend -> {positional_index_or_arg_name -> canonical_name}
# Integer keys: positional index (for backends using ArgN-style or numeric positions).
# String keys: named argument (for backends that report args by name, e.g. DRAKVUF).
API_ARG_MAP: Dict[str, Dict[str, Dict[Union[int, str], str]]] = {
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
    },
    "NtCreateFile": {
        # DRAKVUF records NtCreateFile (not CreateFileW) with a named ObjectAttributes
        # argument that carries the file path, equivalent to CreateFileW's lpFileName.
        "drakvuf": {
            "ObjectAttributes": "lpFileName",
        },
    },
}


def normalize_argument_name(backend: str, api: str, arg_name: str, arg_index: int) -> str:
    backend_map = API_ARG_MAP.get(api, {}).get(backend.lower(), {})

    if arg_name.startswith("Arg") and arg_name[3:].isdigit():
        index = int(arg_name[3:])
        return backend_map.get(index, arg_name)

    # Named-argument lookup first (for backends that report args by name).
    if arg_name in backend_map:
        return backend_map[arg_name]

    return backend_map.get(arg_index, arg_name)
