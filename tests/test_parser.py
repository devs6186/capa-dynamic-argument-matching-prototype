from capa_dynamic_argument_matching.matcher import parse_yaml_rule


def test_parse_argument_and_return_value() -> None:
    text = r"""
rule:
  features:
    - and:
      - api: CreateFileW
      - arg[lpFileName].string: C:\Temp\evil.dll
      - arg[dwDesiredAccess].number: 2147483648
      - return-value: 0
"""
    conditions = parse_yaml_rule(text)
    assert ("api", "CreateFileW") in conditions
    assert ("arg_string", ("lpFileName", r"C:\Temp\evil.dll")) in conditions
    assert ("arg_number", ("dwDesiredAccess", 2147483648)) in conditions
    assert ("return", 0) in conditions


def test_parse_count_expression() -> None:
    text = """
rule:
  features:
    - count(api(CreateFileW)): 2
"""
    conditions = parse_yaml_rule(text)
    assert conditions == [("count", (("api", "CreateFileW"), 2))]
