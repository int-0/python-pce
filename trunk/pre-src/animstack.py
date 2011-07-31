#!/usr/bin/env python

#Import Modules
import os
import copy
import pygame
from pygame.locals import *
from framestack import FrameStack

if not pygame.font: print 'Warning, fonts disabled'

class BadAnimationStack(Exception):
    def __init__(self, info):
        Exception.__init__(self, info)
        self.__info = info

    def __str__(self):
        return repr(self.__info)

class AnimationStack:
    def __init__(self, stack_frame):
        self.stack = stack_frame
        self.__anims = {}
        for group in self.stack.groups.keys():
            self.make_loop(group, group)

    def change_frames(self, new_sf):
        self.stack = new_sf

    def animation_exists(self, animation):
        return self.__anims.has_key(animation)

    def make_loop(self, frame_group, animation):
        if not self.stack.group_exists(frame_group):
            raise BadAnimationStack('Animation stack not found: ' + frame_group)
        print animation, 'is', self.stack.get_group(frame_group)
        self.__anims[animation] = self.stack.get_group(frame_group)

    def convert_pingpong(self, animation):
        if not self.animation_exists(animation):
            raise BadAnimationStack('Animation stack not found: ' + animation)
        first = copy.copy(self.__anims[animation])
        last = copy.copy(self.__anims[animation])
        last.reverse()
        first.pop()
        self.__anims[animation] = first + last

    def copy_animation(self, original, new):
        if not self.animation_exists(original):
            raise BadAnimationStack('Animation stack not found: ' + original)
        self.__anims[new] = copy.copy(self.__anims[original])

    def delete_animation(self, animation):
        if not self.animation_exists(animation):
            raise BadAnimationStack('Animation stack not found: ' + animation)
        del(self.__anims[animation])

    def reverse_animation(self, animation):
        if not self.animation_exists(animation):
            raise BadAnimationStack('Animation stack not found: ' + animation)
        self.__anims[animation].reverse()

    def get_animation(self, animation):
        if not self.animation_exists(animation):
            raise BadAnimationStack('Animation stack not found: ' + animation)
        return self.__anims[animation]

class Drawable(pygame.sprite.Sprite):
    def __init__(self, anim_stack, destination_surface = None,
                 initial = 'initial', event = None):
        pygame.sprite.Sprite.__init__(self)

        self.frame = 0
        self.animations = anim_stack
        self.animation = self.animations.get_animation(initial)
        self.current_animation = initial
        
        self.image = self.animations.stack.frames[self.animation[self.frame]]

        self.rect = self.image.get_rect()
        self.pos = self.rect.topleft

        self.dest = destination_surface
        if not self.dest is None:
            self.area = self.dest.get_rect()
        else:
            self.area = None

        self.event = None

    def set_pos(self, pos):
        self.pos = pos

    def set_event(self, event):
        self.event = event

    def set_destination(self, destination_surface):
        self.dest = destination_surface
        self.area = self.dest.get_rect()

    def restart_animation(self):
        self.frame = 0
        print 'StackFrame:', self.animation[self.frame], '(', len(self.animations.stack.frames), ')'
        self.image = self.animations.stack.frames[self.animation[self.frame]]
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos
        
    def change_animation(self, animation):
        if animation == self.current_animation:
          return
        self.animation = self.animations.get_animation(animation)
        self.restart_animation()

    def update(self):
        self.frame = self.frame + 1
        if (self.frame >= len(self.animation)):
            if not (self.event is None):
                self.event.fire()
            self.frame = 0
        self.image = self.animations.stack.frames[self.animation[self.frame]]
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos

# From prefix name, generates frame stack and animation stack with loop frames
#
def Animation_factory(prefix_name, destination = None):
    return Drawable(AnimationStack(FrameStack(prefix_name)), destination)

# Simple test
#
def main():

    # Initialize Everything
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('Animation Test')
    pygame.mouse.set_visible(0)

    # Create The Backgound
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

    # Display The Background
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Prepare Game Objects
    clock = pygame.time.Clock()

    # Load frames
    animation = Animation_factory('frame', screen)
    allsprites = pygame.sprite.RenderPlain((animation))

    # Main Loop
    while 1:
        clock.tick(10)

        # Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return

        allsprites.update()

        # Draw Everything
        screen.blit(background, (0, 0))
        allsprites.draw(screen)
        pygame.display.flip()

#this calls the 'main' function when this script is executed
if __name__ == '__main__':
    main()
