# if you only have few widgets, a module is not necessary and you can simply use a widget.py file
# in a big module with lot of custom widgets, it can make sense to split things in separate files for the sake of maintenance

# if you use a module import all the functions here to only have 1 call to make
from .folder_select import *
from .out_dir_select import *
from .tiles_select import *
from .backend_select import *
from .date_slider import *
from .date_range_slider import *
from .custom_alert import *
