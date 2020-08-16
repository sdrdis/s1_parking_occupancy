import tifffile
import numpy as np
import pandas as pd
from os.path import join, isdir, splitext
import matplotlib.pyplot as plt
import scipy.stats
import os
from datetime import datetime
import argparse
import common
    

parser = argparse.ArgumentParser(description='')
parser.add_argument('subfolder', type=str, help='Subfolder')
parser.add_argument('--threshold', type=float, default=160, help='Threshold')
parser.add_argument('--save_ims', type=bool, default=False, help='Save images per category')
args = parser.parse_args()



data_folder = 'data'

for subfolder in os.listdir(data_folder):
    if (args.subfolder != '*' and subfolder != args.subfolder):
        continue

    for dirname in os.listdir(join(data_folder, subfolder)):
        print (dirname)
        dirpath = join(data_folder, subfolder, dirname)
        ims_path = join(dirpath, 'images')
        precomputed_path = join(dirpath, 'precomputed')
        if (not isdir(precomputed_path)):
            os.makedirs(precomputed_path)
            
        
            
            
        ims_per_cat = {}
        for filename in os.listdir(ims_path):
            fileid = splitext(filename)[0].split('_')
            direction, orbit = common.get_direction_orbit(fileid)
            if (orbit is None):
                raise Exception('No orbit found in filename')
            cat = orbit
            if (direction is not None):
                cat = direction + '_' + orbit
            
            if (cat not in ims_per_cat):
                ims_per_cat[cat] = []
                
            filepath = join(ims_path, filename)
            
            im_np = tifffile.imread(filepath)
            
            dircat = join(precomputed_path, 'ims', cat)
            
            if (not isdir(dircat)):
                os.makedirs(dircat)
                
            dim_np = im_np[:,:,0] / 320
            dim_np[dim_np > 1] = 1
                
            if (args.save_ims):
                tifffile.imsave(join(dircat, filename), dim_np)
            
            
            ims_per_cat[cat].append(im_np)
            
        all_min = []
        for cat in ims_per_cat:
            ims = np.array(ims_per_cat[cat])

            min_np = np.min(ims, axis=0)
            all_min.append(min_np)
            median_np = np.median(ims, axis=0)
            std_np = np.std(ims, axis=0)
            if (len(median_np.shape) > 1):
                tifffile.imsave(join(precomputed_path, 'min_'+cat+'.tif'), min_np[:,:,[0,0,0]].astype(float))
                tifffile.imsave(join(precomputed_path, 'median_'+cat+'.tif'), median_np[:,:,[0,0,0]])
                tifffile.imsave(join(precomputed_path, 'std_'+cat+'.tif'), std_np[:,:,[0,0,0]])
        #sys.exit()
        
        always_occupied_np = np.max(all_min, axis=0) > args.threshold
        tifffile.imsave(join(precomputed_path, 'always_occupied.tif'), always_occupied_np[:,:,0].astype(float))