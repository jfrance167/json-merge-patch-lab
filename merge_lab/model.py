"""Pure merge-value transformation; no paths, operation lists or resource writes."""
import json
from .contract import LIMITS, SCHEMA, LabError, Unsupported, validate, _walk


def _clone(value):
    # Called only after complete exact-builtin/tree admission; no deepcopy hooks.
    if type(value) is dict:
        return {key: _clone(child) for key, child in value.items()}
    if type(value) is list:
        return [_clone(child) for child in value]
    return value


def _merge(target, patch):
    if type(patch) is not dict:
        return _clone(patch)
    if type(target) is dict:
        result = _clone(target)
    else:
        result = {}
    for name, value in patch.items():
        if value is None:
            result.pop(name, None)
        else:
            # Missing and existing null are both nonobjects for recursive merge;
            # deletion membership and typed comparison retain their distinction.
            result[name] = _merge(result.get(name), value)
    return result


def _equal(left, right):
    if type(left) is not type(right):
        return False
    if type(left) is dict:
        return left.keys() == right.keys() and all(_equal(left[key], right[key]) for key in left)
    if type(left) is list:
        return len(left) == len(right) and all(_equal(a, b) for a, b in zip(left, right))
    return left == right


def analyze(envelope):
    """Return detached report/status after full admission; never mutate inputs."""
    validate(envelope)
    if envelope["schema"] != SCHEMA:
        raise Unsupported("unsupported schema")
    result = _merge(envelope["target"], envelope["patch"])
    _walk(result, "result")
    changed = not _equal(envelope["target"], result)
    kinds = {dict:"object",list:"array",str:"string",int:"integer",bool:"boolean",type(None):"null"}
    report = {"profile":SCHEMA,"representation":"merge-patch-value",
              "assumption":"synthetic supplied values; no resource modification or authorization verdict",
              "limits":dict(LIMITS),"target":_clone(envelope["target"]),
              "patch":_clone(envelope["patch"]),"result":result,
              "result_type":kinds[type(result)],"changed":changed}
    return report, 1 if changed else 0


def render(report):
    """Serialize admitted reports fully before physical delivery."""
    content = json.dumps(report, ensure_ascii=True, allow_nan=False, sort_keys=True, separators=(",", ":")) + "\n"
    if len(content.encode("ascii")) > LIMITS["output_bytes"]:
        raise LabError("resource limit")
    return content
