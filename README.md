

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

## Getting Started

### Prerequisites

Any tools or versions of languages needed to run code. For example specific Python or Node versions. Minimum hardware requirements also go here.

### Installation

How to build or install the applcation.

### Running Locally

How to run the application on your local system.

### Running Tests

How to run tests on your local system.

## Deployment

### Local

#### Preparation for upload to DAFNI
docker build . -t pyramid-dl-2-hipims

docker run -v "$(pwd)/data:/data" pyramid-dl-2-hipims

docker save -o pyramid-dl-2-hipims.tar pyramid-dl-2-hipims:latest

gzip pyramid-dl-2-hipims.tar

### Production

Deploying to the production system. Examples of this would include cloud, HPC or virtual machine. 

## Usage

Any links to production environment, video demos and screenshots.

## Roadmap

- [x] Initial Research  
- [ ] Minimum viable product <-- You are Here  
- [ ] Alpha Release  
- [ ] Feature-Complete Release  

## Contributing

### Main Branch
Protected and can only be pushed to via pull requests. Should be considered stable and a representation of production code.

### Dev Branch
Should be considered fragile, code should compile and run but features may be prone to errors.

### Feature Branches
A branch per feature being worked on.

https://nvie.com/posts/a-successful-git-branching-model/

## License

## Citiation

Please cite the associated papers for this work if you use this code:

```
@article{xxx2021paper,
  title={Title},
  author={Author},
  journal={arXiv},
  year={2021}
}
```


## Acknowledgements
This work was funded by a grant from the UK Research Councils, EPSRC grant ref. EP/L012345/1, “Example project title, please update”.

