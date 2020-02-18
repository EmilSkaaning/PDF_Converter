# Pair Distribution Function Converter
## Introduction
This code was developed as part of my M.Sc. thesis at the University of Copenhagen and is ment to improve data
analysis of x-ray data. More specifical to improve data analysis of _in situ_ measurements using the Pair 
Distribution Function (PDF).   
This simple program is ment to easy the workload of preprocessing the data before modelling is preformed and to
help the user keep track of all used parameters making data reproduceable.   
This framework is build using the following two packages:
 
* [PyFAI](https://pyfai.readthedocs.io/en/latest/)<sup>[1](#references)</sup>
* [PDfgetX3](https://www.diffpy.org/products/pdfgetx.html)<sup>[2](#references)</sup>

Calibration and integration is implemented using PyFAI. What program to use for these tasks are 
an almost religous question, PyFAI was chosen as it supports the most used ones:  
[Fit2D](http://www.esrf.eu/computing/scientific/FIT2D/)<sup>[3](#references)</sup> and 
[Dioptas](http://www.clemensprescher.com/programs/dioptas)<sup>[4](#references)</sup>. 
PyFAI can load both calibration and mask files from either of those programs while still having its own framework for
handling these tasks. This flexibility made it the obivois choise.     
The two following sections will provide a simple guide to installing and running the program. 
A more complete guide for installing, how to use examples and implementation 
can be found in [PDFconverter_manual.pdf](PDFconverter_manual.pdf).  
The __README.md__ file consist of the following sections:

1. [Installing PDF_Converter](#Installing-pdf-converter)
2. [Running the code](#running-the-code)
3. [The GUI](#the-gui)
4. [Argparse](#argparse)
5. [License](#license)
6. [Author](#author)
7. [References](#references)

## Installing PDF_Converter
For running this program i recommend using Python 3.7 but it is compatible down to Python 3.4. If you do not have 
Python installed the easiest way is to install [Anaconda](https://www.anaconda.com/distribution/#windows). Remember to 
add Anaconda to you path when installing it. To verify that python has been installed correctly after installing Anaconda
open your terminal and type _python --version_, if this does not produce an error then you have you
have installed Python correctly!
```
python --version
>>> Python 3.7.4
```
The "hardest" packages to install for this program is functional are PyFAI and PDFgetX3. I recommend reading their  
installation guides, for getting help installing PyFAI [press here](https://pyfai.readthedocs.io/en/latest/operations/index.html#detailed-installation-procedure-on-different-operating-system)
and for PDFgetX3 [press here](https://www.diffpy.org/doc/pdfgetx/2.0.0/install.html). Remember to chose the right operating system!
When these packages are correctly installed then you are practically done, all of the remining packages can simply be
installed using either Anaconda or pip. Unfortunately, the simplest way to install all packages is to run the program
and install the missing packages when it gives an error. Examples on how to install are shown below.
````
pip install tqdm
or
conda install tqdm
````
The number of packages needed to run this program depend on how you chose to install Python. If you chose Anaconda
then you should only have to install 2-3 additional packages.

## Running the code
This program has three core functions: calibration, integration and background subtraction. It is so far 
recommended to use Fit2D for calibration.  
The __main_config.init__ is used to setup the program. To make the program run only three parameters need to be specified,
*Importdir*, *Outputdir* and *Calibrationconfig*. If nothing else is specified default values will be imported from __main_default.init__. 
To ignore/use dedault values within the progrem either use '#' to outcomment the parameter, set it to None or simply delete it
from __main_config.init__.  
The first parameter that needs to be specific is *Importdir*.
````
Importdir = /Home/Folder/Data, /Home/Folder/Background
or
Importdir = /Home/Folder/Data
````
All '.tif' files within these two directories will be imported. The first specified directory is data of interest while 
the second is background data. It is not necesary to specify a background directory, hence no background will be subtracted
from the data.    
The second parameters is the *Outputdir*.
````angular2
Outputdir = /Home/Folder
```` 
This is the directory where the __project folder__ will be created. The __project folder__ will be named after 
the parameter _Stemname_ and is where all generated data and used configurations are saved.   
The calibration and mask file is specified through the parameters _Calibrationconfig_ and _Mask_.  
The 


## The GUI

![GUI example](./img/gui.png)

## Argparse


## Author
* __Emil T. S. Kjær__, PhD student in Nanoscience at the University of Copenhagen   
* suporvisor __Kirsten M. Ø. Jensen__, associate professor at the University og Copenhagen.  
 
Should there be any question, desired improvement or bugs please contact me on GitHub or 
through my email __etsk@chem.ku.dk__.

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## References 
1. Ashiotis, G., Deschildre, A., Nawaz, Z., Wright, J. P., Karkoulis, D., Picca, F. E. & Kieffer, J. (2015). J. Appl. Cryst. 48, 510-519.
2. Juhas, P., Davis, T., Farrow, C. L. & Billinge, S. J. L. (2013). J. Appl. Cryst. 46, 560-566.
3. Hammersley, A. P. (2016). J. Appl. Cryst. 49, 646-652.
4. Clemens Prescher & Vitali B. Prakapenka (2015). High Pressure Research, 35:3, 223-230
