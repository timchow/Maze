class MazeSolution(object):
    def __init__(self, path = [], found = False, endRow = None, endCol = None):
        self.path = path
        self.found = found
        self.endRow = endRow
        self.endCol = endCol