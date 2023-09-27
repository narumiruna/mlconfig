import pytest

from mlconfig import getcls
from mlconfig import instantiate
from mlconfig import load
from mlconfig import register


@register
class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return self.__class__.__name__ + "(x={}, y={})".format(self.x, self.y)

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


def test_instantiate(conf, obj):
    assert conf["x1"] == conf["a"]["x"] == conf["b"]["x"] == obj["x1"]
    assert conf["x1"] == conf["b"]["x"] == conf["b"]["x"] == obj["x1"]

    instantiate(conf.a)

    a = instantiate(conf.a)
    b = instantiate(conf.b)
    conf = instantiate(conf.op, a, b)
    assert conf.x == 2 * obj["x1"]
    assert conf.y == obj["a"]["y"] + obj["b"]["y"]


def test_getcls(conf):
    assert getcls(conf["a"]) == Point
