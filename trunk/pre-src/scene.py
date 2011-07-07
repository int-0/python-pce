#!/usr/bin/env python
#

import os
import os.path
import pygame
from pygame.locals import *
from orderedrender import OrderedRenderUpdates
from itemregistry import ItemRegistry

class Scene(object):
    def __init__(self, bg, mask = None):
        self.bg = bg
        self.fg = mask

        self.__item_resitry = ItemRegistry()

        self.__dirty = []
        self.__attrezo = {}
        self.__objects = []
        self.__sprites = OrderedRenderUpdates()

    def update(self):
        self.__sprites.update()

    def draw(self, surface, pos = (0, 0)):
        frame = self.bg.copy()
        self.__sprites.draw(frame)
        if not self.fg is None:
            frame.blit(self.fg, (0,0))
        surface.blit(frame, pos)

    def __update_group(self):
        self.__sprites.empty()
        for sprite in self.__attrezo.values():
            self.__sprites.add(sprite)
        for sprite in self.__objects:
            self.__sprites.add(self.__item_registry.get_item(sprite))

    # FIXME: check allready added
    def show_item(self, name):
        self.__objects.append(name)
        self.__update_group()

    # FIXME: check availability
    def hide_item(self, name):
        del(self.__objects[name])
        self.__update_group()

    def set_attrezo(self, drawable, name):
        self.__attrezo[name] = drawable
        self.__update_group()

    def remove_attrezo(self, name):
        if self.__attrezo.has_key(name):
            del(self.__attrezo[name])
            self.__update_group()

    def get_objects(self):
        return self.__attrezo.keys()

def load_image(fullname):
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', fullname
        raise SystemExit, message
    return image.convert_alpha()

def main():

    # Initialize Everything
    pygame.init()
    screen = pygame.display.set_mode((1024, 768))
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
    scene = Scene(
        load_image('room.png'),
        load_image('room_mask.png')
        )

    # Main Loop
    while 1:
        clock.tick(10)

        # Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return

        # Draw scene
        scene.update()
        scene.draw(screen)
        pygame.display.flip()

#this calls the 'main' function when this script is executed
if __name__ == '__main__':
    main()
