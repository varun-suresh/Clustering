# Approximate Rank Order Clustering

## What's in this repository
[clustering.py](https://github.com/varun-suresh/Clustering/blob/master/clustering.py) - Contains the implementaion of the clustering algorithm.

[demo.py](https://github.com/varun-suresh/Clustering/blob/master/demo.py) - An example to demonstrate usage. To run this, you need to download the LFW data from [here](http://vis-www.cs.umass.edu/lfw/). For the face vectors, I used the results from Alfred Xiang Wu's [Face Verification Experiment](https://github.com/AlfredXiangWu/face_verification_experiment/tree/master/results). Also evaluates clustering on the LFW dataset using `evaluation.py`.

[evaluation.py](https://github.com/varun-suresh/Clustering/blob/master/demo.py) - Script to calculate pairwise precision and recall as explained in the paper.
TODO

[server.py](https:github.com/varun-suresh/Clustering) - Script to visualize the results.

## Setup
You will need `cmake` for this installation.

### Step 1:
Create a new virtual environment and clone the repository.
```
mkvirtualenv (env-name)
workon (env-name)
git clone https:github.com/varun-suresh/Clustering.git
```

### Step 2:
Follow the instructions [here](http://www.cs.ubc.ca/research/flann/) to install `pyflann`.

### Step 3:
For the demo, download the LFW data and the face vectors as mentioned above and run

```
cd Clustering
python demo.py --lfw_path path_to_lfw_dir -v vector_file
```

## Results
### f1 score:
The best result I have so far is an f1 score of `0.48`, the precision drops quite drastically as the recall increases. I will plot the results in the next couple of days and visualize the results to better understand why the results are not close to the results in the paper.

### Timing:
Using python's multiprocessing module, clustering LFW faces took about ~40 seconds. I did this on an 8-core machine using 4 processes(Using all 8 does not improve it by much because some cores are needed for background processes). The same experiment took 7 seconds on a 20 core machine.

## Citations
You should cite the following paper if you use the algorithm.
```
@ARTICLE{2016arXiv160400989O,
   author = {{Otto}, C. and {Wang}, D. and {Jain}, A.~K.},
    title = "{Clustering Millions of Faces by Identity}",
  journal = {ArXiv e-prints},
archivePrefix = "arXiv",
   eprint = {1604.00989},
```
Face verification experiment
```
@article{wulight,
  title={A Light CNN for Deep Face Representation with Noisy Labels},
  author={Wu, Xiang and He, Ran and Sun, Zhenan and Tan, Tieniu}
  journal={arXiv preprint arXiv:1511.02683},
  year={2015}
}
```
