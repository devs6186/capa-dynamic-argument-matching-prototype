from capa_dynamic_argument_matching.normalization import normalize_argument_name


def test_cape_arg_index_normalization() -> None:
    assert normalize_argument_name("cape", "CreateFileW", "Arg0", 0) == "lpFileName"


def test_fallback_without_mapping() -> None:
    assert normalize_argument_name("cape", "UnknownApi", "Arg0", 0) == "Arg0"
