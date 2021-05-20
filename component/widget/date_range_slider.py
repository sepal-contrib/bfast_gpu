from datetime import timedelta

from sepal_ui import sepalwidgets as sw 
import ipyvuetify as v
import pandas as pd

from component import parameter as cp

class DateRangeSlider(sw.SepalWidget, v.Layout):
    
    def __init__(self, dates=None, **kwargs):
        
        # display the dates in a text filed in a the prepend slot 
        self.display = v.Html(tag="span", children = [''])
        
        # create a range widget with the default params 
        self.slider = v.RangeSlider(class_="pl-5 pr-1 mt-1")
        
        # add the non conventional parameters for customization
        for k, val in kwargs.items():
            if hasattr(self.slider, k):
                setattr(self.slider, k, val)
            
        # wrap everything in a layout
        super().__init__(
            row=True,
            v_model = None,
            xs12=True,
            children=[
                v.Flex(xs10=True, children=[self.slider]), 
                v.Flex(xs2=True, children=[self.display])
            ]
        )
        
        # link the v_models
        self.slider.observe(self._on_change, 'v_model') 
        
        # add the dates if existing
        if dates != None:
            self.set_dates(dates)
        else:
            self.disable()
            
    def _on_change(self, change):
        
        # to avoid bugs on disable
        if not self.dates:
            return self
        
        # get the real dates from the list
        dates = [self.dates[int(c)] for c in change['new']]
        self.v_model = dates
        
        # update what is display to the user 
        txt = [d.strftime("%b-%Y") for d in dates]
        self.display.children = [' - '.join(txt)]
        
        return self
    
    def disable(self):
        """disabled the widget and reset its value"""
        
        self.dates = None
        self.v_model = None
        self.slider.v_model = [0, 1]
        self.slider.max = 1
        self.slider.disabled = True
        self.display.children = ['']
        self.slider.ticks = False
        
        return self
    
    def set_dates(self, dates):
        """set the dates and activate the widget"""  
        
        # set datemin and datemax to their min and max 
        datemin = dates[0].replace(day=1)
        datemax = (dates[-1].replace(day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        # save the dates 
        self.dates = pd.date_range(datemin, datemax, freq='MS').to_pydatetime().tolist()
        
        # get the first usable date index
        min_ = min(cp.min_images, len(dates)/2)
        
        min_date = dates[min_]
        index = next(d[0] for d in enumerate(self.dates) if d[1] > min_date)
        
        # set the slider 
        self.slider.max = len(self.dates)-1
        self.slider.v_model = [index, len(self.dates)-1]
        
        # set the ticks of the slider 
        self.slider.tick_labels = [str(d.year) if d.month == 1 and d.year % 5 == 0 else '' for d in self.dates]
        self.slider.disabled = False
        
        return self