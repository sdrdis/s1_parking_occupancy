import skimage.draw
import numpy as np
import tifffile
import scipy.misc
import os
from os.path import join
import scipy.ndimage
import imageio

root_data_path = 'data'

for subfolder in os.listdir(root_data_path):
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
        imageio.imsave(join(dirpath, 'mask.png'), np.flipud(mask_np).astype('uint8') * 255)