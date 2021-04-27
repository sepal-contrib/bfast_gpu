from sepal_ui import sepalwidgets as sw 
import ipyvuetify as v 

from component.message import cm

class TilesSelect(sw.SepalWidget, v.Select):
    
    def __init__(self, **kwargs):
        
        # default values
        self.label=cm.widget.tiles.label
        self.v_model=None
        self.items=None
        self.chips=True
        self.multiple=True
        self.deletable_chips=True
        
        # create the widget
        super().__init__(**kwargs)
        
    def reset(self):
        """reset the v_model and items values"""
        
        self.v_model = None
        self.items = None
        
        return self
    
    def set_items(self, folder):
        """create selectable items that corresponds to the folders inside the provided folder"""
        
        # update items
        self.items = sorted([d.stem for d in folder.glob('*/')])
        
        # by default selec all available tiles
        self.v_model = self.items
        
        return self