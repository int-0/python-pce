#!/usr/bin/env python
#

from animstack import Drawable

class Actor(Drawable):
    def __init__(self, initial_anim_stack):
        self.Drawable(self, initial_anim_stack)

        self.state = { 'actions' : [],
                       'actual_action' : None }

    def do_action(self, action):
        # FIXME: check if action is valid
        self.state['actions'].append(action)

    def next_action(self):
        if len(self.state['actions']) > 0:
            self.state['actual_action'] = self.state['actions'].pop()
        else:
            self.cancel_all_actions()

    def cancel_all_actions(self):
        self.state['actual_action'] = None
        # Activate Stand-by animation

    def walk(self):
        desired_pos = self.state['actual_action']['position']

        # Check if action finished
        if desired_pos == self.get_pos():
            self.next_action()
            return

        # Calculate new direction

        # Select apropiate animation

        # Continue animation

    def say(self):
        pass

