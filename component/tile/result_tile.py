from pathlib import Path

from sepal_ui import sepalwidgets as sw
from sepal_ui import mapping as sm
from sepal_ui.scripts.utils import loading_button
import ipyvuetify as v
import numpy as np
from matplotlib.colors import ListedColormap
from traitlets import Any
import rasterio as rio

from component import parameter as cp
from component.message import cm


class ResultTile(sw.Tile):

    out_dir = Any(None).tag(sync=True)

    def __init__(self, bfast_tile):

        # create the map
        self.m = sm.SepalMap()
        self.m.add_legend(
            legend_title=cm.display.legend,
            legend_dict={k: c for k, c in cp.legend.values()},
            position="topleft",
        )

        super().__init__(
            "result_tile",
            cm.display.title,
            inputs=[v.Flex(class_="mt-5 mb-5", children=[self.m])],
            btn=sw.Btn(cm.display.btn),
            alert=sw.Alert(),
        )

        # js events
        bfast_tile.observe(self._change_dir, "dir_")
        self.btn.on_event("click", self._compute_map)

    def _change_dir(self, change):

        self.out_dir = change["new"]

        return self

    @loading_button(debug=True)
    def _compute_map(self, widget, event, data):
        """compute the threshold data map and display it on the interactive map"""

        if not self.out_dir:
            raise Exception(cm.display.no_bfast)

        # check if the bfast_output vrt exist
        out_dir = Path(self.out_dir)
        bfast_output = out_dir / f"bfast_outputs_{out_dir.parent.stem}.vrt"

        if not bfast_output.is_file():
            raise Exception(cm.display.no_bfast)

        # check if the threshold map exist
        threshold_output = bfast_output.parent / f"threshold_{out_dir.parent.stem}.tif"
        if not threshold_output.is_dir():

            with rio.open(bfast_output, GEOREF_SOURCES="INTERNAL") as src:

                # get the profile
                profile = src.profile.copy()
                profile.update(driver="GTiff", count=1, dtype=np.int8)

                data = src.read(2).astype(np.int16)

                std = data.flatten().std()
                mean = data.flatten().mean()

                final_data = (
                    (data > (mean + (std * 4))) * 9
                    + (data <= (mean + (std * 4))) * (data > (mean + (std * 3))) * 8
                    + (data <= (mean + (std * 3))) * (data > (mean + (std * 2))) * 7
                    + (data <= (mean + (std * 2))) * (data > (mean + std)) * 6
                    + (data <= (mean + std)) * (data > 0) * 1
                    + (data < 0) * (data > (mean - std)) * 1
                    + (data <= (mean - std)) * (data > (mean - (std * 2))) * 2
                    + (data <= (mean - (std * 2))) * (data > (mean - (std * 3))) * 3
                    + (data <= (mean - (std * 3))) * (data > (mean - (std * 4))) * 4
                    + (data <= (mean - (std * 4))) * 5
                )

                with rio.open(threshold_output, "w", **profile) as dst:
                    dst.write(final_data.astype(np.int8), 1)

        # display it in the interactive map
        self.m.add_raster(
            threshold_output,
            layer_name=cm.display.layer,
            colormap=ListedColormap([cp.legend[i][1] for i in sorted(cp.legend)]),
            colorbar_position=False,
        )

        return self
