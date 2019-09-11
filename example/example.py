import mlconfig


@mlconfig.register
class Point(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return self.__class__.__name__ + '(x={}, y={})'.format(self.x, self.y)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)


@mlconfig.register
def add(x, y):
    return x + y


def main():
    f = 'config.yaml'
    config = mlconfig.load(f)
    print(config)

    a = config.a()
    print('a = {}'.format(a))
    b = config.b()
    print('b = {}'.format(b))

    c = config.op(a, b)
    print('c = {}'.format(c))


if __name__ == '__main__':
    main()
