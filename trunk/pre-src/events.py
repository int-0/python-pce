#!/usr/bin/env python
#

class EventChannel(object):
    def __init__(self):
        self.__subscriptors = {}

    def add_subscriptor(self, name, subscriptor):
        # Subscriptables objects have event_receiver() method
        self.__subscriptors[name] = subscriptor.event_receiver

    def has_subscriptor(self, name):
        return self.__subscriptors.has_key(name)

    def remove_subscriptor(self, name):
        if self.has_subscriptor(name):
            del(self.__subscriptors[name])

    def send(self, event):
        destinations = event.get('dest', 'all')
        if destinations == 'all':
            for cb in self.__subscriptors.values():
                cb(event)
        else:
            for subscriptor in destinations:
                if self.has_subscriptor(subscriptor):
                    self.__subscriptors[subscriptor](event)

# class Event(object):
#     def __init__(self, channel):
#         self.__channel = channel
        
#         self.data = { 'destination' : [] }

#     def add_destination(self, destination):
#         self.data['destination'].append(destination)

#     def get_destination(self):
#         return self.data['destination']

#     def clear_destinations(self):
#         self.data['destination'] = []

#     def set_broadcast(self):
#         self.data['destination'] = 'all'

#     def set_data(self, key, value):
#         self.data[key] = value

#     def fire(self):
#         self.__channel.send(self.data)

