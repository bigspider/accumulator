class Event:
    def __init__(self):
        self.listeners = []

    def __iadd__(self, listener):
        self.listeners.append(listener)
        return self

    def notify(self, *args, **kwargs):
        for listener in self.listeners:
            listener(*args, **kwargs)
