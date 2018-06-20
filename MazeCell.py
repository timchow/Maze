# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 15:02:36 2018

@author: tchow
"""

class MazeCell:

    RIGHT_WALL_OFFSET_PX = 10
    DOWN_WALL_OFFSET_PX = 10

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.rightWallExists = True
        self.downWallExists = True
        self.visitedCount = 0
        self.marked = False
    
    def __repr__(self):
        return 'Coordinates: ({},{}) \nRight Wall: {} \nDown Wall: {} \nVisited: {} '.format(self.x,self.y, self.rightWallExists,self.downWallExists,self.visitedCount)