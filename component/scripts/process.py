import threading
from concurrent import futures
from datetime import datetime
from functools import partial

import rasterio as rio
import numpy as np
from bfast import BFASTMonitor
from bfast.monitor.utils import crop_data_dates
from tqdm import tqdm

from component import parameter as cp
from component.message import cm

def break_to_decimal_year(idx, dates):
    """
    break dates of change into decimal year
    build to be vectorized over the resulting bfast break events
    using the following format 
    """
    
    # everything could have been done in a lambda function but for the sake of clarity I prefer to use it 
    if idx < 0:
        return np.nan
    else:
        break_date = dates[idx-1]
        return break_date.year + (break_date.timetuple().tm_yday - 1)/365

def bfast_window(window, read_lock, write_lock, src, dst, segment_dir, monitor_params, crop_params):
    """TODO"""
    
    # read in a read_lock to avoid duplicate reading and corruption of the data
    with read_lock:
        data = src.read(window=window).astype(np.int16)
        # all the nan are transformed into 0 by casting don't we want to use np.iinfo.minint16 ? 
    
    # read the local observation date
    with (segment_dir/'dates.csv').open() as f:
        dates = [datetime.strptime(l, "%Y-%m-%d") for l in f.read().splitlines() if l.rstrip()]
        
    # crop the initial data to the used dates
    data, dates = crop_data_dates(data,  dates, **crop_params)
    
    # start the bfast process
    model = BFASTMonitor(**monitor_params)
    
    # fit the model 
    model.fit(data, dates)

    # vectorized fonction to format the results as decimal year (e.g mid 2015 will be 2015.5)
    to_decimal = np.vectorize(break_to_decimal_year, excluded=[1])
    
    # slice the date to narrow it to the monitoring dates
    start = monitor_params['start_monitor']
    end = crop_params['end']
    monitoring_dates = dates[dates.index(start):dates.index(end)+1] # carreful slicing is x in [i,j[    
    
    # compute the decimal break on the model 
    decimal_breaks = to_decimal(model.breaks, monitoring_dates)
    
    # agregate the results on 2 bands
    monitoring_results = np.stack((decimal_breaks, model.magnitudes)).astype(np.float32)
    
    with write_lock:
        dst.write(monitoring_results, window=window)
    
    return
        
def run_bfast(folder, out_dir, tiles, monitoring, history, freq, k, hfrac, trend, level, backend, output):
    """run the bfast programm using the user parameters and pilot the differnt threads that will be used"""
    
    # prepare parameters for crop as a dict 
    crop_params = {
        'start': datetime.strptime(history, '%Y-%m-%d'),
        'end': datetime.strptime(monitoring[1], '%Y-%m-%d')
    }
        
    # prepare parameters for the bfastmonitor function 
    monitor_params = {
        'start_monitor': datetime.strptime(monitoring[0], '%Y-%m-%d'),
        'freq': freq,
        'k': k,
        'hfrac': hfrac,
        'trend': trend,
        'level': 1-level,  # it's an hidden parameter I hate it https://github.com/diku-dk/bfast/issues/23
        'backend': backend
    }
    
    # loop through the tiles 
    for tile in tiles:
        
        # get the segment useful folders 
        segment_dir = folder/tile
        save_dir = cp.result_dir/out_dir/tile
        save_dir.mkdir(parents=True, exist_ok=True)
        
        # create the locks to avoid data coruption
        read_lock = threading.Lock()
        write_lock = threading.Lock()

        # get the profile from the master vrt
        with rio.open(segment_dir/'stack.vrt', GEOREF_SOURCES='INTERNAL') as src:
            
            profile = src.profile.copy()
            profile.update(
                driver = 'GTiff',
                count = 2,
                dtype = np.float32
            )
        
            # display an tile computation message
            count = sum(1 for _ in src.block_windows())
            output.add_live_msg(cm.bfast.sum_up.format(count, tile))
        
            # get the windows
            windows = [w for _, w in src.block_windows()]
            
            # execute the concurent threads and write the results in a dst file 
            with rio.open(save_dir/'bfast_outputs.tif', 'w', **profile) as dst:
                
                bfast_params = {
                    'read_lock': read_lock, 
                    'write_lock': write_lock,
                    'src': src,
                    'dst': dst,
                    'segment_dir': segment_dir, 
                    'monitor_params': monitor_params, 
                    'crop_params': crop_params
                }
                
                with tqdm(total=(count)) as progress_bar:
                    with futures.ThreadPoolExecutor(max_workers=4) as executor:
                        executor.map(partial(bfast_window, **bfast_params), windows)
                #bfast_window(windows[0], **bfast_params)
                        
    return 
        
        