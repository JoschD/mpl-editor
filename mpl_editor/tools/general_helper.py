from contextlib import contextmanager


class DotDict(dict):
    """ Make dict fields accessible by . """
    def __init__(self, *args, **kwargs):
        super(DotDict, self).__init__(*args, **kwargs)
        for key in self:
            if isinstance(self[key], dict):
                self[key] = DotDict(self[key])

    # __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __getattr__(self, key):
        """ Needed to raise the correct exceptions """
        try:
            return super(DotDict, self).__getitem__(key)
        except KeyError as e:
            raise AttributeError from e
