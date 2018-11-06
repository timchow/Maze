# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 15:06:57 2018

@author: tchow
"""

import random, math, itertools, queue
from PIL import Image
from DisjointSets import DisjointSets
from Direction import Direction
from Orientation import Orientation
from MazeCell import MazeCell

class Color(object):
    BLACK = (0,0,0)
    WHITE = (255,255,255)
    RED = (255,0,0)

class MazeSolution(object):
    def __init__(self, path = [], found = False, endRow = None, endCol = None):
        self.path = path
        self.found = found
        self.endRow = endRow
        self.endCol = endCol
        
class QueueItem(object):
    def __init__(self, row, column, direction, parent = None):
        self.row = row
        self.col = column
        self.direction = direction
        self.parent = parent

class Maze(object):

    ScaleFactor = 10

    def __init__(self):
        self.width = 0
        self.height = 0
        self.canvasWidth = 0
        self.canvasHeight = 0
        self.mazeCells = []
    
    
    def MakeMaze(self, width, height):
        self.width = width
        self.height = height
        self.canvasWidth = width * self.ScaleFactor
        self.canvasHeight = height * self.ScaleFactor
        self.disjointSets = DisjointSets(width*height)
        self.mazeCells = [[MazeCell(x,y) for y in range(0,height)] for x in range(0,width)]
    
        for i in range(0,2):
            Xs = list(range(self.width))
            Ys = list(range(self.height))
            randomCoords = list(itertools.product(Xs,Ys)) # cartesian product X x Y
            random.shuffle(randomCoords)
            
            for (row,column) in randomCoords:
                mazeCell = self.mazeCells[row][column]
                wallRemoveDirection = random.sample([Direction.RIGHT,Direction.DOWN],1)[0]
                
                if (mazeCell.visitedCount == 1):
                    wallRemoveDirection = Direction.RIGHT if mazeCell.rightWallExists else Direction.DOWN
                
                a = self._findSetIndex(row,column)
                b = self._findSetIndex(row,column,wallRemoveDirection)
                
                if (self._checkBoundary(row,column,wallRemoveDirection) and self.disjointSets.SetUnion(a,b)):
                    self._setWall(mazeCell,wallRemoveDirection,False)
                    
                mazeCell.visitedCount += 1
            
            
    # solution is the longest path
    def SolveMaze(self):
        longestPath = []
        destinationRow = self.height-1
        
        for destinationColumn in range(self.width):
            emptySolution = MazeSolution([],False)
            solvedMaze = self._solveMazeDFSRecursive(0,0,emptySolution,destinationRow,destinationColumn)
            
            self._resetMazeCells()
            
            if (len(solvedMaze.path) > len(longestPath)):
                longestPath = solvedMaze.path
        
        return longestPath
    
    
    def SolveMazeBFS(self):
        longestPath = []
        destinationRow = self.height-1    
        
        for destinationColumn in range(self.width):
            emptySolution = MazeSolution([],False)
            solvedMaze = self._solveMazeBFSIterative(0,0,emptySolution,destinationRow,destinationColumn)
            
            self._resetMazeCells()
            
            if (len(solvedMaze.path) > len(longestPath)):
                longestPath = solvedMaze.path
        
        return longestPath
    
    
    def _resetMazeCells(self):
        for row in range(self.height):
            for col in range(self.width):
                self.mazeCells[row][col].marked = False
    
    
    def _findSetIndex(self, row, column, direction = Direction.NONE):
        if direction is Direction.NONE:
            return (row*self.width) + column
        return (row*self.width) + column + 1 if direction is Direction.RIGHT else ((row+1)*self.width)+column
    
    
    def _setWall(self, mazeCell, direction, exists):
        if (direction is Direction.RIGHT):
            mazeCell.rightWallExists = exists
        elif (direction is Direction.DOWN):
            mazeCell.downWallExists = exists
            
    # Recursive DFS
    # TODO: Iterative DFS, BFS
    def _solveMazeDFSRecursive(self, row, column, sln, targetRow, targetColumn):
        self.mazeCells[row][column].marked = True
        
        if (row == targetRow and column == targetColumn):
            sln.found = True
            return sln
        
        if (self._canTravel(row,column,Direction.RIGHT)):
            sln.path.append(Direction.RIGHT)
            potSln = self._solveMazeDFSRecursive(row,column+1,sln,targetRow,targetColumn)
            if potSln.found == True:
                return potSln
            else:
                sln.path.pop()
            
        if (self._canTravel(row,column,Direction.DOWN)):
            sln.path.append(Direction.DOWN)
            potSln = self._solveMazeDFSRecursive(row+1,column,sln,targetRow,targetColumn)
            if potSln.found == True:
                return potSln
            else:
                sln.path.pop()
        
        if (self._canTravel(row,column,Direction.UP)):
            sln.path.append(Direction.UP)
            potSln = self._solveMazeDFSRecursive(row-1,column,sln,targetRow,targetColumn)
            if potSln.found == True:
                return potSln
            else:
                sln.path.pop()
                
        if (self._canTravel(row,column,Direction.LEFT)):
            sln.path.append(Direction.LEFT)
            potSln = self._solveMazeDFSRecursive(row,column-1,sln,targetRow,targetColumn)
            if potSln.found == True:
                return potSln
            else:
                sln.path.pop()
        
        return sln
    
    
    def addNeighborsToQueue(self,qItem,q):
        if self._canTravel(qItem.row,qItem.col,Direction.DOWN):
            item = QueueItem(qItem.row+1,qItem.col,Direction.DOWN,qItem)
            q.put(item)
            
        if self._canTravel(qItem.row,qItem.col,Direction.RIGHT):
            item = QueueItem(qItem.row,qItem.col+1,Direction.RIGHT,qItem)
            q.put(item)

        if self._canTravel(qItem.row,qItem.col,Direction.UP):
            item = QueueItem(qItem.row-1,qItem.col,Direction.UP,qItem)
            q.put(item)
            
        if self._canTravel(qItem.row,qItem.col,Direction.LEFT):
            item = QueueItem(qItem.row,qItem.col-1,Direction.LEFT,qItem)
            q.put(item)
    
    
    def _solveMazeBFSIterative(self, row, column, sln, targetRow, targetColumn):
        q = queue.Queue()
        q.put(QueueItem(row,column,None))
        
        while not q.empty():
            qItem = q.get()
            self.mazeCells[qItem.row][qItem.col].marked = True
            
            if qItem.row == targetRow and qItem.col == targetColumn:
                sln.found = True
                sln.path = self._createPathFromQueueItems(qItem)
                return sln
                
            self.addNeighborsToQueue(qItem,q)
    
    
    def _createPathFromQueueItems(self,qItem):
        path = []
        
        while qItem is not None:
            path.insert(0,qItem.direction)
            qItem = qItem.parent
            
        return path
    
    
    def _drawMaze(self):
        imageWidth = (self.canvasWidth)+1
        imageHeight = (self.canvasHeight)+1
        size = (imageWidth,imageHeight)
        img = Image.new('RGB',size,"white")
        pixels = img.load()
        
        self._blackenTop(pixels)
        self._blackenLeft(pixels)
        self._blackenCells(pixels)
        
        return img
    
    
    def _drawMazeWithSolution(self,solution):
        img = self._drawMaze()
        pixels = img.load()
        
        currentRow = math.floor(self.ScaleFactor/2)
        currentCol = math.floor(self.ScaleFactor/2)
        
        for step in solution:
            if (step is Direction.DOWN):
                self._colorWall(pixels, Orientation.VERTICAL, currentRow, currentRow+self.ScaleFactor,currentCol, Color.RED)
                currentRow += self.ScaleFactor
                
            elif (step is Direction.RIGHT):
                self._colorWall(pixels, Orientation.HORIZONTAL, currentCol, currentCol+self.ScaleFactor, currentRow, Color.RED)
                currentCol += self.ScaleFactor
            
            elif (step is Direction.LEFT):
                self._colorWall(pixels, Orientation.HORIZONTAL, currentCol-self.ScaleFactor, currentCol, currentRow, Color.RED)
                currentCol -= self.ScaleFactor
                
            elif (step is Direction.UP):
                self._colorWall(pixels, Orientation.VERTICAL, currentRow-self.ScaleFactor, currentRow,currentCol, Color.RED)
                currentRow -= self.ScaleFactor
        
        currentRow += math.floor(self.ScaleFactor/2)
        currentCol -= math.floor(self.ScaleFactor/2)
        
        # Drawing exit
        self._colorWall(pixels, Orientation.HORIZONTAL,currentCol,currentCol+self.ScaleFactor,currentRow,Color.WHITE)
        
        img.show()
        
        
    def _blackenCells(self, pixels):
        for row in range(self.height):
            for column in range(self.width):
                mazeCell = self.mazeCells[row][column]
                
                if (mazeCell.rightWallExists):
                    rowStart = (row*self.ScaleFactor)
                    columnFixed = (column*self.ScaleFactor) + MazeCell.RIGHT_WALL_OFFSET_PX
                    self._colorWall(pixels, Orientation.VERTICAL, rowStart, rowStart+self.ScaleFactor, columnFixed, Color.BLACK)
                    
                if (mazeCell.downWallExists):
                    rowFixed = (row*self.ScaleFactor) + MazeCell.DOWN_WALL_OFFSET_PX
                    columnStart = (column*self.ScaleFactor)
                    self._colorWall(pixels, Orientation.HORIZONTAL, columnStart, columnStart+self.ScaleFactor, rowFixed, Color.BLACK)
    
    
    def _blackenTop(self, pixels):
        DOOR_OFFSET = 10
        self._colorWall(pixels, Orientation.HORIZONTAL, DOOR_OFFSET, self.canvasWidth, 0, Color.BLACK)
    
    
    def _blackenLeft(self,pixels):
        self._colorWall(pixels, Orientation.VERTICAL, 0, self.canvasHeight, 0, Color.BLACK)
            
        
    def _colorWall(self, pixels, orientation, start, end, fixedDimension, color):
        if (orientation is Orientation.VERTICAL):
            for i in range(start,end):
                pixels[fixedDimension,i] = color
        
        elif (orientation is Orientation.HORIZONTAL):
            for i in range(start,end):
                pixels[i,fixedDimension] = color
            
            
    def _canTravel(self,row,column,direction):
        return self._checkBoundary(row,column,direction) and \
                not self._hasWall(row,column,direction) and \
                not self._isVisited(row,column,direction)
    
    
    def _isVisited(self,row,column,direction):
        if (direction is Direction.DOWN):
            return (self.mazeCells[row+1][column].marked)
        elif (direction is Direction.RIGHT):
            return (self.mazeCells[row][column+1].marked)
        elif (direction is Direction.LEFT):
            return (self.mazeCells[row][column-1].marked)
        elif (direction is Direction.UP):
            return (self.mazeCells[row-1][column].marked)
        
        
    def _checkBoundary(self,row,column,direction):
        if (direction is Direction.DOWN):
            return (row + 1 <= self.height-1)
        elif (direction is Direction.RIGHT):
            return (column + 1 <= self.width-1)
        elif (direction is Direction.LEFT):
            return (column - 1 >= 0)
        elif (direction is Direction.UP):
            return (row - 1 >= 0)
    
    
    def _hasWall(self,row,column,direction):
        if (direction is Direction.RIGHT):
            return self.mazeCells[row][column].rightWallExists
        elif (direction is Direction.DOWN):
            return self.mazeCells[row][column].downWallExists
        elif (direction is Direction.LEFT):
            return self.mazeCells[row][column-1].rightWallExists
        elif (direction is Direction.UP):
            return self.mazeCells[row-1][column].downWallExists
        
        
if __name__ == '__main__':
    maze = Maze()
    maze.MakeMaze(20,20)
    mazeSolution = maze.SolveMaze()
    maze._drawMazeWithSolution(mazeSolution)
    
    mazeSolution2 = maze.SolveMazeBFS()
    maze._drawMazeWithSolution(mazeSolution2)
        