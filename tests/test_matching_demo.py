from capa_dynamic_argument_matching.extractors import DynamicCall, new_extract_features, old_extract_features
from capa_dynamic_argument_matching.matcher import match_yaml_rule


OLD_RULE = r"""
rule:
  features:
    - and:
      - api: CreateFileW
      - string: C:\Temp\evil.dll
"""

NEW_RULE = r"""
rule:
  features:
    - and:
      - api: CreateFileW
      - arg[lpFileName].string: C:\Temp\evil.dll
      - return-value: 0
"""


def test_old_rule_false_positive() -> None:
    call = DynamicCall(
        backend="cape",
        api="CreateFileW",
        args={
            "Arg0": r"C:\Windows\System32\kernel32.dll",
            "Arg7": r"C:\Temp\evil.dll",
        },
        return_value=0,
    )
    assert match_yaml_rule(old_extract_features(call), OLD_RULE)


def test_new_rule_avoids_false_positive() -> None:
    call = DynamicCall(
        backend="cape",
        api="CreateFileW",
        args={
            "Arg0": r"C:\Windows\System32\kernel32.dll",
            "Arg7": r"C:\Temp\evil.dll",
        },
        return_value=0,
    )
    assert not match_yaml_rule(new_extract_features(call), NEW_RULE)


def test_new_rule_true_positive() -> None:
    call = DynamicCall(
        backend="cape",
        api="CreateFileW",
        args={
            "Arg0": r"C:\Temp\evil.dll",
        },
        return_value=0,
    )
    assert match_yaml_rule(new_extract_features(call), NEW_RULE)


def test_count_api_calls() -> None:
    rule = r"""
rule:
  features:
    - count(api(CreateFileW)): 2
"""
    f1 = new_extract_features(DynamicCall(backend="vmray", api="CreateFileW", args={}, return_value=0))
    f2 = new_extract_features(DynamicCall(backend="vmray", api="CreateFileW", args={}, return_value=1))
    assert match_yaml_rule([*f1, *f2], rule)
