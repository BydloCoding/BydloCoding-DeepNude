class DataClass(object):
    def __init__(self, *args, customClass = None):
        self.klass = DataClass if customClass is None else customClass
        self.args = args
        for i in args:
            self.__setattr__(i, None)

    def __call__(self, *args):
        newInstance = self.klass(*self.args)
        for j, i in enumerate(self.args):
            newInstance.__setattr__(i, args[j])
        return newInstance
