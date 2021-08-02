import inspect
from SDK.dataClass import DataClass


# kotlin-like enums
class Enum(object):
    def __init__(self, customDataClass = None):
        inspectedArgs = inspect.getfullargspec(self.__init__)
        self.EnumValue = DataClass(*inspectedArgs.args[1:]) if customDataClass is None else customDataClass(*inspectedArgs.args[1:])