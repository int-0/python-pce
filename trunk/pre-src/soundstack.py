#!/usr/bin/env python

import os
import os.path
import pygame
from pygame.locals import *

class BadSoundStack(Exception):
    def __init__(self, info):
        Exception.__init__(self, info)
        self.__info = info

    def __str__(self):
        return repr(self.__info)

class SoundStack(object):
    def __init__(self):
        self.__sounds = {}

    def __load_sound(filename):
        class NoSound:
            def play(self): pass
        try:
            return pygame.mixer.Sound(filename)
        except:
            return NoSound()

    def set_sound(self, filename, name):
        self.__sounds[name] = self.__load_sound(filename)

    def play_sound(self, name):
        if not self.__sounds.has_key(name):
            raise BadSoundStack('Cannot play sound: ' + name)
        self.__sounds[name].play()

    def get_sounds(self):
        return self.__sounds.keys()

    def clear_sounds(self):
        self.__sounds = {}

    def remove_sound(self, name):
        if self.__sounds.has_key(name):
            del(self.__sounds[name])

