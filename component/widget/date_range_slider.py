from sepal_ui import sepalwidgets as sw 
import ipyvuetify as v

class DateRangeSlider(sw.SepalWidget, v.Flex):
    
    def __init__(self, dates=None, **kwargs):
        
        # save the dates values 
        self.dates = dates
        
        # display the dates in a text filed in a the prepend slot 
        self.display = v.Html(tag="span", children = [""])
        
        # create a range widget with the default params 
        self.range = v.RangeSlider(
            disabled = True,
            v_model = [0, 1],
            max=1,
            class_="ml-5 mr-5 mt-1",
            v_slots = [{
                'name': 'append',
                'children': [self.display]
            }]
        )
        
        # add the non conventional parameters for customization
        for k, val in kwargs.items():
            if hasattr(self.range, k):
                setattr(self.range, k, val)
        
        # wrap everything in a layout
        super().__init__(
            v_model = None,
            xs12=True,
            children=[self.range]
        )
        
        # link the v_models
        self.range.observe(self._on_change, 'v_model') 
        
        # add the dates if existing
        if dates:
            self.set_dates(dates)
        
    def _on_change(self, change):
        """update the display and v_model when the slider changes"""
        
        # to avoid bugs on disable
        if not self.dates:
            return self
        
        # get the real dates from the list
        start, end = [self.dates[int(i)] for i in change['new']]
        self.v_model = [start, end]
        
        # update what is display to the user 
        self.display.children = [f"{start} to {end}"]
        
        return self
    
    def disable(self):
        """disabled the widget and reset its value"""
        
        self.dates = None
        self.v_model = None
        self.range.v_model = [0, 1]
        self.range.max = 1
        self.range.disabled = True
        self.display.children = ['']
        
        return self
    
    def set_dates(self, dates):
        """set the dates and activate the widget"""
        
        # save the dates 
        self.dates = dates
        
        # set the slider 
        self.range.max = len(dates)-1
        self.range.v_model = [0, self.range.max]
        # display and self.v_model are automatically updated
        
        # activate the slider 
        self.range.disabled = False
        
        return self