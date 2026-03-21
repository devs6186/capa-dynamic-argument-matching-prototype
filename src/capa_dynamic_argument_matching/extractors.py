from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List

from .features import API, Argument, Number, ReturnValue, String
from .normalization import normalize_argument_name


@dataclass(frozen=True)
class DynamicCall:
    backend: str
    api: str
    args: Dict[str, Any]
    return_value: int | None = None


def _coerce_number(value: Any) -> int | None:
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        text = value.strip()
        if text.startswith("0x"):
            try:
                return int(text, 16)
            except ValueError:
                return None
        if text.isdigit():
            return int(text)
    return None


def old_extract_features(call: DynamicCall) -> List[object]:
    features: List[object] = [API(call.api)]

    for value in call.args.values():
        if isinstance(value, str):
            features.append(String(value))
            number = _coerce_number(value)
            if number is not None:
                features.append(Number(number))
        else:
            number = _coerce_number(value)
            if number is not None:
                features.append(Number(number))

    return features


def new_extract_features(call: DynamicCall) -> List[object]:
    features: List[object] = [API(call.api)]

    for index, (raw_name, raw_value) in enumerate(call.args.items()):
        normalized = normalize_argument_name(call.backend, call.api, raw_name, index)

        if isinstance(raw_value, str):
            features.append(Argument(normalized, raw_value))
            features.append(String(raw_value))
            number = _coerce_number(raw_value)
            if number is not None:
                features.append(Argument(normalized, number))
                features.append(Number(number))
            continue

        number = _coerce_number(raw_value)
        if number is not None:
            features.append(Argument(normalized, number))
            features.append(Number(number))

    if call.return_value is not None:
        features.append(ReturnValue(int(call.return_value)))

    return features
