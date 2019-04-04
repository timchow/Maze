from MazeSolution import MazeSolution
from Direction import Direction
from QueueItem import QueueItem
import queue

class MazeSolver(object):
	def __init__(self, maze):
		self.Maze = maze

	def Solve(self):
		return self.__SolveMaze(self.Maze)
	
	def SolveBFS(self):
		return self.__SolveMazeBFS(self.Maze)

	def __SolveMaze(self, maze):
		destinationRow = maze.height-1
		destinationColumn = maze.width-1
		emptySolution = MazeSolution()
		solvedMaze = self.__solveMazeDFSRecursive(self.Maze, 0, 0, emptySolution, destinationRow, destinationColumn)
		maze._resetMazeCells()

		return solvedMaze

	def __SolveMazeBFS(self, maze):
		destinationRow = maze.height-1
		destinationColumn = maze.width-1
		emptySolution = MazeSolution()
		solvedMaze = self.__solveMazeBFSIterative(self.Maze, 0, 0, emptySolution, destinationRow, destinationColumn)
		maze._resetMazeCells()

		return solvedMaze

	def __solveMazeDFSRecursive(self, maze, row, column, sln, targetRow, targetColumn):
		maze.mazeCells[row][column].marked = True

		if (row == targetRow and column == targetColumn):
			sln.found = True
			return sln

		if (maze._canTravel(row, column, Direction.RIGHT)):
			sln.path.append(Direction.RIGHT)
			potSln = self.__solveMazeDFSRecursive(maze, row, column+1, sln, targetRow, targetColumn)
			if potSln.found == True:
				return potSln
			else:
				sln.path.pop()

		if (maze._canTravel(row, column, Direction.DOWN)):
			sln.path.append(Direction.DOWN)
			potSln = self.__solveMazeDFSRecursive(maze, row+1, column, sln, targetRow, targetColumn)
			if potSln.found == True:
				return potSln
			else:
				sln.path.pop()

		if (maze._canTravel(row, column, Direction.UP)):
			sln.path.append(Direction.UP)
			potSln = self.__solveMazeDFSRecursive(maze, row-1, column, sln, targetRow, targetColumn)
			if potSln.found == True:
				return potSln
			else:
				sln.path.pop()

		if (maze._canTravel(row, column, Direction.LEFT)):
			sln.path.append(Direction.LEFT)
			potSln = self.__solveMazeDFSRecursive(maze, row, column-1, sln, targetRow, targetColumn)
			if potSln.found == True:
				return potSln
			else:
				sln.path.pop()

		return sln

	def __addNeighborsToQueue(self, maze, qItem, q):
		if maze._canTravel(qItem.row, qItem.col, Direction.DOWN):
			item = QueueItem(qItem.row+1, qItem.col, Direction.DOWN, qItem)
			q.put(item)

		if maze._canTravel(qItem.row, qItem.col, Direction.RIGHT):
			item = QueueItem(qItem.row, qItem.col+1, Direction.RIGHT, qItem)
			q.put(item)

		if maze._canTravel(qItem.row, qItem.col, Direction.UP):
			item = QueueItem(qItem.row-1, qItem.col, Direction.UP, qItem)
			q.put(item)

		if maze._canTravel(qItem.row, qItem.col, Direction.LEFT):
			item = QueueItem(qItem.row, qItem.col-1, Direction.LEFT, qItem)
			q.put(item)

	def __solveMazeBFSIterative(self, maze, row, column, sln, targetRow, targetColumn):	
		q = queue.Queue()
		q.put(QueueItem(row, column, None))

		while not q.empty():
			qItem = q.get()
			maze.mazeCells[qItem.row][qItem.col].marked = True

			if qItem.row == targetRow and qItem.col == targetColumn:
				sln.found = True
				sln.path = self.__createPathFromQueueItems(qItem)
				return sln

			self.__addNeighborsToQueue(maze, qItem, q)
	
	def __createPathFromQueueItems(self, qItem):
		path = []

		while qItem is not None:
			path.insert(0, qItem.direction)
			qItem = qItem.parent

		return path
