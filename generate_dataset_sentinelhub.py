from sentinelhub import WebFeatureService, BBox, CRS, DataSource, WmsRequest, WcsRequest, BBox, constants
import numpy as np
from os.path import join, isdir, isfile
import os
import tifffile
import json
import argparse

# https://forum.step.esa.int/t/sentinel-1-relative-orbit-from-filename/7042
def get_orbit_id(id):
    sid = id.split('_')
    sat = sid[0]
    abs_orbit = int(sid[-3])
    if (sat == 'S1A'):
        orbit_id = (abs_orbit - 73) % 175 + 1
    else:
        orbit_id = (abs_orbit - 27) % 175 + 1
    
    return "{:03d}".format(orbit_id)
    
INSTANCE_ID = 'f4f0f030-c7cc-4707-a579-98fd1c76b588'

data_path = 'data'
positions_path = 'positions'

parser = argparse.ArgumentParser(description='')
parser.add_argument('positions_id', type=str, help='Positions filename')
parser.add_argument('--from_datetime', type=str, default='2019-01-01T00:00:00', help='From date')
parser.add_argument('--to_datetime', type=str, default='2020-03-31T23:59:59', help='To date')
parser.add_argument('--resolution', type=str, default='5m', help='Resolution')
args = parser.parse_args()


filename = args.positions_id+'.npz'
subfolder = args.positions_id

filepath = join(positions_path, filename)
if (filename.endswith('.npz')):
    data = np.load(filepath)
    shapes = data['shapes']
    dirnames = data['dirnames']
else:
    with open(filepath, 'r') as f:
        data = json.load(f)
    shapes = data['shapes']

    
margin = 0.001

for i in range(len(shapes)):#range(len(shapes)):
    print ('*'*10, i)
    shape = np.array(shapes[i])
    
    from_pos = np.min(shape, axis=0) - margin
    to_pos = np.max(shape, axis=0) + margin
    
    bb = np.array([from_pos, to_pos])
    
    
    to_path = join(data_path, subfolder, dirnames[i])
    to_images_path = join(to_path, 'images')
    if (not isdir(to_path)):
        os.makedirs(to_path)
        
    if (not isdir(to_images_path)):
        os.makedirs(to_images_path)
    
    np.savez_compressed(join(to_path, 'metadata.npz'), shape=shape, bb=bb)
    
    search_bbox = BBox(bbox=[(bb[0,0],bb[0,1]),(bb[1,0],bb[1,1])], crs=CRS.WGS84)
    
    search_time_interval = (args.from_datetime, args.to_datetime)
    wfs_iterator = WebFeatureService(search_bbox, search_time_interval,
                                 data_source=DataSource.SENTINEL1_IW,
                                 maxcc=1.0, instance_id=INSTANCE_ID)
    
    additional_data = []
    for el in wfs_iterator:
        additional_data.append([el['properties']['id'].split('_')[0], el['properties']['orbitDirection'], get_orbit_id(el['properties']['id'])])
     
    dates = wfs_iterator.get_dates()
    
    last_date = None
    for i in range(len(dates)):
        d = dates[i]
        if (last_date is not None):
            if ((last_date - d).total_seconds() < 3600):
                continue
        
        last_date = d
        add_data = additional_data[i]
        filepath = join(to_images_path, d.strftime("%Y%m%d_%H%M%S") + '_' + '_'.join(add_data) + '.tif')
        if (isfile(filepath)):
            continue
        print (d)
        s1_request = WcsRequest(data_source=DataSource.SENTINEL1_IW,
                                 layer='BOTH',
                                 bbox=search_bbox,
                                 time=d,
                                 resx=args.resolution, resy=args.resolution,
                                 image_format=constants.MimeType.TIFF_d32f, #_d32f
                                 instance_id=INSTANCE_ID)
        
        s1_data = s1_request.get_data()
        tifffile.imsave(filepath, np.dstack((s1_data[-1], np.zeros((s1_data[-1].shape[0],s1_data[-1].shape[1])))), compress=7)
        
    #sys.exit()