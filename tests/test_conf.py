from typing import cast

import pytest
from omegaconf import DictConfig

from mlconfig import flatten
from mlconfig import getcls
from mlconfig import instantiate
from mlconfig import instantiate_as
from mlconfig import load
from mlconfig import register

ConfigData = dict[str, object]


@register
class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return self.__class__.__name__ + f"(x={self.x}, y={self.y})"

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)


@register
def add(x: Point, y: Point) -> Point:
    return x + y


@pytest.fixture
def obj() -> ConfigData:
    return {
        "x1": 1,
        "x2": 2,
        "a": {"name": "Point", "x": "${x1}", "y": 3},
        "b": {"name": "Point", "x": "${x1}", "y": 4},
        "op": {"name": "add"},
    }


@pytest.fixture
def conf(obj: ConfigData) -> DictConfig:
    loaded = load(obj=obj)
    assert isinstance(loaded, DictConfig)
    return loaded


def test_instantiate(conf: DictConfig, obj: ConfigData) -> None:
    assert conf["x1"] == conf["a"]["x"] == conf["b"]["x"] == obj["x1"]
    assert conf["x1"] == conf["b"]["x"] == conf["b"]["x"] == obj["x1"]

    instantiate(conf.a)

    a = instantiate(conf.a)
    b = instantiate(conf.b)
    assert isinstance(a, Point)
    assert isinstance(b, Point)

    result = instantiate(conf.op, a, b)
    assert isinstance(result, Point)
    x1 = obj["x1"]
    point_a = cast("ConfigData", obj["a"])
    point_b = cast("ConfigData", obj["b"])
    y_a = point_a["y"]
    y_b = point_b["y"]
    assert isinstance(x1, int)
    assert isinstance(y_a, int)
    assert isinstance(y_b, int)
    assert result.x == 2 * x1
    assert result.y == y_a + y_b


def test_instantiate_as(conf: DictConfig, obj: ConfigData) -> None:
    a = instantiate_as(conf.a, Point)
    assert a.x == obj["x1"]
    assert a.y == 3


def test_instantiate_as_invalid_type(conf: DictConfig) -> None:
    with pytest.raises(TypeError, match="instantiated object has type Point, expected str"):
        instantiate_as(conf.a, str)


def test_instantiate_as_with_kwargs(conf: DictConfig, obj: ConfigData) -> None:
    a = instantiate_as(conf.a, Point, y=10)
    assert a.x == obj["x1"]
    assert a.y == 10


def test_instantiate_as_with_args() -> None:
    conf_with_args: ConfigData = {"name": "Point"}
    a = instantiate_as(conf_with_args, Point, 5, 6)
    assert a.x == 5
    assert a.y == 6


def test_getcls(conf: DictConfig) -> None:
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
def test_flatten(test_input: ConfigData, expected: ConfigData) -> None:
    assert flatten(test_input) == expected


def test_getcls_valid(conf: DictConfig) -> None:
    assert getcls(conf["a"]) == Point
    assert getcls(conf["op"]) == add


def test_getcls_invalid_key_type(conf: DictConfig) -> None:
    _key = "name"
    conf_invalid = conf.copy()
    conf_invalid["a"][_key] = 123  # Invalid key type
    with pytest.raises(TypeError, match="key 123 must be a string"):
        getcls(conf_invalid["a"])


def test_getcls_key_not_found(conf: DictConfig) -> None:
    _key = "name"
    conf_invalid = conf.copy()
    conf_invalid["a"][_key] = "NonExistentKey"  # Key not in registry
    with pytest.raises(ValueError, match="key NonExistentKey not found in registry"):
        getcls(conf_invalid["a"])


def test_register_duplicate() -> None:
    with pytest.raises(ValueError, match="duplicate name Point found"):

        @register(name="Point")
        class PointDuplicate:
            def __init__(self, x: int, y: int) -> None:
                self.x = x
                self.y = y


def test_instantiate_with_kwargs(conf: DictConfig, obj: ConfigData) -> None:
    a = instantiate(conf.a, y=10)
    assert isinstance(a, Point)
    assert a.y == 10
    assert a.x == obj["x1"]


def test_instantiate_with_args() -> None:
    conf_with_args: ConfigData = {"name": "Point"}
    a = instantiate(conf_with_args, 5, 6)
    assert isinstance(a, Point)
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


def test_instantiate_non_callable(monkeypatch: pytest.MonkeyPatch) -> None:
    from mlconfig import conf as conf_module

    monkeypatch.setitem(conf_module._registry, "_non_callable_test", 42)  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="is not callable"):
        instantiate({"name": "_non_callable_test"})


def test_flatten_with_custom_separator() -> None:
    nested_dict = {"a": {"b": "c"}}
    expected = {"a/b": "c"}
    assert flatten(nested_dict, sep="/") == expected
