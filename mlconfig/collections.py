from collections import OrderedDict


class AttrDict(OrderedDict):
    IMMUTABLE = '__immutable__'

    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        for key, value in self.items():
            if isinstance(value, dict):
                self[key] = self.__class__(value)

        self.__dict__[AttrDict.IMMUTABLE] = False

    def __getattr__(self, key):
        if key in self.__dict__:
            return self.__dict__[key]
        elif key in self:
            return self[key]
        else:
            raise AttributeError(key)

    def __setattr__(self, key, value):
        if self.__dict__[AttrDict.IMMUTABLE]:
            raise AttributeError('Attempted to set "{}" to "{}", but AttrDict is immutable'.format(key, value))

        if isinstance(value, dict):
            value = self.__class__(value)

        if key in self.__dict__:
            self.__dict__[key] = value
        else:
            self[key] = value

    def set_immutable(self, immutable=True):
        self.__dict__[AttrDict.IMMUTABLE] = immutable

        for value in self.__dict__.values():
            if isinstance(value, AttrDict):
                value.set_immutable(immutable)

        for value in self.values():
            if isinstance(value, AttrDict):
                value.set_immutable(immutable)

    def is_immutable(self):
        return self.__dict__[AttrDict.IMMUTABLE]

    def to_dict(self):
        data = OrderedDict()

        for key, value in self.items():
            if isinstance(value, AttrDict):
                data[key] = value.to_dict()
            else:
                data[key] = value

        return data

    def flat(self, prefix=None, sep='.'):
        data = OrderedDict()

        for key, value in self.items():
            if prefix is not None:
                key = prefix + sep + key

            if isinstance(value, self.__class__):
                data.update(value.flat(prefix=key))
            else:
                data[key] = value

        return data
