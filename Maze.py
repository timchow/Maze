import random
import itertools
from PIL import Image
from DisjointSets import DisjointSets
from Direction import Direction
from Orientation import Orientation
from MazeCell import MazeCell
from Color import Color
from MazeSolver import MazeSolver


class Maze(object):

    SCALE_FACTOR = 10

    def __init__(self):
        self.width = 0
        self.height = 0
        self.canvasWidth = 0
        self.canvasHeight = 0
        self.mazeCells = []

    def MakeMaze(self, width, height):
        self.width = width
        self.height = height
        self.canvasWidth = width * self.SCALE_FACTOR
        self.canvasHeight = height * self.SCALE_FACTOR
        self.disjointSets = DisjointSets(width*height)
        self.mazeCells = [[MazeCell(x, y) for y in range(height)]
                          for x in range(0, width)]

        Xs = list(range(self.width))
        Ys = list(range(self.height))
        # cartesian product X x Y
        randomCoords = list(itertools.product(Xs, Ys))
        randomCoords.extend(randomCoords)
        random.shuffle(randomCoords)

        for (row, column) in randomCoords:
            mazeCell = self.mazeCells[row][column]
            wallRemoveDirection = random.sample(
                [Direction.RIGHT, Direction.DOWN], 1)[0]

            if (mazeCell.visitedCount == 1):
                wallRemoveDirection = Direction.RIGHT if mazeCell.rightWallExists else Direction.DOWN

            a = self._findSetIndex(row, column)
            b = self._findSetIndex(row, column, wallRemoveDirection)

            if (self._checkBoundary(row, column, wallRemoveDirection) and self.disjointSets.SetUnion(a, b)):
                self._setWall(mazeCell, wallRemoveDirection, False)

            mazeCell.visitedCount += 1

    def _resetMazeCells(self):
        for row in range(self.height):
            for col in range(self.width):
                self.mazeCells[row][col].marked = False

    def _findSetIndex(self, row, column, direction=Direction.NONE):
        if direction is Direction.NONE:
            return (row*self.width) + column

        return (row*self.width) + column + 1 if direction is Direction.RIGHT else ((row+1)*self.width)+column

    def _setWall(self, mazeCell, direction, exists):
        if (direction is Direction.RIGHT):
            mazeCell.rightWallExists = exists
        elif (direction is Direction.DOWN):
            mazeCell.downWallExists = exists

    def _drawMaze(self):
        imageWidth = (self.canvasWidth)+1
        imageHeight = (self.canvasHeight)+1
        size = (imageWidth, imageHeight)
        img = Image.new('RGB', size, Color.WHITE.name)
        pixels = img.load()

        self._blackenTop(pixels)
        self._blackenLeft(pixels)
        self._blackenCells(pixels)

        return img

    def DrawMaze(self, solution):
        img = self._drawMaze()
        pixels = img.load()

        currentRow = self.SCALE_FACTOR // 2
        currentCol = self.SCALE_FACTOR // 2

        for step in solution.path:
            if (step is Direction.DOWN):
                self._colorWall(pixels, Orientation.VERTICAL, currentRow,
                                currentRow+self.SCALE_FACTOR, currentCol, Color.RED)
                currentRow += self.SCALE_FACTOR

            elif (step is Direction.RIGHT):
                self._colorWall(pixels, Orientation.HORIZONTAL, currentCol,
                                currentCol+self.SCALE_FACTOR, currentRow, Color.RED)
                currentCol += self.SCALE_FACTOR

            elif (step is Direction.LEFT):
                self._colorWall(pixels, Orientation.HORIZONTAL, currentCol -
                                self.SCALE_FACTOR, currentCol, currentRow, Color.RED)
                currentCol -= self.SCALE_FACTOR

            elif (step is Direction.UP):
                self._colorWall(pixels, Orientation.VERTICAL, currentRow -
                                self.SCALE_FACTOR, currentRow, currentCol, Color.RED)
                currentRow -= self.SCALE_FACTOR

        currentRow += self.SCALE_FACTOR // 2
        currentCol -= self.SCALE_FACTOR // 2

        # Drawing exit
        self._colorWall(pixels,
                        Orientation.HORIZONTAL,
                        currentCol,
                        currentCol + self.SCALE_FACTOR,
                        currentRow,
                        Color.WHITE)

        img.show()
    
    def DrawMazeStepWise(self, solution):
        img = self._drawMaze()
        pixels = img.load()

        currentRow = self.SCALE_FACTOR // 2
        currentCol = self.SCALE_FACTOR // 2

        for step in solution.path:
            if (step is Direction.DOWN):
                self._colorWall(pixels, Orientation.VERTICAL, currentRow,
                                currentRow+self.SCALE_FACTOR, currentCol, Color.RED)
                currentRow += self.SCALE_FACTOR

            elif (step is Direction.RIGHT):
                self._colorWall(pixels, Orientation.HORIZONTAL, currentCol,
                                currentCol+self.SCALE_FACTOR, currentRow, Color.RED)
                currentCol += self.SCALE_FACTOR

            elif (step is Direction.LEFT):
                self._colorWall(pixels, Orientation.HORIZONTAL, currentCol -
                                self.SCALE_FACTOR, currentCol, currentRow, Color.RED)
                currentCol -= self.SCALE_FACTOR

            elif (step is Direction.UP):
                self._colorWall(pixels, Orientation.VERTICAL, currentRow -
                                self.SCALE_FACTOR, currentRow, currentCol, Color.RED)
                currentRow -= self.SCALE_FACTOR
            
            #img.show()

        currentRow += self.SCALE_FACTOR // 2
        currentCol -= self.SCALE_FACTOR // 2

        # Drawing exit
        self._colorWall(pixels,
                        Orientation.HORIZONTAL,
                        currentCol,
                        currentCol + self.SCALE_FACTOR,
                        currentRow,
                        Color.WHITE)

        img.show()

    def _blackenCells(self, pixels):
        for row in range(self.height):
            for column in range(self.width):
                mazeCell = self.mazeCells[row][column]

                if (mazeCell.rightWallExists):
                    rowStart = (row*self.SCALE_FACTOR)
                    columnFixed = (column*self.SCALE_FACTOR) + \
                        MazeCell.RIGHT_WALL_OFFSET_PX
                    self._colorWall(pixels, Orientation.VERTICAL, rowStart,
                                    rowStart+self.SCALE_FACTOR, columnFixed, Color.BLACK)

                if (mazeCell.downWallExists):
                    rowFixed = (row*self.SCALE_FACTOR) + \
                        MazeCell.DOWN_WALL_OFFSET_PX
                    columnStart = (column*self.SCALE_FACTOR)
                    self._colorWall(pixels, Orientation.HORIZONTAL, columnStart,
                                    columnStart+self.SCALE_FACTOR, rowFixed, Color.BLACK)

    def _blackenTop(self, pixels):
        DOOR_OFFSET = 10
        self._colorWall(pixels, Orientation.HORIZONTAL,
                        DOOR_OFFSET, self.canvasWidth, 0, Color.BLACK)

    def _blackenLeft(self, pixels):
        self._colorWall(pixels, Orientation.VERTICAL, 0,
                        self.canvasHeight, 0, Color.BLACK)

    def _colorWall(self, pixels, orientation, start, end, fixedDimension, color):
        if (orientation is Orientation.VERTICAL):
            for i in range(start, end):
                pixels[fixedDimension, i] = tuple(color)

        elif (orientation is Orientation.HORIZONTAL):
            for i in range(start, end):
                pixels[i, fixedDimension] = tuple(color)

    def _canTravel(self, row, column, direction):
        return self._checkBoundary(row, column, direction) and \
            not self._hasWall(row, column, direction) and \
            not self._isVisited(row, column, direction)

    def _isVisited(self, row, column, direction):
        if (direction is Direction.DOWN):
            return (self.mazeCells[row+1][column].marked)
        elif (direction is Direction.RIGHT):
            return (self.mazeCells[row][column+1].marked)
        elif (direction is Direction.LEFT):
            return (self.mazeCells[row][column-1].marked)
        elif (direction is Direction.UP):
            return (self.mazeCells[row-1][column].marked)

    def _checkBoundary(self, row, column, direction):
        MIN_HEIGHT, MIN_WIDTH = 0, 0
        MAX_HEIGHT = self.height-1
        MAX_WIDTH = self.width-1

        if (direction is Direction.DOWN):
            return (row + 1 <= MAX_HEIGHT)
        elif (direction is Direction.RIGHT):
            return (column + 1 <= MAX_WIDTH)
        elif (direction is Direction.LEFT):
            return (column - 1 >= MIN_WIDTH)
        elif (direction is Direction.UP):
            return (row - 1 >= MIN_HEIGHT)

    def _hasWall(self, row, column, direction):
        if (direction is Direction.RIGHT):
            return self.mazeCells[row][column].rightWallExists
        elif (direction is Direction.DOWN):
            return self.mazeCells[row][column].downWallExists
        elif (direction is Direction.LEFT):
            return self.mazeCells[row][column-1].rightWallExists
        elif (direction is Direction.UP):
            return self.mazeCells[row-1][column].downWallExists


if __name__ == '__main__':
    mazeWidth = 20
    mazeHeight = 20

    maze = Maze()
    maze.MakeMaze(mazeWidth, mazeHeight)

    mazeSolution = MazeSolver(maze).Solve()
    maze.DrawMaze(mazeSolution)

    mazeSolution2 = MazeSolver(maze).SolveBFS()
    maze.DrawMaze(mazeSolution2)