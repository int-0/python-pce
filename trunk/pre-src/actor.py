#!/usr/bin/env python
#

from animstack import Drawable

class Actor(Drawable):
    def __init__(self, initial_anim_stack):
        self.Drawable(self, initial_anim_stack)

    
