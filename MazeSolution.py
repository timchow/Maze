# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 17:07:52 2018

@author: tchow
"""

class MazeSolution(object):
    def __init__(self, path = [], found = False, endRow = None, endCol = None):
        self.path = path
        self.found = found
        self.endRow = endRow
        self.endCol = endCol