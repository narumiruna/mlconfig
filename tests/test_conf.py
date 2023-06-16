from mlconfig import instantiate
from mlconfig import load
from mlconfig import register


@register
class Point(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return self.__class__.__name__ + '(x={}, y={})'.format(self.x, self.y)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)


@register
def add(x, y):
    return x + y


def test_instantiate():
    d = {
        'x1': 1,
        'x2': 2,
        'a': {
            'name': 'Point',
            'x': '${x1}',
            'y': 3
        },
        'b': {
            'name': 'Point',
            'x': '${x1}',
            'y': 4
        },
        'op': {
            'name': 'add'
        }
    }
    c = load(obj=d)
    assert c['x1'] == c['a']['x'] == c['b']['x'] == d['x1']
    assert c['x1'] == c['b']['x'] == c['b']['x'] == d['x1']

    instantiate(c.a)

    a = instantiate(c.a)
    b = instantiate(c.b)
    c = instantiate(c.op, a, b)
    assert c.x == 2 * d['x1']
    assert c.y == d['a']['y'] + d['b']['y']
