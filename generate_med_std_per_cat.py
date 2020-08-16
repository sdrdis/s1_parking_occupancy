import tifffile
import numpy as np
import pandas as pd
from os.path import join, isdir
import matplotlib.pyplot as plt
import scipy.stats
import os
from datetime import datetime

data_folder = 'data'

for subfolder in os.listdir(data_folder):
    for dirname in os.listdir(join(data_folder, subfolder)):
        dirpath = join(data_folder, subfolder, dirname)
        ims_path = join(dirpath, 'images')
        precomputed_path = join(dirpath, 'precomputed')
        if (not isdir(precomputed_path)):
            os.makedirs(precomputed_path)
            
        ims_per_cat = {}
        for filename in os.listdir(ims_path):
            cat = '_'.join(filename[:-4].split('_')[2:])
            if (cat not in ims_per_cat):
                ims_per_cat[cat] = []
                
            filename_dt = datetime.strptime('_'.join(filename.split('_')[:2]), "%Y%m%d_%H%M%S")
            if (filename_dt.weekday() != 6):
                continue
            filepath = join(ims_path, filename)
            
            ims_per_cat[cat].append(tifffile.imread(filepath))
            
        for cat in ims_per_cat:
            ims = np.array(ims_per_cat[cat])

            print (ims.shape)

            median_np = np.median(ims, axis=0)
            std_np = np.std(ims, axis=0)
            if (len(median_np.shape) > 1):
                tifffile.imsave(join(precomputed_path, 'median_'+cat+'.tif'), median_np[:,:,[0,0,0]])
                tifffile.imsave(join(precomputed_path, 'std_'+cat+'.tif'), std_np[:,:,[0,0,0]])
        #sys.exit()