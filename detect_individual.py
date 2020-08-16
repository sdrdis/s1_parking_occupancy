import tifffile
import os
from os.path import join, splitext
import scipy.ndimage

path = 'D:\\Developments\\parking_detection_sar\\dataset_kayrros\\data\\pipeline\\tile_191\\images'

for filename in os.listdir(path):
    fileid = splitext(filename)[0]
    type = fileid.split('_')[-1]
    if (type == 'ASCENDING'):
        im_np = tifffile.imread(join(path, filename))[:,:,1]
        #im_np = im_np - scipy.ndimage.grey_opening(im_np, size=(19,19))
        #im_np = (im_np > 5000).astype(float)
        tifffile.imsave(join('debug_output', filename), im_np, compress=7)