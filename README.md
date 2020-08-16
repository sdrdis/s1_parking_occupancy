# PARKING OCCUPANCY ESTIMATION ON SENTINEL-1 IMAGES

Implementation for our ISPRS 2020 paper [PARKING OCCUPANCY ESTIMATION ON SENTINEL-1 IMAGES](https://www.isprs-ann-photogramm-remote-sens-spatial-inf-sci.net/V-2-2020/821/2020/).

Authors:
* Sébastien Drouyer ([Website](http://sebastien.drouyer.com/), [Github](https://github.com/sdrdis), [Twitter](https://twitter.com/sdrdis))
* Carlo de Franchis ([Website](http://cdefranc.perso.math.cnrs.fr/), [Github](https://github.com/carlodef))


## Step 1: generation of positions files

Positions can be generated from KMLs for example:

```
python utils_generate_positions_from_kmls.py kmls_folder id
```

Where `kmls_folder` is a folder containing kmls and `id` is an identifier (for example "retail_parkings")

Generates a NPZ file containing coordinates of all parkings to monitor in the `positions` folder.

## Step 2: generate dataset

Generate dataset (example below from sentinel-hub website)

```
python generate_dataset_sentinelhub.py id
```

Where `id` is an identifier (for example "retail_parkings").

Generates folders in `data/{id}` containing images.

## Step 3: evaluate masks

### First way: simple mask

Generate parking masks.

```
python generate_masks.py
```

Generates images (all ids) in `data` indicating where the parking is and where it is not.

### Second way: mask minus always occupied areas


Generate parking masks.

```
python generate_stats_per_orbit.py id
python generate_masks_minus_always_occupied.py id
```

Where `id` is an identifier (for example "retail_parkings").

`generate_stats_per_orbit.py` generates stats per orbit (median, std, min).

`generate_masks_minus_always_occupied.py` generates a mask removing areas where it is always occupied.

## Step 4: evaluate occupancy

Estimate occupancy rates.

### First way: simple thresholding

```
python estimate_simple.py
```

Applies a simple thresholding on all images (all ids). See parameters `python estimate_simple.py --help`.

### Second way: thresholding compared to weekends

TODO

## Step 5: generate csv

CSV are generated using following script:

```
python generate_csvs.py id
```

Where `id` is an identifier (for example "retail_parkings").

CSVs and graphs are generated in the `output_csv/{id}` folder.