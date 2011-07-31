#!/usr/bin/env python

from registry import Registry

class ActorRegistry(object):
    # storage for the instance reference
    __instance = None

    class Implementation(Registry):
        def __init__(self, channel):
            Registry.__init__(self, channel)

    def __init__(self, channel):
        # Check whether we already have an instance
        if ActorRegistry.__instance is None:
            ActorRegistry.__instance = ActorRegistry.Implementation(channel)
        self._EventHandler_instance = ActorRegistry.__instance

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
