#!/usr/bin/env python
#

from animstack import Drawable

ACTOR_WALK_X = 1
ACTOR_WALK_Y = 1

class Actor(Drawable):
    def __init__(self, initial_anim_stack):
        Drawable.__init__(self, initial_anim_stack)

        self.state = { 
            'actions' : [],
            'actual_action' : None,
            'standby_action' : None,
            'usr_vars' : {}
            }
        self.cycles = 0
        self.displacement = (0, 0)

    def set_var(self, var_name, value):
        self.state['usr_vars'][var_name] = value

    def get_var(self, var_name):
        return self.state['usr_vars'][var_name]

    def __can_walk(self):
        return (self.animations.animation_exists('WALK_E') and
                self.animations.animation_exists('WALK_O') and
                self.animations.animation_exists('WALK_S') and
                self.animations.animation_exists('WALK_N') and
                self.animations.animation_exists('WALK_EN') and
                self.animations.animation_exists('WALK_ES') and
                self.animations.animation_exists('WALK_OE') and
                self.animations.animation_exists('WALK_OS'))

    def do_action(self, action):
        # FIXME: check if action is valid
        self.state['actions'].append(action)

    def next_action(self):
        if len(self.state['actions']) > 0:
            self.state['actual_action'] = self.state['actions'].pop()
            self.cycles = 0
            #self.change_animation(self.state['actual_action'])
        else:
            self.cancel_all_actions()

    def cancel_all_actions(self):
        self.state['actions'] = []
        # Cancel current action
        if self.state['actual_action'] != self.state['standby_action']:
            self.state['actual_action'] = self.state['standby_action']
            self.cycles = 0

    def walk(self):
        desired_pos = self.state['actual_action']['position']

        # Check if action finished       
        if desired_pos == self.pos:
            self.next_action()
            return

        # Calculate new direction
        direction = 'WALK_'
        if desired_pos[0] > self.pos[0]:
            direction += 'E'
            self.displacement[0] = ACTOR_WALK_X
        elif desired_pos[0] < self.pos[0]:
            direction += 'O'
            self.displacement[0] = -ACTOR_WALK_X
        else:
            self.displacement[0] = 0
        if desired_pos[1] > self.pos[1]:
            direction += 'S'
            self.displacement[1] = ACTOR_WALK_Y
        elif desired_pos[1] < self.pos[1]:
            direction += 'N'
            self.displacement[1] = -ACTOR_WALK_Y
        else:
            self.displacement[1] = 0

        # Select apropiate animation
        self.change_animation(direction)

    def talk(self):
        pass

    def event_receiver(self, event):        
        pass

    def update(self):
        Drawable.update(self)
        self.cycles += 1
