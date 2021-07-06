# if you only have few parameters, a module is not necessary and you can simply use a tile.py file 
# in a big module with lot of parameters, it can make sense to split things in separate for the sake of maintenance
# this should be the only place you hard-code parameters

# if you use a module import all the functions here to only have 1 call to make
from .directory import *
from .bfast import *
from .viz import *