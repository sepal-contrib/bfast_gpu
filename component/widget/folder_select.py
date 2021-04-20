from pathlib import Path

from sepal_ui import sepalwidgets as sw 

from component import parameter as cp

class FolderSelect(sw.FileInput):
    
    def __init__(self):
        
        super().__init__([''], label="Select Folder", folder=cp.down_dir)
        
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