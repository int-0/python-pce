#!/usr/bin/env python

import sys
import uuid
import math
import pygame

class Walkable:
    def __init__(self, rect_area):
        self.rect = rect_area
        self.rect.normalize()

        self.id = uuid.uuid4()

        # Walkable neighbors
        self.__neighbors = []

        # Common-center points with neighbors
        self.__npoints = {}

    def get_id(self):
        return self.id

    def get_rect(self):
        return self.rect

    def absolute_to_relative(self, point):
        return (point[0] - self.__rect.left,
                point[1] - self.__rect.top)

    def relative_to_absolute(self, point):
        return (point[0] + self.__rect.left,
                point[1] + self.__rect.top)

    def get_center_intersection_with(self, rect):
        x = [self.rect.left, self.rect.right, rect.left, rect.right]
        x.sort()
        y = [self.rect.top, self.rect.bottom, rect.top, rect.bottom]
        y.sort()
        
        x1 = x[1]
        y1 = y[1]
        
        centerx = x1 + int((x[2] - x1) / 2)
        centery = y1 + int((y[2] - y1) / 2)

        return (centerx, centery)

    def get_center(self):
        return (self.rect.centerx, self.rect.centery)

    def add_neighbor(self, walkable):
        if walkable.id in self.__neighbors:
            # Already added
            return
        if not self.rect.colliderect(walkable.rect):
            # FIXME: raises an exception: neighbor not collide!
            return
        self.__neighbors.append(walkable.get_id())
        self.__npoints[walkable.get_id()] = self.get_center_intersection_with(walkable.rect)

    def add_neighbors(self, walkables):
        for area in walkables:
            if area.id == self.id:
                # My self!
                continue
            self.add_neighbor(area)

    def has_neighbor(self, neighbor):
        return neighbor.id in self.__neighbors

    def get_neighbors(self):
        return self.__neighbors

    def __distance(self, p1, p2):
        x = p2[0] - p1[0]
        y = p2[1] - p1[1]
        return int(math.sqrt((x * x) + (y * y)))

    def get_graph(self, extra_points = []):
        # Collect points
        points = extra_points
        points.append(self.get_center())
        for center_collide in self.__npoints.values():
            points.append(center_collide)
        # Make connected graph
        graph = {}
        for vertex in points:
            graph[vertex] = {}
            for point in points:
                if vertex == point:
                    continue
                graph[vertex].update({ point : self.__distance(vertex,
                                                               point) })
        # print 'Area:', self.id
        # print '\tPoints:', points
        # print '\tGraph:', graph
        return graph

class WalkableMap:
    def __init__(self):
        self.__areas = {}
        # self.__obstacles = {}

    def add_area(self, new_area):
        # Already added
        if self.__areas.has_key(new_area.id):
            return

        # Update neighbor info of current areas
        for area in self.__areas.values():
            area.add_neighbor(new_area)

        # Update area with neighbor info
        new_area.add_neighbors(self.__areas.values())

        # Add it
        self.__areas[new_area.id] = new_area

    def is_walkable(self, point):
        # Point collide in some walkable area?
        for area in self.__areas.values():
            if area.rect.collidepoint(point):
                return True

        return False

    def __get_walkable_of(self, point):
        for area in self.__areas.keys():
            if self.__areas[area].rect.collidepoint(point):
                return area

    def __join_graph(self, graph1, graph2):
        new_graph = graph1
        for vertex in graph2.keys():
            if new_graph.has_key(vertex):
                new_graph[vertex].update(graph2[vertex])
            else:
                new_graph.update({ vertex : graph2[vertex] })
        return new_graph

    def get_path(self, from_point, to_point):
        from_area = self.__get_walkable_of(from_point)
        to_area = self.__get_walkable_of(to_point)

        # Construct graph
        #
        # FIXME: update() method not work because replaces entire point
        # distances instead of append new distances:
        #  a = { (1,1):1, (2,2):2}
        #  a.update({ (2, 2):3, (3, 3): 4) })
        #
        #  expected a = {(1, 1):1, (2, 2):[2, 3], (3, 3):4}
        #  obtained a = {(1, 1):1, (2, 2):3, (3, 3):4}
        #
        # Note: values are examples!
        
        graph = {}
        for area in self.__areas.values():
            points = []
            if area.id == from_area:
                points.append(from_point)
            if area.id == to_area:
                points.append(to_point)
            graph = self.__join_graph(graph, area.get_graph(points))

        # Search shortest path
        # print 'Graph:', graph
        return self.__shortestpath(graph, from_point, to_point)[1]

    # Shortest path by Dijkstra (recursive)
    def __shortestpath(self,
                       graph, 
                       start, end,
                       visited = [],
                       distances = {}, predecessors = {}):
        """Implementation from: http://rebrained.com/?p=392&cpage=1"""
        # print 'Start:', start, ' End:', end
        # print 'Distances:', distances
        # print 'Visited:', visited
        # print 'Predecessors:', predecessors
        # detect if it's the first time through, set current distance to zero
        if not visited:
            distances[start] = 0
        if start == end:
            # we've found our end node, now find the path to it, and return
            path = []
            while end != None:
                path.append(end)
                end = predecessors.get(end, None)
            return distances[start], path[::-1]

        # process neighbors as per algorithm, keep track of predecessors
        for neighbor in graph[start]:
            if neighbor not in visited:
                neighbordist = distances.get(neighbor, sys.maxint)
                tentativedist = distances[start] + graph[start][neighbor]
                if tentativedist < neighbordist:
                    distances[neighbor] = tentativedist
                    predecessors[neighbor] = start

        # neighbors processed, now mark the current node as visited
        visited.append(start)

        # finds the closest unvisited node to the start
        unvisiteds = dict(
            (k,
             distances.get(k, sys.maxint)) for k in graph if k not in visited)
        closestnode = min(unvisiteds, key = unvisiteds.get)

        # now we can take the closest node and recurse, making it current
        return self.__shortestpath(graph,
                                   closestnode, end,
                                   visited, distances,
                                   predecessors)

# Simple test: make two areas and find path from one to other
#
if __name__ == '__main__':
    map = WalkableMap()
    map.add_area(Walkable(pygame.Rect(0, 0, 200, 200)))
    map.add_area(Walkable(pygame.Rect(90, 0, 300, 300)))
    print map.get_path((10, 10), (200, 20))
