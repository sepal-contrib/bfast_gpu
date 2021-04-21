from sepal_ui import sepalwidgets as sw 
import ipyvuetify as v

class DateSlider(sw.SepalWidget, v.Flex):
    
    def __init__(self, dates=None, **kwargs):
        
        # save the dates values 
        self.dates = dates
        
        # display the dates in a text filed in a the prepend slot 
        self.display = v.Html(tag="span", children = [''])
        
        # create a range widget with the default params 
        self.slider = v.Slider(
            disabled=True,
            v_model = 0,
            max= 1,
            class_="ml-5 mr-5 mt-1",
            v_slots = [{
                'name': 'append',
                'children': [self.display]
            }]
        )
        
        # add the non conventional parameters for customization
        for k, val in kwargs.items():
            if hasattr(self.slider, k):
                setattr(self.slider, k, val)
            
        # wrap everything in a layout
        super().__init__(
            v_model = None,
            xs12=True,
            children=[self.slider]
        )
        
        # link the v_models
        self.slider.observe(self._on_change, 'v_model') 
        
        # add the real dates if existing 
        if dates:
            self.set_dates(dates)
        
    def _on_change(self, change):
        
        # to avoid bugs on disable
        if not self.dates:
            return self
        
        # get the real dates from the list
        date = self.dates[int(change['new'])]
        self.v_model = date
        
        # update what is display to the user 
        self.display.children = [date]
        
        return self
         
    def disable(self):
        """disable the widget and reset it's values"""
        
        self.dates = None
        self.v_model = None
        self.slider.v_model = 0
        self.slider.max = 1
        self.slider.disabled = True
        self.display.children = ['']
        
        return self
    
    def set_dates(self, dates):
        """set the dates of the widget"""
        
        # save the dates 
        self.dates = dates
        
        # set the slider 
        self.slider.max = len(dates)-1
        self.slider.v_model = 0
        
        # activate the slider 
        self.slider.disabled = False
        
        return self
        
        
        