BFAST GPU
=========

This document provides usage instructions for the GPU implementation of BFAST, here implemented as a Jupyter dashboard on SEPAL.

Introduction 
------------

Large amounts of satellite data are now becoming available, which, in combination with appropriate change detection methods, offer the opportunity to derive accurate information on timing and location of disturbances such as deforestation events across the earth surface. Typical scenarios require the analysis of billions of image patches/pixels, which can become very expensive from a computational point of view. The `bfast package <https://pypi.org/project/bfast/>`_ provides an efficient massively-parallel implementation for one of the state-of-the-art change detection methods called `Breaks For Additive Season and Trend (BFASTmonito) <http://bfast.r-forge.r-project.org>` proposed by Verbesselt et al.

.. figure:: https://raw.githubusercontent.com/12rambau/bfast_gpu/master/doc/img/bfastmonitor_1.png

    the analysis perfomed pixel wise

The implementation is based on `OpenCL <https://www.khronos.org/opencl/>`_ and allows to process large-scale change detection scenarios given satellite time series data. The optimizations made are tailored to the specific requirements of modern massively-parallel devices such as graphics processing units (GPUs). The full documentation of the :code:`bfast` package can be found `here <https://bfast.readthedocs.io/en/latest/>`_.

Usage
-----

.. warning::

    **prerequist**: before launching the bfast module, you need to have at least 1 time series in SEPAL folders

Set up
^^^^^^

To launch the app please follow the `SEPAL registration steps <https://docs.sepal.io/en/latest/setup/register.html>`_. Then open a GPU instance in your terminal (:code:`g4`or :code:`g8`). Then move to the SEPAL Apps dashboard (purple wrench icon on the left side panel), search for and click on **bfast GPU**. 

The application should launch itself in the **BFAST process** section. On the left side the navdrawer will help you navigate between the different pages of the app. If you click on :code:`wiki`, :code:`bug report` or :code:`code source`, you will be redirected to the corresponding webpage. 

.. note::

    The launching process can take several minutes
    
.. figure:: https://raw.githubusercontent.com/12rambau/bfast_gpu/master/doc/img/full_app.png
    
    The landing page of bfast GPU
    
Select folder 
^^^^^^^^^^^^^

Select a folder in using the first widget. Navigate in your folders to find the time series foder you want to analyse. click outside the popup to exit the selection. Your folder should only contain folders with numbered name (corresponding to each tile of the TS). 

By selecting an appropriate folder some widget will be automatically filled and unable: 

-   :code:`output directory name`: filled with the basename of your TS folder
-   :code:`select tiles to use`: preselect all the available tiles
-   :code:`monitoring dates`: the slider is unabled and filled with the date list included in the TS folder. The values are defaulted to the full range of dates.
-   :code:`historical period`: The slider is unabled and filled with the date list included in the TS folder. The value is defaulted to the first date of the TS.

.. figure:: https://raw.githubusercontent.com/12rambau/bfast_gpu/master/doc/img/correct_folder.png

    Select a folder and preload all the informations
    
.. warning:: 

    If your selected folder does not meet the requirements of a SEPAL TS folder, the prefilled inputs will be emptied and disabled and you will be notified in 2 spots (in the input and in the warning banner) that the folder is not set. Change to an appropriate foldeer to see these messages disapear.
    
    .. figure:: https://raw.githubusercontent.com/12rambau/bfast_gpu/master/doc/img/wrong_folder.png
    
        The error messages if a wrong folder is provided

Parameters
^^^^^^^^^^

Now you can change the parameters to fit the requirements of your analysis:

-   :code:`output directory name`: this name will be used to store all your analysis. It is automatically filled with the basename of your TS folder but you can still change it. 
    
    .. note:: 
    
        The name of your folder can only contain alphanumeric characters and no special characters (like :code:`space`). If you try to use them the name will be sanitized automatically.
        
-   :code:`select tiles to use`: This is the tiles that you want to use in your analysis. they default to :code:`all` but you can deselect the one that you don't need.
-   :code:`number of harmonic`: Specifies the order of the harmonic term, defaulting to 3.
-   :code:`frequency of seasonal model`: The frequency for the seasonal model.
-   :code:`add trend`: Whether a trend offset term shall be used or not
-   :code:`Monitoring dates`: The year that marks the end of the historical period and the start of the monitoring period. The default value does not let enough images in the historical stable perdiod

    .. danger::
    
        If you let less than 40 images between the start of the historical stable period and the start of the monitoring, the program will send you a warning. You will still be able to launch the process but the result will be very uncertain has not enough image were provided to build an accurate model. 
        
        .. figure:: https://raw.githubusercontent.com/12rambau/bfast_gpu/master/doc/img/too_short.png
        
-   :code:`History start date`: Specifies the start of the stable history period

Advanced parameter
^^^^^^^^^^^^^^^^^^

.. tip:: 

    this parameters are for advanced user only, the default value our team set for you already give accurate results in many situation
    
Click on :code:`advanced parameter` and a new panel of options will be available:

-   :code:`bandwith relative to sample size`: Float in the interval (0,1) specifying the bandwidth relative to the sample size in the MOSUM/ME monitoring processes.
-   :code:`Significance level of the monitoring`: Significance level of the monitoring (and ROC, if selected) procedure, i.e., probability of type I error.
-   :code:`backend`: Specifies the implementation that shall be used: **Python** resorts to the non-optimized Python version; **OpenCL** resorts to the optimized massively-parallel OpenCL implementation.

    .. note::
    
        If before starting the application you didn't start a GPU instance, the **OpenCL** backend will be disabled as no GPU are available on your machine. Please close the app and your previous instance and start a :code:`g4` or :code:`g8`. If you run the application on a GPU machine the default backend is **OpenCL**.
        
.. figure:: https://raw.githubusercontent.com/12rambau/bfast_gpu/master/doc/img/advance_params.png

    advanced parameters list

Run process
^^^^^^^^^^^

You can now click on :code:`LAUNCH BFAST ANALYSIS` to start the process. 

The process wil start shortly notifying you of it's advancment tile by tyle in the info banner as shown on the following image. 

.. figure:: https://raw.githubusercontent.com/12rambau/bfast_gpu/master/doc/img/advancement.png

    process currently runnning
    
.. danger:: 

    Closing the app will shut down the Python kernel that runs underneath and thus stop your process. In it's current implementation the app should stay open to run
    
.. tip::

    If your connection to SEPAL is lost and the application stop, use the exact same parameters as in your previous analysis, the application will find back the already computed tiles and images and will start from where it stops instead of restarting from scratch
    
    
.. figure:: https://raw.githubusercontent.com/12rambau/bfast_gpu/master/doc/img/computation_end.png

    End of computation screen
    

The module provide the following :code:`.vrt` outputs:
-   :code:`~/module_results/bfast/[name_of_input]/[bfast_params]/bfast_outputs.vrt`

It is a 2 band raster with band 1 being the breakpoints in decimal year format and on band 2, the magnitude of change. This raster has the exact same dimension as the input raste`

Example
^^^^^^^

Here you'll find an example of this 2 bands over the Juaboso Region in Ghana whit a monitoring period between 2017 and 2019:

.. figure:: https://raw.githubusercontent.com/12rambau/bfast_gpu/master/utils/magnitude.png

    Magnitude display with the magma colormap, values in [-624, 417]
    
.. figure:: https://raw.githubusercontent.com/12rambau/bfast_gpu/master/utils/breaks.png

    Breaks masked in the center of the region. displayed with a viridis colormap, values in [2017.26, 2019.98]
    

    



    

    

    

    
 
