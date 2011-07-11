#!/usr/bin/env python
#

import os
import os.path
import pygame
from pygame.locals import *
from orderedrender import OrderedRenderUpdates
from itemregistry import ItemRegistry
from scene import Scene
from events import EventChannel
from framestack import FrameStack
from animstack import AnimationStack
from animstack import Drawable

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
    pygame.display.set_caption('PCE Test')
    pygame.mouse.set_visible(1)

    # Create game objects
    events = EventChannel()
    registry = ItemRegistry(events)

    # Load objects
    arcade_frames = FrameStack('test_data/arcade')
    arcade_anim = AnimationStack(arcade_frames)
    arcade = Drawable(arcade_anim)
    arcade.set_pos((400, 100))

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
        load_image('test_data/scene.png'),
        load_image('test_data/room_mask.png')
        )

    # Add objects to scene
    scene.set_attrezo(arcade, 'arcade')

    # Main Loop
    while 1:
        clock.tick(20)

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
