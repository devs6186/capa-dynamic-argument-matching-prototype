from __future__ import annotations

from capa_dynamic_argument_matching.extractors import DynamicCall, new_extract_features, old_extract_features
from capa_dynamic_argument_matching.matcher import match_yaml_rule


OLD_RULE = r"""
rule:
  meta:
    name: legacy generic path match
    scopes:
      dynamic:
        - call
  features:
    - and:
      - api: CreateFileW
      - string: C:\Temp\evil.dll
""".strip()

NEW_RULE = r"""
rule:
  meta:
    name: structured path match
    scopes:
      dynamic:
        - call
  features:
    - and:
      - api: CreateFileW
      - arg[lpFileName].string: C:\Temp\evil.dll
      - return-value: 0
""".strip()


def main() -> None:
    false_positive = DynamicCall(
        backend="cape",
        api="CreateFileW",
        args={
            "Arg0": r"C:\Windows\System32\kernel32.dll",
            "Arg1": "0x80000000",
            "Arg2": "1",
            "Arg3": "0",
            "Arg4": "3",
            "Arg5": "128",
            "Arg6": "0",
            "Arg7": r"C:\Temp\evil.dll",
        },
        return_value=0,
    )

    true_positive = DynamicCall(
        backend="cape",
        api="CreateFileW",
        args={
            "Arg0": r"C:\Temp\evil.dll",
            "Arg1": "0x80000000",
            "Arg2": "1",
            "Arg3": "0",
            "Arg4": "3",
            "Arg5": "128",
            "Arg6": "0",
        },
        return_value=0,
    )

    old_false = match_yaml_rule(old_extract_features(false_positive), OLD_RULE)
    old_true = match_yaml_rule(old_extract_features(true_positive), OLD_RULE)
    new_false = match_yaml_rule(new_extract_features(false_positive), NEW_RULE)
    new_true = match_yaml_rule(new_extract_features(true_positive), NEW_RULE)

    print("Before (generic string rule):")
    print(f"  false-positive call matched: {old_false}")
    print(f"  true-positive call matched : {old_true}")
    print()
    print("After (structured argument + return rule):")
    print(f"  false-positive call matched: {new_false}")
    print(f"  true-positive call matched : {new_true}")


if __name__ == "__main__":
    main()
