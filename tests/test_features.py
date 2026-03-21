from capa_dynamic_argument_matching.features import Argument, ReturnValue


def test_argument_name_generation() -> None:
    assert Argument("lpFileName", "x").name == "arg[lpFileName].string"
    assert Argument("dwFlags", 1).name == "arg[dwFlags].number"


def test_hash_and_equality() -> None:
    assert Argument("lpFileName", "x") == Argument("lpFileName", "x")
    assert hash(Argument("lpFileName", "x")) == hash(Argument("lpFileName", "x"))


def test_return_value_name() -> None:
    assert ReturnValue(0).name == "return-value"
