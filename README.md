# HashStream
HashStream is a pure python module for analyzing the hashtag graphs from raw Twitter stream data. 

With a simple user interface, based on scikit-style class calls and process flow, HashStream can be used both for bulk data post processing, and for real-time on-the-fly data extraction. 

## Introduction
If you're more of a hands-on learner, why not check out the [tutorial](/src/hashstream_tutorial.ipynb), a Jupyter Notebook you can either view here on GitHub, or download and run for yourself if you have Jupyter installed. 

static blah

dynamic blah

This project was completed for the [*Insight Data Engineering*](http://insightdataengineering.com/) coding challenge, finished April 4, 2016. As such the current structure meets requirements for the challenge, as opposed to standard Python/Pypy practices (example, the `src/` file, which is not very Pythonic). Plans are in place to restructure post-challenge, so bear with us as we change things up!

## Installation 
Simply download and extract the .zip file in your desired directory. Running the included `main.py` file in the `src` module will require two additional arguments in the command, specifically the input data and the name/location of the output.
  
  `$ python main.py path/to/input.txt path/to/output.txt`
  
It will run a simple test, extracting all average degrees for the hashtag graph, rolled over 60s time windows, sourced from the input file. If you've already placed a file called `tweets.txt` in the `tweet_input` folder, you can alternatively just try 

  `$ ./run.sh`

from the root directory, which will call `main.py` with some default arguments. 

**Dependencies**
- [Numpy](http://www.numpy.org/): "The fundamental package for scientific computing with Python." -- *array manipulation*
- [Pandas](http://pandas.pydata.org/pandas-docs/version/0.18.0/): "Package providing fast, flexible, and expressive data structures designed to make working with “relational” or “labeled” data both easy and intuitive" -- *timestamp handling and filtering*
- [NetworkX](https://networkx.github.io/index.html) : "A Python language software package for the creation, manipulation, and study of the structure, dynamics, and functions of complex networks" -- *graph construction, visualization, and analysis*

**Optional**
Not having/installing these will not break hashstream, but they can provide a nicer experience while using this module. 
- [TQDM](https://pypi.python.org/pypi/tqdm): "A Fast, Extensible Progress Meter"
- [MatPlotLib](http://matplotlib.org/): "python 2D plotting library" -- *native visualization of graphs*

