from pathlib import Path

import ipyvuetify as v 
from sepal_ui import sepalwidgets as sw

from component.message import cm

class OutDirSelect(sw.SepalWidget, v.TextField):
    
    def __init__(self, **kwargs):
        
        # default parameters 
        self.v_model=None
        self.label=cm.widget.out_dir.label
        self.readonly=True
        self.hint=cm.widget.out_dir.hint
        self.class_="mb-2"
        #self.persistent_hint=True
        
        # create the widget
        super().__init__(**kwargs)
        
    def set_folder(self, path):
        """use the path of the time_series to name the folder that is used to store the information"""
        
        # unsure it's a path
        path = Path(path)
        
        # change the v_model 
        self.v_model = path.stem
        
        return self
        
        
        
        
        
        
        