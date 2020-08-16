import pandas as pd
import numpy as np
import csv
from os.path import splitext, join
import os

import argparse


parser = argparse.ArgumentParser(description='')
parser.add_argument('subfolder', type=str, help='Subfolder')
args = parser.parse_args()

csv_path = 'output_csv'


path = join(csv_path, args.subfolder)

for filename in os.listdir(path):
    if (splitext(filename)[1] != '.csv' or filename.startswith('analysis_')):
        continue
        
    df = pd.read_csv(join(path, filename), skiprows=[1]) #, header=0, names=['Date'] + cols + ['Total', 'Total IOU', 'Orbit', 'Direction'])
    
    cols = []
    for key in df:
        if (key.isnumeric()):
            cols.append(key)
            
    orbits = np.unique(df['Orbit'])

    with open(join(path, 'analysis_' + filename), 'w') as f:
        w = csv.writer(f, lineterminator="\n")
        
        w.writerow(['Direction', 'Orbit'] + cols + ['Total'])
        
        for orbit in orbits:
            sel_df = df[df['Orbit'] == orbit]
            

            row = [sel_df.iloc[0]['Direction'], orbit]
            for col in cols:
                row.append(str(int(round(np.mean(sel_df[col]) * 100))) + ' -+ ' + str(int(round(np.std(sel_df[col]) * 100))))
                
            row.append(str(int(round(np.mean(sel_df['Total']) * 100))) + ' -+ ' + str(int(round(np.std(sel_df['Total']) * 100))))
            w.writerow(row)