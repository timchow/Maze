# This class was formed to create easier access to Color.
# So that Color.BLACK can be manipulated by an iterating 
# function such as tuple/list and allowing Color.BLACK.name 
# to return a string

class ColorProperties(object):
    def __init__(self,farg,*argv):
        self.name = farg
        self.value = argv[0]
        
    def __repr__(self):
        return str(self.value)
    
    def __iter__(self):
        for i in self.value:
            yield i

class Color(object):
    _black = (0,0,0)
    _white = (255,255,255)
    _red = (255,0,0)

    BLACK = ColorProperties("BLACK",_black)
    WHITE = ColorProperties("WHITE",_white)
    RED = ColorProperties("RED",_red)
    