#!/usr/bin/env python

import os
import os.path
import pygame
from pygame.locals import *

class BadFrameStack(Exception):
    def __init__(self, info):
        Exception.__init__(self, info)
        self.__info = info

    def __str__(self):
        return repr(self.__info)

class FrameStack:
    def __init__(self, basename = None):
        self.frames = []
        self.groups = {}
        if not basename is None:
            self.load_group('initial', basename)

    def __load_image(self, fullname):
        try:
            image = pygame.image.load(fullname)
        except pygame.error, message:
            print 'Cannot load image:', fullname
            raise SystemExit, message
        return image.convert_alpha()

    def __get_filenames(self, basename):
        for frame_n in range(1, 100):
            filename = basename + '%02d' % frame_n + '.png'
            yield filename

    def load_group(self, group_name, basename):
        self.frames = []
        nframe = 0
        group = []
        for filename in self.__get_filenames(basename):
            if not os.path.exists(filename):
                break
            self.frames.append(self.__load_image(filename))
            group.append(nframe)
            nframe += 1
        self.groups[group_name] = group

    def group_exists(self, group):
        return self.groups.has_key(group)

    def get_group(self, group):
        if not self.group_exists(group):
            raise BadFrameStack('Frame group not found: ' + group)
        return self.groups[group]

    def copy_group(self, old, new):
        if not self.group_exists(old):
            raise BadFrameStack('Frame group not found: ' + old)
        new_grp = []
        first = len(self.frames)
        for frame in self.groups[old]:
            new_grp.append(first)
            self.frames.append(self.frames[frame].copy())
            first += 1
        self.groups[new] = new_grp

    def delete_group(self, group):
        if not self.group_exists(group):
            raise BadFrameStack('Frame group not found: ' + group)
        del(self.groups[group])

    def vflip_group(self, group):
        if not self.group_exists(group):
            raise BadFrameStack('Frame group not found: ' + group)

        for frame in self.groups[group]:
            self.frames[frame] = pygame.transform.flip(self.frames[frame], 1, 0)

    def hflip_group(self, group):
        if not self.group_exists(group):
            raise BadFrameStack('Frame group not found: ' + group)

        for frame in self.groups[group]:
            self.frames[frame] = pygame.transform.flip(self.frames[frame], 0, 1)

    def scale_group(self, group, scale_factor_x, scale_factor_y = None):
        if not self.group_exists(group):
            raise BadFrameStack('Frame group not found: ' + group)

        if scale_factor_y is None:
            scale_factor_y = scale_factor_x

        for frame in self.groups[group]:
            resolution = self.frames[frame].get_rect()
            new_res_x = int(float(resolution.width) * float(scale_factor_x))
            new_res_y = int(float(resolution.height) * float(scale_factor_y))
            self.frames[frame] = pygame.transform.scale(self.frames[frame], (new_res_x, new_res_y))
