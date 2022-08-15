###############################################################################
# Deep Learning model to HiPIMS data converter
# Amy Green, Robin Wardle
# February 2022
###############################################################################

###############################################################################
# Install Python packages
###############################################################################
import os
# import pathlib
from pathlib import Path
# import shutil
import csv
import zipfile
from datetime import datetime

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

    
# INPUT imagery names
img_name = ['Z2463', 'Z2464', 'Z2465', 'Z2563', 'Z2564', 'Z2565', 'Z2664']
dota_1_0_res, dota_1_5_res = [], []

# INPUT data paths and files
input_path = data_path / Path("inputs")
input_path_src1_0 = input_path / Path("dota_1_0_res")
output_path = data_path / Path("outputs")
# Remove the output path if it exists, and create a new one
if output_path.exists() and output_path.is_dir():
    # shutil.rmtree(output_path)
    os.remove(output_path)
pathlib.Path.mkdir(output_path)

results_file_1_0 = output_path / pathlib.Path("vehicle_objects_1_0.txt")
results_file_1_5 = output_path / pathlib.Path("vehicle_objects_1_5.txt")

for i in range(len(img_name)):
    with open(Path(input_path_src1_0, "BboxAndScore_{}._{}.txt".format(img_name[i], 4)), "r") as f10:
        post_processing(input_path_src1_0, f10, results_file_1_0)
        print ("Finish the postprocessing of results obtained using DOTA 1.0")

input_path_src1_5 = input_path / Path("dota_1_5_res")
for j in range(len(img_name)):
    with open(Path(input_path_src1_5, "BboxAndScore_{}._{}.txt".format(img_name[i], 4)), "r") as f15:
        post_processing(input_path_src1_5, f15, results_file_1_5)
        print ("Finish the postprocessing of results obtained using DOTA 1.5")
"""
# INPUT data paths and files
input_path = data_path / pathlib.Path("inputs")
dsr_input_path = input_path / pathlib.Path("dsr")
bbs_input_path = dsr_input_path / pathlib.Path("BboxAndScore")
bbs_input_file = bbs_input_path / pathlib.Path("BboxAndScore_4.txt")
data_file = input_path / pathlib.Path("sample_car_data.txt")

# DAFNI test dataset - unzip the sample data file
zipfile_name = pathlib.Path("dl-outputs-sample.zip")
if pathlib.Path(input_path / zipfile_name).exists():
    with zipfile.ZipFile(input_path / zipfile_name, 'r') as zip_ref:
        zip_ref.extractall(input_path)

# OUTPUT data paths and files
output_path = data_path / pathlib.Path("outputs")
"""

###############################################################################
# Processing
###############################################################################
# Score threshold
score_thresh = 0.8

# Percentage errors for similar cars
err = 10  # error allowed (%)

def post_processing(data_file, bbs_input_file, results_file):
    
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
    # Output results file
    ###############################################################################
    output.to_csv(results_file, index=False)

###############################################################################
# Create metadata file
# Originally taken from the CITYCAT project:
#  https://github.com/OpenCLIM/citycat-dafni
###############################################################################
app_title = "pyramid-dl-2-hipims"
app_description = "Default dataslot test output"
metadata = f"""{{
  "@context": ["metadata-v1"],
  "@type": "dcat:Dataset",
  "dct:title": "{app_title}",
  "dct:description": "{app_description}",
  "dct:identifier":[],
  "dct:subject": "Environment",
  "dcat:theme":[],
  "dct:language": "en",
  "dcat:keyword": ["PYRAMID"],
  "dct:conformsTo": {{
    "@id": null,
    "@type": "dct:Standard",
    "label": null
  }},
  "dct:spatial": {{
    "@id": null,
    "@type": "dct:Location",
    "rdfs:label": null
  }},
  "geojson": {{}},
  "dct:PeriodOfTime": {{
    "type": "dct:PeriodOfTime",
    "time:hasBeginning": null,
    "time:hasEnd": null
  }},
  "dct:accrualPeriodicity": null,
  "dct:creator": [
    {{
      "@type": "foaf:Organization",
      "@id": "http://www.ncl.ac.uk/",
      "foaf:name": "Newcastle University",
      "internalID": null
    }}
  ],
  "dct:created": "{datetime.now().isoformat()}Z",
  "dct:publisher":{{
    "@id": null,
    "@type": "foaf:Organization",
    "foaf:name": null,
    "internalID": null
  }},
  "dcat:contactPoint": {{
    "@type": "vcard:Organization",
    "vcard:fn": "DAFNI",
    "vcard:hasEmail": "support@dafni.ac.uk"
  }},
  "dct:license": {{
    "@type": "LicenseDocument",
    "@id": "https://creativecommons.org/licences/by/4.0/",
    "rdfs:label": null
  }},
  "dct:rights": null,
  "dafni_version_note": "created"
}}
"""

with open(os.path.join(output_path, 'metadata.json'), 'w') as f:
    f.write(metadata)
