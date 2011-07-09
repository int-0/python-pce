#!/usr/bin/env python

# TAKE INTO ACCOUNT: Child classes must be singletons!
class Registry(object):
    def __init__(self, channel):
        
        self.registry = {}
        self.__channel = channel

    def add(self, name, item):
        self.registry[name] = item
        self.__channel.add_subscriptor(name, item.event_receiver)

    def remove(self, name):
        del(self.registry[name])

    def elements(self):
        return self.registry.keys()

    def get(self, name):
        return self.registry[name]

    def iterate(self):
        for item in self.registry.values():
            yield item

    def __call__(self, name):
        return self.get(name)

    def set_event_channel(self, channel):
        self.__channel = channel

    # Event forwarding
    def event_receiver(self, event):
        self.__channel.send(event)

