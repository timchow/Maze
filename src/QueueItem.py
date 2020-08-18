class QueueItem(object):
    def __init__(self, row, column, direction, parent = None):
        self.row = row
        self.col = column
        self.direction = direction
        self.parent = parent
