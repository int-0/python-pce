#!/usr/bin/env python

# FIXME: MUST BE A SINGLETON!
class ItemRegistry(object):
    def __init__(self, channel):
        
        self.__registry = {}
        self.__channel = channel

    # Registry operations
    #
    def add_item(self, name, item):
        self.__registry[name] = item
        self.__channel.add_subscriptor(name, item.event_receiver)

    def get_item(self, name):
        return self.__registry[name]

    # def remove_item(self, name):
    #     del(self.__registry[name])

    def get_items(self):
        return self.__registry.keys()

    def set_event_channel(self, channel):
        self.__channel = channel

    # Event forwarding
    def event_receiver(self, event):
        self.__channel.send(event)
