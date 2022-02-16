

# PYRAMID Deep Learning to HiPIMS data converter model

## About
This model takes output from the [DL object detection model](https://github.com/NCL-PYRAMID/PYRAMID-object-detection) in the form of a list of polygons (rectangles), and writes out these objects as floating debris models suitable for use in [HiPIMS](https://github.com/NCL-PYRAMID/PYRAMID-HiPIMS).

### Project Team
Amy Green, Newcastle University  ([a.c.brown@newcastle.ac.uk](mailto:a.c.brown@newcastle.ac.uk))  
Xue Tong, Loughborough University ([x.tong2@lboro.ac.uk](mailto:x.tong2@lboro.ac.uk))  
Shidong Wang, Newcastle University ([shidong.wang@newcastle.ac.uk](mailto:shidong.wang@newcastle.ac.uk))  
Elizabeth Lewis, Newcastle University  ([elizabeth.lewis2@newcastle.ac.uk](mailto:elizabeth.lewis2@newcastle.ac.uk))  

### RSE Contact
Robin Wardle  
RSE Team, Newcastle Data  
Newcastle University NE1 7RU  
([robin.wardle@newcastle.ac.uk](mailto:robin.wardle@newcastle.ac.uk))  

## Built With

[Python 3](https://www.python.org)  
* [pandas](https://pandas.pydata.org)  
* [numpy](https://numpy.org)  
* [shapely](https://github.com/shapely/shapely)  

[Docker](https://www.docker.com)  

Other required tools: [tar](https://www.unix.com/man-page/linux/1/tar/), [zip](https://www.unix.com/man-page/linux/1/gzip/).

## Getting Started

### Prerequisites
The `requirements.txt` file lists the Python and module versions required.

### Installation
The application is a Python 3 script and needs no installation for local execution. Deployment to DAFNI is covered below.

### Running Locally
The model can be run from the command-line as

```
python bbox_to_object.py
```

The results of the processing are written to a file:

```
./data/outputs/vehicle_objects.txt
```

### Running Tests
Some default data for testing is in

```
./data/inputs
```

There are no unit test cases for this model at present.

## Deployment

### Local
A local Docker container that mounts the test data can be built and executed using:

```
docker build . -t pyramid-dl-2-hipims
docker run -v "$(pwd)/data:/data" pyramid-dl-2-hipims
```

Note that output from the container, placed in the `./data` subdirectory, will have `root` ownership as a result of the way in which Docker's access permissions work.

### Production
#### DAFNI upload
The model is containerised using Docker, and the image is _tar_'ed and _zip_'ed for uploading to DAFNI. Use the following commands in a *nix shell to accomplish this.

```
docker build . -t pyramid-dl-2-hipims
docker save -o pyramid-dl-2-hipims.tar pyramid-dl-2-hipims:latest
gzip pyramid-dl-2-hipims.tar
```

The `pyramid-dl-2-hipims.tar.gz` Docker image and accompanying DAFNI model definintion file (`model-definition.yml`) can be uploaded as a new model using the "Add model" facility at [https://facility.secure.dafni.rl.ac.uk/models/](https://facility.secure.dafni.rl.ac.uk/models/).

## Usage
The deployed model can be run in a DAFNI workflow. See the [DAFNI workflow documentation](https://docs.secure.dafni.rl.ac.uk/docs/how-to/how-to-create-a-workflow) for details.

## Roadmap
- [x] Initial Research  
- [ ] Minimum viable product <-- You are Here  
- [ ] Alpha Release  
- [ ] Feature-Complete Release  

## Contributing
TBD

### Main Branch
All development can take place on the main branch. 

## License
This code is private to the the PYRAMID project.

## Acknowledgements
This work was funded by NERC, grant ref. NE/V00378X/1, “PYRAMID: Platform for dYnamic, hyper-resolution, near-real time flood Risk AssessMent Integrating repurposed and novel Data sources”. See the project funding [URL](https://gtr.ukri.org/projects?ref=NE/V00378X/1).

