import os
from os.path import join, splitext, isdir
from fastkml import kml
import numpy as np
import argparse



parser = argparse.ArgumentParser(description='')
parser.add_argument('kml_folder', type=str, help='KMLs folder')
parser.add_argument('positions_filename', type=str, help='Positions filename')
args = parser.parse_args()

positions_folder = 'positions'

if (not (isdir(positions_folder))):
    os.makedirs(positions_folder)

from_path = args.kml_folder
to_path = join(positions_folder, args.positions_filename)

if (not to_path.endswith('.npz')):
    to_path = to_path + '.npz'

shapes = []
dirnames = []
for filename in os.listdir(from_path):
    with open(join(from_path, filename), 'r', encoding="utf-8") as myfile:
        doc = myfile.read().encode('utf-8')
    k = kml.KML()
    k.from_string(doc)
    f = list(k.features())
    for el in f[0].features():
        xys = el.geometry.boundary.coords.xy
        shape = np.vstack((xys[0], xys[1])).transpose()
        shapes.append(shape)
        dirnames.append(splitext(filename)[0])

np.savez_compressed(to_path, shapes=shapes, dirnames=dirnames)