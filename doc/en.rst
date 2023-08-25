BFAST GPU
=========

This document provides usage instructions for the GPU implementation of BFAST, implemented here as a Jupyter dashboard on SEPAL.

Introduction
------------

Large amounts of satellite data are now becoming available, which, in combination with appropriate change detection methods, offer the opportunity to derive accurate information on timing and location of disturbances (e.g. deforestation events across the Earth's surface). Typical scenarios require the analysis of billions of image patches/pixels, which can become very expensive from a computational point of view. The `BFAST package <https://pypi.org/project/bfast/>`_ provides efficient, massively parallel implementation for one of the state-of-the-art change detection methods called `Breaks For Additive Season and Trend (BFASTmonitor) <http://bfast.r-forge.r-project.org>`, as proposed by Verbesselt *et al.*

.. figure:: https://raw.githubusercontent.com/12rambau/bfast_gpu/master/doc/img/bfastmonitor_1.png

    The analysis perfomed pixel-wise

The implementation is based on `OpenCL <https://www.khronos.org/opencl/>`_. It allows the processing of large-scale change detection scenarios given satellite time-series data. The optimizations made are tailored to the specific requirements of modern, massively parallel devices, such as graphics processing units (GPUs). 

The full documentation of the :code:`bfast` package can be found `on this page <https://bfast.readthedocs.io/en/latest/>`_.

Usage
-----

.. important::

    Before launching the BFAST module, you need to have at least one time series in your SEPAL folders.
    
.. attention:: 

    If, while using the app, a user comes across an error starting with "Unable to allocate ...", it means that the instance used to run the application is too small. You'll need to start a larger instance and restart the application.

Set up
^^^^^^

To launch the app, follow the `steps to register for SEPAL <https://docs.sepal.io/en/latest/setup/register.html>`_. 

Open a GPU instance in your terminal (:code:`g4` or :code:`g8`). Then move to the SEPAL **Apps** dashboard (purple wrench icon on the left side panel). Finally, search for and select **bfast GPU**. 

The application should launch itself in the **BFAST process** section. On the left side, the **navdrawer** will help you navigate between the different pages of the app. If you click on :code:`wiki`, :code:`bug report` or :code:`code source`, you will be redirected to the corresponding webpage.

.. note::

    The launching process can take several minutes.
    
.. figure:: https://raw.githubusercontent.com/12rambau/bfast_gpu/master/doc/img/full_app.png
    
    The landing page of bfast GPU
    
Select folder
^^^^^^^^^^^^^

Select a folder in the first widget. Navigate through your folders to find the time series folder you want to analyse. Click outside the pop-up window to exit the selection. Your folder should only contain folders with numbered names (corresponding to each tile of the TS). 

By selecting an appropriate folder, a widget will be automatically filled out and enabled, as described below: 

-   :code:`output directory name`: Filled out with the basename of your TS folder.
-   :code:`select tiles to use`: Preselect all of the available tiles.
-   :code:`monitoring dates`: The slider is enabled and filled with the date list included in the TS folder. The values default to the full range of dates.
-   :code:`historical period`: The slider is enabled and filled with the date list included in the TS folder. The value defaults to the first date of the TS.

.. figure:: https://raw.githubusercontent.com/12rambau/bfast_gpu/master/doc/img/correct_folder.png

    Select a folder and preload all of the information.
    
.. attention:: 

    If your selected folder does not meet the requirements of a SEPAL TS folder, the prefilled inputs will be emptied and disabled, and you will be notified twice that the folder is not set (in the input and in the warning banner). Select an appropriate folder to see these messages disappear.
    
    .. figure:: https://raw.githubusercontent.com/12rambau/bfast_gpu/master/doc/img/wrong_folder.png
    
        The error messages if incorrect folders are provided

Parameters
^^^^^^^^^^

Now you can change the parameters to fit the requirements of your analysis:

-   :code:`output directory name`: This name will be used to store all of your analysis. While it is completed automatically with the base name of your TS folder, you can still change it. 
    
    .. note:: 
    
        The name of your folder can only contain alphanumeric characters and no special characters (e.g. :code:`space`). If you try to use them, the name will be automatically sanitized.
        
-   :code:`Select tiles to use`: These are the tiles that you want to use in your analysis. They default to :code:`all` but you can deselect any that you don't need.
-   :code:`Number of harmonic`: Specifies the order of the harmonic term, defaulting to 3.
-   :code:`Frequency of seasonal model`: The frequency for the seasonal model, set here in months.
-   :code:`Add trend`: Whether a trend offset term shall be used or not.
-   :code:`Monitoring dates`: The year that marks the end of the historical period and the start of the monitoring period. The default value does not allow sufficient images in the historical stable period.

    .. attention::
    
        If you allow less than 40 images between the start of the historical stable period and the start of monitoring, the programme will display a warning. You will still be able to launch the process, but the result will be very uncertain, as not enough images were provided to build an accurate model. 
        
        .. figure:: https://raw.githubusercontent.com/12rambau/bfast_gpu/master/doc/img/too_short.png
        
-   :code:`History start date`: Specifies the start of the stable historical period

Advanced parameters
^^^^^^^^^^^^^^^^^^^

.. tip:: 

    These parameters are for advanced users only. The default value provides accurate results in many situations.
    
Select :code:`Advanced parameters` and a new panel of options will be available:

-   :code:`bandwith relative to sample size`: Float in the interval (0,1), specifying the bandwidth relative to the sample size in the MOSUM/ME monitoring processes.
-   :code:`Significance level of the monitoring`: Significance level of the monitoring procedure (and ROC, if selected), i.e. probability of Type I error.
-   :code:`backend`: Specifies the implementation that shall be used: **Python** resorts to the non-optimized Python version; **OpenCL** resorts to the optimized, massively parallel OpenCL implementation.

    .. note::
    
        If you didn't initiate a GPU instance before starting the application, the **OpenCL** backend will be disabled, as no GPU is available on your machine. Please close the app and your previous instance, and start a :code:`g4` or :code:`g8`. If you run the application on a GPU machine, the default backend is **OpenCL**.
        
.. figure:: https://raw.githubusercontent.com/12rambau/bfast_gpu/master/doc/img/advance_params.png

    Advanced parameters list

Run process
^^^^^^^^^^^

You can now select :code:`LAUNCH BFAST ANALYSIS` to start the process. 

The process will start shortly, notifying you of it's advancement tile by tile in the info banner, as shown in the following figure. 

.. figure:: https://raw.githubusercontent.com/12rambau/bfast_gpu/master/doc/img/advancement.png

    Process currently runnning
    
.. attention:: 

    Closing the app will shut down the Python kernel that runs underneath, thus stopping your process. In it's current implementation, the app should stay open to run.
    
.. tip::

    If your connection to SEPAL is lost and the application stops, use the exact same parameters as your previous analysis. The application will find the already computed tiles and images, and start from where it stopped instead of restarting from scratch.
    
    
.. figure:: https://raw.githubusercontent.com/12rambau/bfast_gpu/master/doc/img/computation_end.png

    End of computation screen
    

The module provided the following :code:`.vrt` outputs:
-   :code:`~/module_results/bfast/[name_of_input]/[bfast_params]/bfast_outputs.vrt`

It is a three-band raster:

-   band 1, the breakpoints in decimal year format
-   band 2, the magnitude of change
-   band 3, the validity of the pixel model

This raster has the exact same dimensions as the input raster.

Example
^^^^^^^

Here you'll find an example of two bands over the Juaboso Region in Ghana with a monitoring period between 2017 and 2019:

.. figure:: https://raw.githubusercontent.com/12rambau/bfast_gpu/master/utils/magnitude.png

    Magnitude display with the magma colormap, values in [-624, 417]
    
.. figure:: https://raw.githubusercontent.com/12rambau/bfast_gpu/master/utils/breaks.png

    Breaks masked in the center of the region, displayed with a viridis colormap, values in [2017.26, 2019.98]
    
.. custom-edit:: https://raw.githubusercontent.com/sepal-contrib/bfast_gpu/release/doc/en.rst
