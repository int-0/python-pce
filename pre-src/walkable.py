#!/usr/bin/env python

import sys
import uuid
import pygame

class WalkableArea:
    def __init__(self, rect_area):
        self.__rect = rect_area
        self.__rect.normalize()

        self.__id = uuid.uuid4()

        # Walkable neighbors
        self.__neighbors = {}
        # Common-center points with neighbors
        self.__npoints = {}

    def get_id(self):
        return self.__id

    def get_rect(self):
        return self.__rect

    def abosulte_to_relative(self, point):
        return (point[0] - self.__rect.left,
                point[1] - self.__rect.top)

    def relative_to_absolute(self, point):
        return (point[0] + self.__rect.left,
                point[1] + self.__rect.top)

    def __get_center_collide_area(self, rect):
        x = [self.__rect.left, self.__rect.right,
             rect.left, rect.right]
        x.sort()
        y = [self.__rect.top, self.__rect.bottom,
             rect.top, rect.bottom]
        y.sort()

        x1 = x[1]
        y1 = y[1]

        dx = int((x[2] - x1) / 2)
        dy = int((y[2] - y1) / 2)

        centerx = x1 + dx
        centery = y1 + dy

        return (centerx, centery)

    def __get_center(self):
        return (self.__rect.centerx, self.__rect.centery)

    def distance_between(self, neighbor1, neighbor2):
        if ((not self.__neighbors.has_key(neighbor1.get_id())) or
            (not self.__neighbors.has_key(neighbor2.get_id()))):
            # Some neighbour is not connected
            return sys.maxint

        p1 = self.__get_center_collide_area(neighbor1.get_rect())
        p2 = self.__get_center_collide_area(neighbor2.get_rect())

        x = p2[0] - p1[0]
        y = p2[1] - p1[1]

        return int(sqrt((x * x) + (y * y)))

    def __add_single_neighbor(self, walkable):
        # This function not check for overlapped area, simply adds
        # to the neighbors tree
        if self.__neighbors.has_key(walkable.get_id()):
            # Already added
            return
        self.__neighbors[walkable.get_id()] = walkable
        self.__npoints[walkable.get_id()] = self.__get_center_collide_area(walkable.get_rect())

    def add_neighbors(self, walkables):
        for area in walkables:
            if area.get_id() == self.__id:
                # My self!
                continue
            if self.__rect.colliderect(area.get_rect()):
                # It is a neighbour
                self.__add_single_neighbor(area)

    def has_neighbor(self, neighbor):
        return self.__neighbors.has_key(neighbor.get_id())

    def get_neighbors(self):
        return self.__neighbors.values()

    def get_neighbor_points(self):
        return self.__npoints.values()

class Walkable:
    def __init__(self, initial = None):
        self.__areas = {}
        if not initial is None:
            self.__areas[initial.get_id()] = initial

    def add_rect(self, rect):
        self.add_area(WalkableArea(rect))

    def add_area(self, new_area):
        # Already added
        if self.__areas.has_key(new_area.get_id()):
            return

        # Update current areas
        for area in self.__areas.values():
            area.add_neighbors([new_area])

        # Update area
        new_area.add_neighbors(self.__areas.values())

        # Add it
        self.__areas[new_area.get_id()] = new_area

    def get_walkable_area_for(self, point):
        # Get area with whis point
        for area in self.__areas.values():
            if area.get_rect().collidepoint(point):
                return area

    def get_areas(self):
        return self.__areas.keys()

    def get_area(self, area_id):
        if not self.__areas.has_key(area_id):
            return
        return self.__areas[area_id]

    def get_common_points(self):
        points = []
        for walkable in self.__areas.values():
            points += walkable.get_neighbor_points()
        return points

    # def get_path(self, from_point, to_point):
    #     from_area = self.get_walkable_area_for(from_point)
    #     to_area = self.get_walkable_area_for(from_point)

    #     # init distances{} = maxint
    #     # init distances[start] = 0
    #     # init visited[] = false

    # def __shortestpath(start, end,
    #                    visited = [],
    #                    distances = {}, predecesors = {}):
    #     pass
