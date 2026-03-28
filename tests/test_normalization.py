from capa_dynamic_argument_matching.normalization import normalize_argument_name


def test_cape_arg_index_normalization() -> None:
    assert normalize_argument_name("cape", "CreateFileW", "Arg0", 0) == "lpFileName"


def test_fallback_without_mapping() -> None:
    assert normalize_argument_name("cape", "UnknownApi", "Arg0", 0) == "Arg0"


def test_drakvuf_ntcreatefile_objectattributes() -> None:
    # DRAKVUF records NtCreateFile with a named ObjectAttributes argument;
    # normalization maps it to lpFileName (the canonical file-path argument name).
    assert normalize_argument_name("drakvuf", "NtCreateFile", "ObjectAttributes", 2) == "lpFileName"


def test_drakvuf_createfilew_positional() -> None:
    # DRAKVUF CreateFileW positional-index normalization is unaffected.
    assert normalize_argument_name("drakvuf", "CreateFileW", "Arg0", 0) == "lpFileName"


def test_named_arg_not_in_map_returns_original() -> None:
    # An unrecognized named argument with no map entry is returned as-is.
    assert normalize_argument_name("drakvuf", "NtCreateFile", "DesiredAccess", 1) == "DesiredAccess"
