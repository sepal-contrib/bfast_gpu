from pathlib import Path

import ipyvuetify as v
from sepal_ui import sepalwidgets as sw 

from component import widget as cw
from component.message import cm

class BfastTile(sw.Tile):
    
    def __init__(self):
        
        # create the different widgets 
        # I will not use Io as the information doesn't need to be communicated to any other tile
        self.folder = cw.FolderSelect()
        self.out_dir = cw.OutDirSelect()
        self.tiles = cw.TilesSelect()
        self.poly = v.Select(label=cm.widget.harmonic.label, v_model=None, items=[i for i in range(3,11)])
        self.freq = v.Slider(label=cm.widget.freq.label, v_model = None, min=1, max=365, thumb_label="always", class_='mt-5')
        self.trend = v.Switch(v_model=False, label=cm.widget.trend.label)
        self.hfrac = v.Slider(label=cm.widget.hfrac.label, v_model=None, step=.01, max=1.00, thumb_label="always", class_='mt-5')
        self.level = v.Slider(label=cm.widget.level.label, v_model=None, step=.001, max=1.000, thumb_label="always", class_='mt-5')
        self.backend = cw.BackendSelect()
        self.monitoring = cw.DateRangeSlider(label=cm.widget.monitoring.label)
        self.history = cw.DateSlider(label=cm.widget.history.label)
        
        # create the tile 
        super().__init__(
            "BFAST_tile",
            cm.bfast.title,
            inputs=[
                self.folder, self.out_dir, self.tiles,
                v.Divider(),
                self.poly, self.freq, self.trend, self.hfrac, self.level, self.backend,
                v.Divider(),
                self.monitoring, self.history
                
            ],
            output=sw.Alert(),
            btn=sw.Btn(cm.bfast.btn)
        
        )
        
        # add js behaviour 
        self.folder.observe(self._on_folder_change, 'v_model')
        
    def _on_folder_change(self, change):
        """
        Change the available tiles according to the selected folder
        Raise an error if the folder is not structured as a SEPAL time series (i.e. folder number for each tile)
        """
        
        # get the new selected folder 
        folder = Path(change['new'])
        
        # reset the widgets
        self.out_dir.v_model = None
        self.tiles.reset()
        
        # check if it's a time series folder 
        if not self.folder.is_valid_ts():
            
            # reset the non working inputs 
            self.monitoring.disable()
            self.history.disable()
            self.tiles.reset()
            
            # display a message to the end user
            self.output.add_msg(cm.widget.folder.no_ts.format(folder), 'warning')
            
            return self
        
        # set the basename
        self.out_dir.set_folder(folder)
        
        # set the items in the dropdown 
        self.tiles.set_items(folder)
        
        # set the dates for the sliders 
        # we consider that the dates are consistent through all the folders so we can use only the first one
        with (folder/'0'/'dates.csv').open() as f:
            dates = f.read().split('\n')
            
        self.monitoring.set_dates(dates)
        self.history.set_dates(dates)
        
        self.output.add_msg(cm.widget.folder.valid_ts.format(folder))
        
        return self
        
        