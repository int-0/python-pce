#!/usr/bin/env python

"""
This simple example is used for the line-by-line tutorial
that comes with pygame. It is based on a 'popular' web banner.
Note there are comments here, but for the full explanation, 
follow along in the tutorial.
"""

#Import Modules
import os, pygame
from pygame.locals import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'


#functions to create our resources
def load_image(name):
    try:
        image = pygame.image.load(name)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    image = image.convert_alpha()
    return image

def main():
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the function returns."""

#Initialize Everything
    pygame.init()
    screen = pygame.display.set_mode((1024, 768))
    pygame.display.set_caption('Monkey Fever')
    pygame.mouse.set_visible(1)

#Create The Backgound
    background = load_image('mask.png')

# #Put Text On The Background, Centered
#     if pygame.font:
#         font = pygame.font.Font(None, 36)
#         text = font.render("Pummel The Chimp, And Win $$$", 1, (10, 10, 10))
#         textpos = text.get_rect(centerx=background.get_width()/2)
#         background.blit(text, textpos)

#Display The Background
    screen.blit(background, (0, 0))
    pygame.display.flip()

#Prepare Game Objects
    clock = pygame.time.Clock()

#Main Loop
    while 1:
        clock.tick(60)

    #Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            elif event.type == MOUSEBUTTONDOWN:
                print background.get_at(event.pos)[3]
            elif event.type is MOUSEBUTTONUP:
                pass

    #Draw Everything
        screen.blit(background, (0, 0))
        pygame.display.flip()

#Game Over


#this calls the 'main' function when this script is executed
if __name__ == '__main__': main()
