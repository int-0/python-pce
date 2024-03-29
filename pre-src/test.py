#!/usr/bin/env python
#

import os
import os.path
import pygame
from pygame.locals import *
from orderedrender import OrderedRenderUpdates
from item import Item
from itemregistry import ItemRegistry
from actorregistry import ActorRegistry
from scene import Scene
from events import EventChannel
from framestack import FrameStack
from animstack import AnimationStack
from animstack import Drawable
from actor import Actor

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
    items = ItemRegistry(events)
    actors = ActorRegistry(events)

    # Load objects
    arcade_frames = FrameStack('test_data/arcade')
    arcade_anim = AnimationStack(arcade_frames)
    arcade = Drawable(arcade_anim)
    arcade.set_pos((400, 100))

    # Load items
    ttpie_frames = FrameStack('test_data/ttpie_static_')
    ttpie_frames.load_group('action', 'test_data/ttpie')
    ttpie_anim = AnimationStack(ttpie_frames)
    ttpie = Item(ttpie_anim)
    ttpie.set_state('active', { 'handler' : None,
                                'animation' : 'action',
                                'next_state' : 'initial' })
    ttpie.set_state('initial', { 'handler' : None,
                                 'animation' : 'initial',
                                 'next_state' : 'active' })
    ttpie.set_pos((300, 400))
    items.add('ttpie', ttpie)

    # Load actors
    tory_frames = FrameStack('test_data/tory_static')
    tory_frames.load_group('WALK_O', 'test_data/tory_walk')
    tory_frames.load_group('WALK_ON', 'test_data/tory_uwalk')
    tory_frames.copy_group('WALK_ON', 'WALK_N')
    tory_frames.copy_group('WALK_ON', 'WALK_EN')
    tory_frames.vflip_group('WALK_EN')
    tory_frames.copy_group('WALK_O', 'WALK_E')
    tory_frames.vflip_group('WALK_E')
    tory_frames.copy_group('WALK_O', 'WALK_S')
    tory_frames.copy_group('WALK_O', 'WALK_OS')
    tory_frames.copy_group('WALK_O', 'WALK_ES')
    tory_frames.vflip_group('WALK_ES')
    tory_frames.load_group('action_o', 'test_data/tory_action')
    tory_anim = AnimationStack(tory_frames)
    tory = Actor(tory_anim)
    tory.set_pos((500, 400))
    actors.add('tory', tory)

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

    # Enable items in scene
    scene.show_item('ttpie')
    scene.show_actor('tory')

    # Main Loop
    while 1:
        clock.tick(20)

        # Handle Input Events
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    # Generate syntethic event
                    move_event = {
                        'dest' : ['tory'],
                        'op' : 'walk_to',
                        'position' : event.pos
                        }
                    scene.fire_event(move_event)
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
