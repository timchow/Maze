# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 11:17:14 2018

@author: tchow
"""

class DisjointSets:
    
    def __init__(self, size):
        self.uptrees = []
        self.Add(size)
        
    def Add(self, size):
        for idx in range(0,size):
            self.uptrees.append(-1)
            
    # Returns the index of the root
    def FindRoot(self, eIdx):
        if (eIdx < 0):
            return -1
        
        if (eIdx < len(self.uptrees) and self.uptrees[eIdx] < 0):
            return eIdx
        
        return self.FindRoot(self.uptrees[eIdx])
    
    # e1,e2 represent indices
    def SetUnion(self, e1, e2):
        if (e1 >= len(self.uptrees) or e2 >= len(self.uptrees)):
            return False
        
        root1Idx = self.FindRoot(e1)
        root2Idx = self.FindRoot(e2)
        
        # Already part of the same set
        if (root1Idx == root2Idx):
            return False
        
        size = self.uptrees[root1Idx] + self.uptrees[root2Idx]

        if (abs(self.uptrees[root1Idx]) > abs(self.uptrees[root2Idx])):
            self.uptrees[root2Idx] = root1Idx
            self.uptrees[root1Idx] = size
        else:
            self.uptrees[root1Idx] = root2Idx
            self.uptrees[root2Idx] = size
        
        return True
        
        
        
        