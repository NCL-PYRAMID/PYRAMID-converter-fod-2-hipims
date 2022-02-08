# install relevent packages
import pandas as pd
import numpy as np
from os.path import join

from shapely.geometry import Polygon, box, Point

######## input variables to change

# folder path for bounding box output (saved as seperate files for each grouping)
folder_path = r"C:\Users\Amy\OneDrive - Newcastle University\Documents\PYRAMID\Shidong\Geospatial\Detection and Segmentation Results\BboxAndScore"

# folder path for sample car data
sample_data_path = r"C:\Users\Amy\OneDrive - Newcastle University\Documents\PYRAMID\sample_car_data.txt"

# output file path
output_path = "vehicle_objects.txt"

# score threshold
score_thresh = 0.8

# percentage errors for similar cars
err = 10  # error allowed (%)

# read in sample car data
sample_cars = pd.read_csv(sample_data_path, index_col=0)

# read in detected objects (small vehicles only)
small_vehicles = np.fromfile(join(folder_path, "BboxAndScore_4.txt"), sep=" ")
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

# save output
output.to_csv(output_path, index=False)