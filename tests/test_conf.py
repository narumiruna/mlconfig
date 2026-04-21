import pytest

from mlconfig import flatten
from mlconfig import getcls
from mlconfig import instantiate
from mlconfig import load
from mlconfig import register


@register
class Point:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return self.__class__.__name__ + f"(x={self.x}, y={self.y})"

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)


@register
def add(x, y):
    return x + y


@pytest.fixture
def obj():
    return {
        "x1": 1,
        "x2": 2,
        "a": {"name": "Point", "x": "${x1}", "y": 3},
        "b": {"name": "Point", "x": "${x1}", "y": 4},
        "op": {"name": "add"},
    }


@pytest.fixture
def conf(obj):
    return load(obj=obj)


def test_instantiate(conf, obj) -> None:
    assert conf["x1"] == conf["a"]["x"] == conf["b"]["x"] == obj["x1"]
    assert conf["x1"] == conf["b"]["x"] == conf["b"]["x"] == obj["x1"]

    instantiate(conf.a)

    a = instantiate(conf.a)
    b = instantiate(conf.b)
    conf = instantiate(conf.op, a, b)
    assert conf.x == 2 * obj["x1"]
    assert conf.y == obj["a"]["y"] + obj["b"]["y"]


def test_getcls(conf) -> None:
    assert getcls(conf["a"]) == Point


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ({}, {}),
        ({"a": "b"}, {"a": "b"}),
        ({"a": {"b": {"c": "d"}}}, {"a.b.c": "d"}),
        ({"a": {"b": "c"}, "d": {"e": "f"}}, {"a.b": "c", "d.e": "f"}),
    ],
)
def test_flatten(test_input: dict, expected: dict) -> None:
    assert flatten(test_input) == expected


def test_getcls_valid(conf) -> None:
    assert getcls(conf["a"]) == Point
    assert getcls(conf["op"]) == add


def test_getcls_invalid_key_type(conf) -> None:
    _key = "name"
    conf_invalid = conf.copy()
    conf_invalid["a"][_key] = 123  # Invalid key type
    with pytest.raises(TypeError, match="key 123 must be a string"):
        getcls(conf_invalid["a"])


def test_getcls_key_not_found(conf) -> None:
    _key = "name"
    conf_invalid = conf.copy()
    conf_invalid["a"][_key] = "NonExistentKey"  # Key not in registry
    with pytest.raises(ValueError, match="key NonExistentKey not found in registry"):
        getcls(conf_invalid["a"])


def test_register_duplicate() -> None:
    with pytest.raises(ValueError, match="duplicate name Point found"):

        @register(name="Point")
        class PointDuplicate:
            def __init__(self, x, y) -> None:
                self.x = x
                self.y = y


def test_instantiate_with_kwargs(conf, obj) -> None:
    a = instantiate(conf.a, y=10)
    assert a.y == 10
    assert a.x == obj["x1"]


def test_instantiate_with_args(conf, obj) -> None:
    conf_with_args = {"name": "Point"}
    a = instantiate(conf_with_args, 5, 6)
    assert a.x == 5
    assert a.y == 6


def test_flatten_with_empty_dict() -> None:
    assert flatten({}) == {}


def test_flatten_with_nested_dict() -> None:
    nested_dict = {"a": {"b": {"c": "d"}}}
    expected = {"a.b.c": "d"}
    assert flatten(nested_dict) == expected


def test_flatten_with_prefix() -> None:
    nested_dict = {"a": {"b": "c"}}
    expected = {"prefix.a.b": "c"}
    assert flatten(nested_dict, prefix="prefix") == expected


def test_flatten_with_custom_separator() -> None:
    nested_dict = {"a": {"b": "c"}}
    expected = {"a/b": "c"}
    assert flatten(nested_dict, sep="/") == expected
