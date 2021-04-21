# if you only have few funcitions a module is not necessary and you can simply use a scripts.py file 
# in a big module with lot of functions, it can make sense to split things in separate for the sake of maintenance

# if you use a module import all the functions here to only have 1 call to make
from .process import *
