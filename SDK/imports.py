import os

from importlib import util


class ImportTools(object):
    ignore = ["__pycache__"]
    modules = {}

    def __init__(self, paths=None):
        if paths is None:
            paths = ["packages"]
        for path in paths:
            if not os.path.exists(path): os.makedirs(path)
            for file in os.listdir(path):
                if path in self.ignore: continue
                thisPath = os.path.join(path, file)
                if os.path.isdir(thisPath): continue
                fileName = os.path.splitext(file)[0]
                spec = util.spec_from_file_location(fileName, thisPath)
                foo = util.module_from_spec(spec)
                spec.loader.exec_module(foo)
                self.modules.update({path: foo})
