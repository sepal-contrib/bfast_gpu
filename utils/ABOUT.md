This dasboard application based on the [sepal-ui](https://sepal-ui.readthedocs.io/en/latest/) framework, provide the user with a friendly interface to use the [GPU implementation](https://github.com/diku-dk/bfast) of the bfast algorithm.

The bfast package provides an efficient massively-parallel implementation for one of the state-of-the-art change detection methods called [Breaks For Additive Season and Trend (BFASTmonitor)](http://bfast.r-forge.r-project.org) proposed by Verbesselt et al.

## Output

The scripts provide the following tvrt outputs:
- `~/module_results/bfast/[name_of_input]/[bfast_params]/bfast_outputs.vr`

It is a 2 band raster with band 1 being the breakpoints in decimal year format and on band 2, the magnitude of change. This raster has the exact same dimension as the input raster.

## Example

Here you'll find an example of the first band over the Juaboso Region in Ghana whit a monitoring period between 2017 and 2019. The magnitude is displayed with the magma colormap, values in [-624, 417]:

![breaks](https://raw.githubusercontent.com/12rambau/bfast_gpu/master/utils/magnitude.png)