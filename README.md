# BFAST GPU  
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)  
[![Black badge](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
  
## About  
  
This dasboard application based on the [sepal-ui](https://sepal-ui.readthedocs.io/en/latest/) framework, provide the user with a friendly interface to use the [GPU implementation](https://github.com/diku-dk/bfast) of the bfast algorithm.

The bfast package provides an efficient massively-parallel implementation for one of the state-of-the-art change detection methods called [Breaks For Additive Season and Trend (BFASTmonitor)](http://bfast.r-forge.r-project.org) proposed by Verbesselt et al.

![demo](https://raw.githubusercontent.com/12rambau/bfast_gpu/master/utils/full_app.gif)

## Output

The scripts provide the following tvrt outputs:
- ~/module_results/bfast/[name_of_input]/[bfast_params]/bfast_outputs.vrt

It is a 2 band raster with band 1 being the breakpoints in decimal year format and on band 2, the magnitude of change. This raster has the exact same dimension as the input raster

## Example

Here you'll find an example of this 2 bands over the Juaboso Region in Ghana whit a monitoring period between 2017 and 2019:

| ![breaks](https://raw.githubusercontent.com/12rambau/bfast_gpu/master/utils/magnitude.png) | ![breaks](https://raw.githubusercontent.com/12rambau/bfast_gpu/master/utils/breaks.png)                    |
|--------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------|
| Magnitude display with the magma colormap, values in [-624, 417]                           | Breaks masked in the center of the region. displayed with a viridis colormap, values in [2017.26, 2019.98] |
    
## Contribute

first download the repository to your own sepal account 

```
git clone https://github.com/12rambau/bfast_gpu.git
```

Then in the `bfast_gpu` folder, launch the `ui.ipynb` notebook and run it with voila.

> :warning: If for some reason the sepal_ui module doesn't work on your instance, you can run the `no_ui.ipynb` file as a notebook using `kernel->run all`
