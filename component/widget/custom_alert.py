from sepal_ui import sepalwidgets as sw 

class CustomAlert(sw.Alert):
    """
    An alert design to be compatible with multithreading
    Only addition being the possiblity to increase the rogress bar from multiple threads
    """
    
    def __init__(self, **kwargs):
        
        # the variables used to save the progress
        self.progress_count = 0
        self.progress_total = 0
        self.progress_msg = None
        
        super().__init__(**kwargs)
        
    def update_progress(self):
        
        # increase the counte value 
        self.progress_count += 1
    
        # compute the progress
        progress = self.progress_count / self.progress_total
        
        # display it in the alert 
        super().update_progress(progress, self.progress_msg)
        
        return self
    
    def reset_progress(self, total, msg):
        """remove the progress value"""
        
        # reset the counter
        self.progress_count = 0 
        
        # set the new total
        self.progress_total = total
        
        # set the new message 
        self.progress_msg = msg 
        
        # remove the message
        self.add_msg('')
        
        super().update_progress(0, self.progress_msg)
        
        return self
        