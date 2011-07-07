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

import walkable

class RectFactory:
    def __init__(self, srf, new_rect_cb = None):
        self.srf = srf
        self.r_cb = new_rect_cb
        self.first_point = None

    def set_point(self, point):
        if self.first_point == None:
            self.first_point = point
            return
        rect = pygame.Rect(self.first_point,
                              (point[0] - self.first_point[0],
                               point[1] - self.first_point[1]))
        if not self.r_cb is None:
            self.r_cb(rect)

        self.first_point = None
        self.draw(rect)

    def draw(self, rect):
        pygame.draw.rect(self.srf, 0xffffff, rect, 2)

# Function to show cross
def put_cross(srf, point):
    h1 = (point[0] - 5, point[1])
    h2 = (point[0] + 5, point[1])
    v1 = (point[0], point[1] - 5)
    v2 = (point[0], point[1] + 5)

    pygame.draw.line(srf, 0xffffff, h1, h2)
    pygame.draw.line(srf, 0xffffff, v1, v2)

def main():
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the function returns."""

    # Initialize Everything
    pygame.init()
    screen = pygame.display.set_mode((1024, 768))
    pygame.display.set_caption('Monkey Fever')
    pygame.mouse.set_visible(1)

    # Display The Background
    pygame.display.flip()

    # Prepare Game Objects
    clock = pygame.time.Clock()

    # Walkable areas
    warea = walkable.Walkable()
    # Rect factory
    rfactory = RectFactory(screen, warea.add_rect)

    # Main Loop
    while 1:
        clock.tick(60)

        # Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            elif event.type is MOUSEBUTTONUP:
                rfactory.set_point(event.pos)
                points = warea.get_common_points()
                for point in points:
                    put_cross(screen, point)

        # Draw Everything
        pygame.display.flip()

# Game Over


# This calls the 'main' function when this script is executed
if __name__ == '__main__': main()
