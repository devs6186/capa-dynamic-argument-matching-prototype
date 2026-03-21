from __future__ import annotations

import re
from collections import Counter
from typing import Any, Dict, Iterable, List, Sequence, Tuple

import yaml

from .features import API, Argument, Number, ReturnValue, String

ARG_RE = re.compile(r"^arg\[(?P<name>[^\]]+)\]\.(?P<kind>string|number)$")
COUNT_RE = re.compile(r"^count\((?P<inner>.+)\)$")
INNER_RE = re.compile(r"^(api|return-value|arg\[[^\]]+\]\.(?:string|number))\((.+)\)$")


def _flatten_features(node: Any) -> List[Dict[str, Any]]:
    if isinstance(node, list):
        if len(node) == 1 and isinstance(node[0], dict) and "and" in node[0]:
            return _flatten_features(node[0]["and"])
        out: List[Dict[str, Any]] = []
        for item in node:
            out.extend(_flatten_features(item))
        return out

    if isinstance(node, dict):
        if "and" in node:
            return _flatten_features(node["and"])
        return [node]

    raise ValueError("invalid rule features section")


def _parse_value(term: str, value: Any) -> Tuple[str, Any]:
    if term == "api":
        return ("api", str(value))
    if term == "string":
        return ("string", str(value))
    if term == "number":
        return ("number", int(value))
    if term == "return-value":
        return ("return", int(value))

    m = ARG_RE.match(term)
    if m:
        name = m.group("name")
        kind = m.group("kind")
        return (f"arg_{kind}", (name, str(value) if kind == "string" else int(value)))

    cm = COUNT_RE.match(term)
    if cm:
        inner_expr = cm.group("inner")
        im = INNER_RE.match(inner_expr)
        if not im:
            raise ValueError(f"unsupported count expression: {inner_expr}")
        inner_term = im.group(1)
        inner_value = im.group(2)
        parsed_inner = _parse_value(inner_term, inner_value)
        return ("count", (parsed_inner, int(value)))

    raise ValueError(f"unsupported term: {term}")


def parse_yaml_rule(text: str) -> List[Tuple[str, Any]]:
    data = yaml.safe_load(text)
    body = data["rule"]["features"]

    conditions: List[Tuple[str, Any]] = []
    for feature_map in _flatten_features(body):
        if len(feature_map) != 1:
            raise ValueError("feature maps must have one term")
        (term, value), = feature_map.items()
        conditions.append(_parse_value(term, value))
    return conditions


def _to_atoms(features: Sequence[object]) -> List[Tuple[str, Any]]:
    atoms: List[Tuple[str, Any]] = []
    for feature in features:
        if isinstance(feature, API):
            atoms.append(("api", feature.name))
        elif isinstance(feature, String):
            atoms.append(("string", feature.value))
        elif isinstance(feature, Number):
            atoms.append(("number", feature.value))
        elif isinstance(feature, Argument):
            kind = "arg_string" if isinstance(feature.value, str) else "arg_number"
            atoms.append((kind, (feature.arg_name, feature.value)))
        elif isinstance(feature, ReturnValue):
            atoms.append(("return", feature.value))
    return atoms


def match_conditions(features: Sequence[object], conditions: Sequence[Tuple[str, Any]]) -> bool:
    atoms = _to_atoms(features)
    counts = Counter(atoms)

    for kind, expected in conditions:
        if kind == "count":
            (inner_kind, inner_value), minimum = expected
            if counts[(inner_kind, inner_value)] < minimum:
                return False
            continue

        if (kind, expected) not in atoms:
            return False
    return True


def match_yaml_rule(features: Sequence[object], text: str) -> bool:
    return match_conditions(features, parse_yaml_rule(text))
