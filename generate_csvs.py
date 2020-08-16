import os
import numpy as np
from os.path import join, isdir
import csv
from area import area
import imageio
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser(description='')
parser.add_argument('subfolder', type=str, help='Subfolder')
parser.add_argument('--resolution', type=float, default=5, help='Resolution in meter')
#parser.add_argument('--row_area', type=bool, default=False, help='Row of areas')

args = parser.parse_args()

data_path = 'data'
output_path = 'output'
output_csv_path = 'output_csv'

input_path = join(data_path, args.subfolder)
path = join(output_path, args.subfolder)
csv_path = join(output_csv_path, args.subfolder)

if (not isdir(csv_path)):
    os.makedirs(csv_path)

all_data = {}
all_subids = {}
all_areas = {}
all_misc = {}
for dirname in os.listdir(path):
    did = '_'.join(dirname.split('_')[:-1])
    subid = dirname.split('_')[-1]
    
    
    mask_np = imageio.imread(join(input_path,dirname,'mask.png'))
    mask_np = mask_np > 127
    metadata = np.load(join(input_path,dirname,'metadata.npz'))
    shape = metadata['shape']
    
    obj = {'type':'Polygon','coordinates':[shape.tolist()]}

    area_m2 = np.sum(mask_np) * args.resolution * args.resolution #area(obj)
    
    if not(did in all_data):
        all_data[did] = {}
        all_subids[did] = set()
        all_areas[did] = {}
        all_misc[did] = {}
        
    all_areas[did][subid] = area_m2
    all_subids[did].add(subid)
    data = np.load(join(path, dirname, 'predictions.npz'))
    dates = data['dates']
    occupancies = data['occupancies']
    ious = data['ious']
    orbit_ids = data['orbit_ids']
    orbit_directions = data['orbit_directions']
    
    for i in range(len(dates)):
        d = dates[i]
        occ = occupancies[i]
        iou = ious[i]
        if not(d in all_data[did]):
            all_data[did][d] = {}
            
        all_data[did][d][subid] = [occ, iou]
        all_misc[did][d] = [orbit_ids[i], orbit_directions[i]]
        
for key in all_data:
    print (key)
    with open(join(csv_path, key + '.csv'), 'w') as f:
        w = csv.writer(f, lineterminator="\n")
        subids_l = sorted(list(all_subids[key]))
        w.writerow(['Date'] + subids_l + ['Total', 'Total IOU', 'Orbit', 'Direction'])
        
        row_area = ['Area']
        areas = []
        for subid in subids_l:
            area = all_areas[key][subid]
            row_area.append(area)
            areas.append(area)
        row_area.append(np.sum(areas))
        areas = np.array(areas)
        w.writerow(row_area)
        
        weekdays = []
        total_occs_dates = []
        total_occs = []
        total_ious = []
        p_wd = [[] for i in range(7)]
        for d in all_data[key]:
            [orbit_id, orbit_direction] = all_misc[key][d]
        
            wd = int(d.strftime('%w'))
            row = [d.strftime("%Y-%m-%dT%H:%M:%S")]
            occs = []
            ious = []
            for subid in subids_l:
                occ, iou = all_data[key][d][subid]
                occs.append(occ)
                ious.append(iou)
                row.append(occ)
                
                
            total_occ = np.sum(occs*areas)/np.sum(areas)
            total_iou = np.sum(ious*areas)/np.sum(areas)
            
            total_ious.append(total_iou)
            total_occs.append(total_occ)
            total_occs_dates.append(d)
            weekdays.append(wd)
            row.append(total_occ)
            row.append(total_iou)
            row.append(orbit_id)
            row.append(orbit_direction)
            w.writerow(row)
            p_wd[wd].append(total_occ)
        
        total_occs = np.array(total_occs)
        total_occs_dates = np.array(total_occs_dates)
        total_ious = np.array(total_ious)
        weekdays = np.array(weekdays)
        
        '''
        sel = np.logical_and(weekdays != 0, weekdays != 6)
        total_occs = total_occs[sel]
        total_occs_dates = total_occs_dates[sel]
        total_ious = total_ious[sel]
        '''
        
        
        plt.clf()
        plt.plot(total_occs_dates, total_occs)
        plt.title(key)
        plt.xlabel('Date')
        plt.ylabel('Occupancy')
        plt.savefig(join(csv_path, key+'_annual.png')) # _no_weekends
        
        
        
        plt.clf()
        plt.plot(total_occs_dates, total_ious)
        plt.title(key)
        plt.xlabel('Date')
        plt.ylabel('IOUs')
        plt.savefig(join(csv_path, key+'_iou_annual.png'))
        
        
            
        
        weekdays_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        std_wd = np.zeros(len(p_wd))
        for i in range(len(p_wd)):
            std_wd[i] = np.std(p_wd[i])
            p_wd[i] = np.mean(p_wd[i])
            print (i, p_wd[i], std_wd[i])
        p_wd = np.array(p_wd)
        plt.clf()
        plt.bar(weekdays_names, p_wd[[1,2,3,4,5,6,0]], yerr=std_wd[[1,2,3,4,5,6,0]])
        plt.title(key)
        #plt.xticks(np.arange(7), )
        plt.xlabel('Weekday')
        plt.ylabel('Occupancy')
        plt.savefig(join(csv_path, key+'_weekly.png'))
        