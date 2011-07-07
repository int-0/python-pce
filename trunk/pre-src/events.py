#!/usr/bin/env python
#

class EventChannel(object):
    def __init__(self):
        self.__subscriptors = {}

    def add_subscriptor(self, name, callback):
        self.__subscriptors[name] = callback

    def has_subscriptor(self, name):
        return self.__subscriptors.has_key(name)

    def send(self, event):
        destinations = event['destination']
        if destinations == 'all':
            for cb in self.__subscriptors.values():
                cb(event)
        else:
            for destination in destinations:
                if self.has_subscriptor(destination):
                    self.__subscriptors[destination](event)

class Event(object):
    def __init__(self, channel):
        self.__channel = channel
        
        self.data = { 'destination' : [] }

    def add_destination(self, destination):
        self.data['destination'].append(destination)

    def get_destination(self):
        return self.data['destination']

    def clear_destinations(self):
        self.data['destination'] = []

    def set_broadcast(self):
        self.data['destination'] = 'all'

    def set_data(self, key, value):
        self.data[key] = value

    def fire(self):
        self.__channel.send(self.data)

