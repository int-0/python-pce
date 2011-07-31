#!/usr/bin/env python

# TAKE INTO ACCOUNT: Child classes must be singletons!
class Registry(object):
    def __init__(self, channel):
        
        self.registry = {}
        self.__channel = channel

    def add(self, name, item):
        self.registry[name] = item
        self.__channel.add_subscriptor(name, item)

    def remove(self, name):
        del(self.registry[name])
        self.__channel.remove_subscriptor(name)

    def elements(self):
        return self.registry.keys()

    def get(self, name):
        return self.registry[name]

    def exists(self, name):
        return self.registry.has_key(name)

    def iterate(self):
        for item in self.registry.values():
            yield item

    def __call__(self, name):
        return self.get(name)

    # Event forwarding
    def event_receiver(self, event):
        # Forward only if event is not processed by registry
        if not self.process_event(event):
            self.__channel.send(event)

    # Overwrite method to process particular events (by default
    # registries forward all events)
    def process_event(self, event):
        return False
