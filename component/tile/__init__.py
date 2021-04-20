# if you only have few tiles a module is not necessary and you can simply use a tile.py file 
# in a big module with lot of tiles, it can make sense to split things in separate for the sake of maintenance

# if you use a module import all the functions here to only have 1 call to make
from .bfast_tile import *