# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 17:06:21 2018

@author: tchow
"""

class QueueItem(object):
    def __init__(self, row, column, direction, parent = None):
        self.row = row
        self.col = column
        self.direction = direction
        self.parent = parent
