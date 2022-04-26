import pytest

from mlconfig.collections import AttrDict


def test_attrdict_init():
    d = AttrDict(a=1, b=2)
    assert d.a == 1
    assert d.b == 2


def test_attrdict_flat():
    data = {'a': 0, 'b': {'c': 1, 'd': {'e': 2, 'f': 3}}}

    d1 = AttrDict(data).flat()
    d2 = {'a': 0, 'b.c': 1, 'b.d.e': 2, 'b.d.f': 3}

    assert d1 == d2


def test_attrdict_to_dict():
    d = AttrDict()
    d.a = 0
    d.b = 1

    assert d.to_dict() == {'a': 0, 'b': 1}


def test_attrdict_immutable():
    d = AttrDict()
    d.set_immutable()

    with pytest.raises(AttributeError):
        d.a = 0


def test_attrdict_is_immutable():
    d = AttrDict(a=0, b=1)
    assert not d.is_immutable()

    d.set_immutable()
    assert d.is_immutable()
