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
        
        # create the tile 
        super().__init__(
            "BFAST_tile",
            cm.bfast.title,
            inputs=[self.folder, self.out_dir, self.tiles],
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
            self.output.add_msg(cm.widget.folder.no_ts.format(folder), 'warning')
            return self
        
        # set the basename
        self.out_dir.set_folder(folder)
        
        # set the items in the dropdown 
        self.tiles.set_items(folder)
        
        self.output.add_msg(cm.widget.folder.valid_ts.format(folder))
        
        return self
        
        