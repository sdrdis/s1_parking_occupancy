import os
from os.path import join, isdir, splitext
import tifffile
import scipy.misc
import numpy as np
from datetime import datetime
import scipy.stats
import imageio
import argparse
import common

parser = argparse.ArgumentParser(description='')
parser.add_argument('--subfolder', type=str, default='*', help='Subfolder')
parser.add_argument('--debug_path', type=str, default='', help='Debug folder path')
parser.add_argument('--threshold', type=float, default=0.0160, help='Threshold')
args = parser.parse_args()

root_data_path = 'data'
output_path = 'output'
debug_path = args.debug_path

for subfolder in os.listdir(root_data_path):
    if (args.subfolder != '*'):
        if (subfolder != args.subfolder):
            continue
    data_path = join(root_data_path, subfolder)
    for dirname in os.listdir(data_path):
        print (dirname)
        dirpath = join(data_path, dirname)
        im_path = join(dirpath, 'images')
        to_path = join(output_path, subfolder, dirname)
        if (not isdir(to_path)):
            os.makedirs(to_path)
            
        debug_subdir_path = ''
        if (debug_path != ''):
            debug_subdir_path = join(debug_path, subfolder, dirname)
            if (not isdir(debug_subdir_path)):
                os.makedirs(debug_subdir_path)
        mask_np = scipy.misc.imread(join(dirpath, 'mask.png')) > 127
        no_mask_np = np.logical_not(mask_np)
        dates = []
        occupancies = []
        orbit_ids = []
        orbit_directions = []
        ious = []
        last_occupancy_np = None
        for filename in sorted(os.listdir(im_path)):
            filename_dt = datetime.strptime('_'.join(filename.split('_')[:2]), "%Y%m%d_%H%M%S")
            fileid = splitext(filename)[0].split('_')
            
            orbit_direction, orbit_id = common.get_direction_orbit(fileid)
            if (orbit_id is None):
                orbit_id = '?'
            if (orbit_direction is None):
                orbit_direction = '?'
            
            filepath = join(im_path, filename)
            im_np = tifffile.imread(filepath)
            threshold_np = im_np[:,:,0] > args.threshold
            threshold_np[no_mask_np] = 0
            
            if (debug_subdir_path != ''):
                tifffile.imsave(join(debug_subdir_path, filename), threshold_np.astype(float))
            
            occupancy_np = threshold_np[mask_np]
            if (last_occupancy_np is not None):
                iou = np.sum(np.logical_and(occupancy_np, last_occupancy_np)) / np.sum(np.logical_or(occupancy_np, last_occupancy_np))
            else:
                iou = 0
            occupancy = np.sum(occupancy_np) / np.sum(mask_np)
            dates.append(filename_dt)
            occupancies.append(occupancy)
            ious.append(iou)
            orbit_ids.append(orbit_id)
            orbit_directions.append(orbit_direction)
            last_occupancy_np = occupancy_np
            
        np.savez_compressed(join(to_path, 'predictions.npz'), dates=dates, occupancies=occupancies, ious=ious, orbit_ids=orbit_ids, orbit_directions=orbit_directions)