#!/usr/bin/env python
#

from animstack import Drawable

class ItemStateError(Exception):
    def __init__(self, msg = ''):
        self.__msg = msg

    def __str__(self):
        return self.__msg

class Item(Drawable):
    def __init__(self, anim_stack, state = 'initial'):
        Drawable.__init__(anim_stack)

        self.__state = state
        self.__state_stubs = {
            self.__state : { 'handler' : None,
                             'animation' : 'initial',
                             'next_state' : 'initial' }
            }

    def goto_state(self, state):
        self.__state = state
        self.change_animation(self.__state['animation'])

    def next_state(self):
        self.goto_state(self.__state_stubs['next_state'])

    def get_state(self):
        return self.__state

    def set_state(self, state, data):
        if (not data.has_key('handler') or
            not data.has_key('animation') or
            not data.has_key('next_state')):
            raise ItemStateError('Invalid state.')
        self.__state_stubs.update({state : data})

    def event_receiver(self, event):
        pass
