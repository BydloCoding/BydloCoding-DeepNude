import json
from typing import Callable


class StructByAction(object):
    def __init__(self, initDict, parent=None, parent_key=None, action: Callable = lambda _: _):
        self.parent = parent
        self.dictionary = initDict
        self.parent_key = parent_key
        self.action = action

    def __setitem__(self, key, value):
        if self.parent is None:
            self.dictionary.__setitem__(key, value)
            self.action(self.dictionary)
        else:
            self.dictionary[key] = value
            self.parent.__setitem__(self.parent_key, self.dictionary)

    def __getitem__(self, key):
        tmp_return = self.dictionary[key]
        if isinstance(tmp_return, dict) or isinstance(tmp_return, list):
            return StructByAction(tmp_return, parent=self, parent_key=key, action=self.action)
        else:
            return tmp_return

    def get(self, key):
        return self.dictionary[key]

    def __str__(self):
        return self.dictionary.__str__()

    def __repr__(self):
        return f"StructByAction({self.dictionary})"

    def __delitem__(self, item):
        del self.dictionary[item]
        self.action(self.dictionary)

    def __contains__(self, item):
        return self.dictionary.__contains__(item)

    # list methods
    def __len__(self):
        return len(self.dictionary)

    def append(self, value):
        self.dictionary.append(value)
        self.action(self.dictionary)

    def __iadd__(self, keys):
        self.dictionary += keys
        self.action(self.dictionary)
        return self

    def insert(self, index, value):
        self.dictionary.insert(index, value)
        self.action(self.dictionary)
        return self


def save(file, obj):
    with open(file, "w") as f:
        json.dump(obj, f)


def load(file):
    with open(file) as f:
        return StructByAction(json.load(f), action=lambda d: save(file, d))


def isCastToFloatAvailable(data):
    try:
        float(data)
        return True
    except ValueError:
        return False


def isDeserializable(data):
    try:
        if isCastToFloatAvailable(data) or not (data.startswith("{") or data.startswith("[")): return {}, False
        return json.loads(data), True
    except (ValueError, TypeError):
        return {}, False
