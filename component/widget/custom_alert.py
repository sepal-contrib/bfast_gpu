from sepal_ui import sepalwidgets as sw 

class CustomAlert(sw.Alert):
    """
    An alert design to be compatible with multithreading
    Only addition being the possiblity to increase the rogress bar from multiple threads
    """
    
    def __init__(self, **kwargs):
        
        # the variable used to save the progress
        self.progress_count = 0
        
        super().__init__(**kwargs)
        
    def update_progress(self, total, msg):
        
        # increase the counte value 
        self.progress_count += 1
    
        # compute the progress
        progress = self.progress_count / total
        
        # display it in the alert 
        super().update_progress(progress, msg)
        
        return self
    
    def reset_progress(self):
        """remove the progress value"""
        
        # reset the counter
        self.progress_count = 0 
        
        # remove the message
        self.add_msg('')
        
        return self
        