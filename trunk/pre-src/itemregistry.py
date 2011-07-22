#!/usr/bin/env python

from registry import Registry

class ItemRegistry(object):
    # storage for the instance reference
    __instance = None

    class Implementation(Registry):
        def __init__(self, channel):
            Registry.__init__(self, channel)

    def __init__(self, channel):
        # Check whether we already have an instance
        if ItemRegistry.__instance is None:
            ItemRegistry.__instance = ItemRegistry.Implementation(channel)
        self._EventHandler_instance = ItemRegistry.__instance

    def __getattr__(self, aAttr):
        return getattr(self.__instance, aAttr)

    def __setattr__(self, aAttr, avalue):
        return setattr(self.__instance, aAttr, avalue)

    def process_event(self, event):
        operation = event.get('op', None)
       # Ignore malformed events
        if operation is None:
            return True
        # Forward valid events
        return False

if __name__ == '__main__':
    class DummyEventChannel:
        def add_subscriptor(self, name, callback):
            pass
    class DummyItem:
        def event_receiver(self):
            pass
    a = ItemRegistry(DummyEventChannel())
    a.add('pepe', DummyItem())
    b = ItemRegistry(DummyEventChannel())
    print a.elements()
    print b.elements()
