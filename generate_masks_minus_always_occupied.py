import skimage.draw
import numpy as np
import tifffile
import scipy.misc
import os
from os.path import join, isfile
import scipy.ndimage
import imageio
import argparse

root_data_path = 'data'

parser = argparse.ArgumentParser(description='')
parser.add_argument('subfolder', type=str, help='Subfolder')
parser.add_argument('--dilations', type=int, default=2, help='Resolution in meter')
args = parser.parse_args()

for subfolder in os.listdir(root_data_path):
    if (args.subfolder != '*' and subfolder != args.subfolder):
        continue

    data_path = join(root_data_path, subfolder)
    for dirname in os.listdir(data_path):
        print (dirname)
        dirpath = join(data_path, dirname)
        data = np.load(join(dirpath, 'metadata.npz'))
        bb = data['bb']
        shape = data['shape']
        
        filepath = join(join(dirpath, 'images'), os.listdir(join(dirpath, 'images'))[0])
        im_np = tifffile.imread(filepath)
        
        borders = shape

        mask_np = np.zeros(im_np.shape[:2], dtype=bool)
        x = (borders[:,0] - bb[0,0]) / (bb[1,0] - bb[0,0])
        y = (borders[:,1] - bb[0,1]) / (bb[1,1] - bb[0,1])

        

        x = np.round(x * mask_np.shape[1]).astype(int)
        y = np.round(y * mask_np.shape[0]).astype(int)

        rr, cc = skimage.draw.polygon(y, x)

        mask_np[rr, cc] = True
        
        mask_np = np.flipud(mask_np)
        
        always_occupied_path = join(dirpath, 'precomputed', 'always_occupied.tif')
        
        if (not isfile(always_occupied_path)):
            raise Exception ('No always occupied file! Please launch generate_stats_per_orbit before!')
        
        always_occupied_np = tifffile.imread(always_occupied_path) > 0.5
        
        if (args.dilations > 0):
            always_occupied_np = scipy.ndimage.binary_dilation(always_occupied_np, iterations=args.dilations)
        
        mask_np[always_occupied_np] = False
        
        imageio.imsave(join(dirpath, 'mask.png'), mask_np.astype('uint8') * 255)