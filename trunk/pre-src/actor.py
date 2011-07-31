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
        #self.displacement = (0, 0)

    # def set_pos(self, pos):
    #     Drawable.set_post(self, pos)
    #     self.state['actual_position'] = pos

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
        desired_pos = self.state['actual_action']['destination']

        # Check if action finished       
        if desired_pos == self.pos:
            self.next_action()
            return

        # Calculate new direction
        direction = 'WALK_'
        if desired_pos[0] > self.pos[0]:
            direction += 'E'
            new_pos_X = self.pos[0] + ACTOR_WALK_X
        elif desired_pos[0] < self.pos[0]:
            direction += 'O'
            new_pos_X = self.pos[0] - ACTOR_WALK_X
        else:
            new_pos_X = self.pos[0]
        if desired_pos[1] > self.pos[1]:
            direction += 'S'
            new_pos_Y = self.pos[1] + ACTOR_WALK_Y
        elif desired_pos[1] < self.pos[1]:
            direction += 'N'
            new_pos_Y = self.pos[1] - ACTOR_WALK_Y
        else:
            new_pos_Y = self.pos[1]

        # Select apropiate animation
        self.set_pos((new_pos_X, new_pos_Y))
        self.change_animation(direction)

    def talk(self):
        pass

    def event_receiver(self, event):
        op = event.get('op', None)
        # Ignore malformed events
        if op is None:
            return
        print 'Received event:', event
        if event['op'] == 'walk_to':
            self.cancel_all_actions()
            self.do_action({'op' : 'walk_to',
                            'destination' : event['position'],
                            'handler' : self.walk })

    def update(self):
        # Nothing to do? check for new actions!
        if self.state['actual_action'] == self.state['standby_action']:
            self.next_action()
        # Perform current action
        else:
            handler = self.state['actual_action'].get('handler', None)
            if not handler is None:
                handler()
        Drawable.update(self)
        self.cycles += 1
