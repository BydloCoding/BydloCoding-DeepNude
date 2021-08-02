import threading

from SDK import listExtension


class ThreadManager(object):
    thread_poll = listExtension.ListExtension([])

    def threadByName(self, name):
        return self.thread_poll.find(lambda item: item.name == name)

    def changeInterval(self, name, newInterval):
        thread = self.threadByName(name)
        thread.interval = newInterval

    def __getitem__(self, key):
        return self.threadByName(key)


class Every(threading.Thread):
    def __init__(self, callback, interval, *args, onExecCallback=None, **kwargs):
        self.callback = callback
        self.interval = interval
        self.event = threading.Event()
        self.onExecCallback = onExecCallback
        self.args = args
        ThreadManager.thread_poll.append(self)
        super().__init__(**kwargs)
        self.start()

    # override
    def run(self):
        self.callback(*self.args)
        while not self.event.wait(self.interval):
            if self.onExecCallback is not None: self.onExecCallback()
            self.callback(*self.args)


def every(interval, *myArgs, callback=None, **myKwargs):
    def func_wrap(func):
        return Every(func, interval, *myArgs, onExecCallback=callback, **myKwargs)

    return func_wrap
