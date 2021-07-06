from pathlib import Path

from sepal_ui import sepalwidgets as sw 
import ipyvuetify as v 

from component.message import cm

class BackendSelect(sw.SepalWidget, v.Select):
    
    BACKENDS = [
        {'text': "NumPy", 'value': 'python', 'disabled': False},
        {'text': 'OpenCL', 'value': 'opencl', 'disabled': False},
        {'text': 'CuPy', 'value': 'cupy', 'disabled': False}
    ]
    
    def __init__(self, **kwargs):
        
        # guess if the current instance is a gpu and adapt the backend items accordingly
        items = self.BACKENDS
        value = items[1]['value']
        hint = None
        
        if not self.is_gpu():
            items[1]['disabled'] = True
            value = items[0]['value']
            self.hint = cm.widget.backend.hint
            self.persistent_hint = True
        
        # default values 
        self.label = cm.widget.backend.label
        self.v_model = value
        self.items = items
        self.class_ = 'mb-4'
        
        # create the widget
        super().__init__(**kwargs)
    
    @staticmethod
    def is_gpu():
        """return if the current AWS instance is a GPU machine"""
        
        # the 3 folders we are looking for: 
        dev_dir = Path('/dev')
        dev_content = [el for el in dev_dir.glob('*')]
        files = [dev_dir/'nvidia-uvm', dev_dir/'nvidia0', dev_dir/'nvidiactl']
        
        return all(f in dev_content for f in files)
        
        
        
        
        