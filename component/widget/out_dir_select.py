from pathlib import Path
import re

import ipyvuetify as v
from sepal_ui import sepalwidgets as sw

from component.message import cm


class OutDirSelect(sw.SepalWidget, v.TextField):
    def __init__(self, **kwargs):

        # default parameters
        self.v_model = None
        self.label = cm.widget.out_dir.label
        self.hint = cm.widget.out_dir.hint
        self.class_ = "mb-2"

        # create the widget
        super().__init__(**kwargs)

        # add a behaviour on modifications
        self.on_event("blur", self._sanitize)

    def set_folder(self, path):
        """use the path of the time_series to name the folder that is used to store the information"""

        # unsure it's a path
        path = Path(path)

        # change the v_model
        self.v_model = path.stem

        return self

    def _sanitize(self, widget, event, data):
        """if the user decide to change the folder name it need to be sanitized to be used"""

        val = re.sub("[^a-zA-Z\d\-\_]", "_", self.v_model)
        self.v_model = val

        return self
