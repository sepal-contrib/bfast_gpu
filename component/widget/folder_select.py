from pathlib import Path

from sepal_ui import sepalwidgets as sw 

from component import parameter as cp
from component.message import cm

class FolderSelect(sw.FileInput):
    
    def __init__(self, folder=cp.down_dir):
        
        super().__init__([''], label=cm.widget.folder.label, folder=folder)
        
    def _on_file_select(self, change):
        """Dispatch the behaviour between file selection and folder change"""
        
        if not change['new']:
            return self
        
        new_value = Path(change['new'])
        
        # I keep the same behaviour but I write the value for each directory as no file will ever be selected
        if new_value.is_dir():
            self.folder = new_value
            self.file = str(new_value)
            self._change_folder()            
            
        return self
    
    def is_valid_ts(self):
        """Check if the current folder is a SEPAL generated time series folder"""
        
        # clean the errors 
        self.selected_file.error_messages = None
        
        # avoid bug at start 
        if not self.v_model:
            return True
        
        folder = Path(self.v_model)
        
        valid = True
        dirs = [d for d in folder.glob('*/')]
        if len(dirs) == 0: 
            valid = False
        else:
            for d in dirs:
                try:
                    n = int(d.stem)
                except:
                    valid = False
                    break
                    
        # write an error message 
        self.selected_file.error_messages = None if valid else cm.widget.folder.no_ts.format('')  
        
        return valid