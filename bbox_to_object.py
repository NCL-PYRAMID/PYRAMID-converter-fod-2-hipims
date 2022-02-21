###############################################################################
# Deep Learning model to HiPIMS data converter
# Amy Green, Robin Wardle
# February 2022
###############################################################################

###############################################################################
# Install Python packages
###############################################################################
import os
import pathlib
import shutil
import csv
import zipfile

import pandas as pd
import numpy as np
from shapely.geometry import Polygon, box, Point


###############################################################################
# Paths
###############################################################################
# Setup base path
platform = os.getenv("PLATFORM")
if platform=="docker":
    data_path = os.getenv("DATA_PATH", "/data")
else:
    data_path = os.getenv("DATA_PATH", "./data")

# Data paths and files
input_path = data_path / pathlib.Path("inputs")
dsr_input_path = input_path / pathlib.Path("dsr")
bbs_input_path = dsr_input_path / pathlib.Path("BboxAndScore")
bbs_input_file = bbs_input_path / pathlib.Path("BboxAndScore_4.txt")
data_file = input_path / pathlib.Path("sample_car_data.txt")

output_path = data_path / pathlib.Path("outputs")
results_file = output_path / pathlib.Path("vehicle_objects.txt")

if output_path.exists() and output_path.is_dir():
    shutil.rmtree(output_path)
pathlib.Path.mkdir(output_path)

# Unzip the input data if it exists as a dataslot
zipfile_dir = pathlib.Path("./data/inputs")
zipfile_name = pathlib.Path("dl-outputs-sample.zip")
if pathlib.Path(zipfile_dir / zipfile_name).exists():
    with zipfile.ZipFile(zipfile_dir / zipfile_name, 'r') as zip_ref:
        zip_ref.extractall(zipfile_dir)


###############################################################################
# Processing
###############################################################################
# Score threshold
score_thresh = 0.8

# Percentage errors for similar cars
err = 10  # error allowed (%)

# read in sample car data
sample_cars = pd.read_csv(data_file, index_col=0)

# read in detected objects (small vehicles only)
small_vehicles = np.fromfile(bbs_input_file, sep=" ")
small_vehicles = small_vehicles.reshape([int(small_vehicles.shape[0] / 9), 9])
scores = small_vehicles[:, -1]
bboxes = small_vehicles[:, 0:-1]

output = pd.DataFrame(columns=[
    "center_x",
    "center_y",
    "length",
    "width",
    "height",
    "weight",
    "angle",
    "score"])

for i in range(scores.shape[0]):
    coords = bboxes[i]
    obj = Polygon([[coords[0], coords[1]], [coords[2], coords[3]], [coords[4], coords[5]], [coords[6], coords[7]]])

    # get centre location for object
    center_x = obj.centroid.x
    center_y = obj.centroid.y

    # get width and length of object
    length1 = Point(obj.exterior.coords[0]).distance(Point(obj.exterior.coords[1]))
    length2 = Point(obj.exterior.coords[0]).distance(Point(obj.exterior.coords[3]))
    length = 0.1 * max(length1, length2)
    width = 0.1 * min(length1, length2)

    # get angle of rotation (from x-axis, anti-clockwise in degrees)
    angles = np.array([np.arctan2((obj.exterior.coords[idx][1] + obj.exterior.coords[idx + 1][1]) / 2,
                                  (obj.exterior.coords[idx][0] + obj.exterior.coords[idx + 1][0]) / 2) for idx in
                       range(4)])
    dists = np.array([np.sqrt(((obj.exterior.coords[idx][0] + obj.exterior.coords[idx + 1][0]) / 2 - center_x) ** 2 + (
                (obj.exterior.coords[idx][1] + obj.exterior.coords[idx + 1][1]) / 2 - center_y) ** 2) for idx in
                      range(4)])
    angle = np.degrees(angles[np.argmax(dists)])  # getting angle to midpoint of furthest away line of polygon

    # get sample cars within err% of width and length of object
    similar_vehicles = (abs(sample_cars.Length - length) <= length * 0.01 * err) & (
                abs(sample_cars.Width - width) <= width * 0.01 * err)

    if sample_cars[similar_vehicles].shape[0] > 0:
        height, weight = sample_cars[similar_vehicles][["Height", "Weight"]].mean()

        if scores[i] >= score_thresh:
            data = [center_x,
                    center_y,
                    length,
                    width,
                    height,
                    weight,
                    angle,
                    scores[i]]
            if all(~np.isnan(data)):
                output.loc[i, ["center_x",
                               "center_y",
                               "length",
                               "width",
                               "height",
                               "weight",
                               "angle",
                               "score"]] = data

###############################################################################
# Output
###############################################################################
output.to_csv(results_file, index=False)
