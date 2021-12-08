from datetime import timedelta

from sepal_ui import sepalwidgets as sw
import ipyvuetify as v
import pandas as pd


class DateSlider(sw.SepalWidget, v.Layout):
    def __init__(self, dates=None, **kwargs):

        # display the dates in a text filed in a the prepend slot
        self.display = v.Html(tag="span", children=[""])

        # create a range widget with the default params
        self.slider = v.Slider(class_="pl-5 pr-1 mt-1")

        # add the non conventional parameters for customization
        for k, val in kwargs.items():
            if hasattr(self.slider, k):
                setattr(self.slider, k, val)

        # wrap everything in a layout
        super().__init__(
            row=True,
            v_model=None,
            xs12=True,
            children=[
                v.Flex(xs10=True, children=[self.slider]),
                v.Flex(xs2=True, children=[self.display]),
            ],
        )

        # link the v_models
        self.slider.observe(self._on_change, "v_model")

        # add the real dates if existing
        if dates:
            self.set_dates(dates)
        else:
            self.disable()

    def _on_change(self, change):

        # to avoid bugs on disable
        if not self.dates:
            return self

        # get the real dates from the list
        date = self.dates[int(change["new"])]
        self.v_model = date

        # update what is display to the user
        self.display.children = [date.strftime("%b-%Y")]

        return self

    def disable(self):
        """disable the widget and reset it's values"""

        self.dates = None
        self.v_model = None
        self.slider.v_model = 1
        self.slider.max = 1
        self.slider.disabled = True
        self.display.children = [""]
        self.slider.ticks = False

        return self

    def set_dates(self, dates):
        """set the dates of the widget"""

        # set datemin and datemax to their min and max
        datemin = dates[0].replace(day=1)
        datemax = (dates[-1].replace(day=1) + timedelta(days=32)).replace(
            day=1
        ) - timedelta(days=1)

        # save the dates
        self.dates = pd.date_range(datemin, datemax, freq="MS").to_pydatetime().tolist()

        # set the slider
        self.slider.max = len(self.dates) - 1
        self.slider.v_model = 0

        # activate the slider
        self.slider.tick_labels = [
            str(d.year) if d.month == 1 and d.year % 5 == 0 else "" for d in self.dates
        ]
        self.slider.disabled = False

        return self
