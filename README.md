# Pair Distribution Function converter
## Introduction
This code was developed as part of my M.Sc. thesis at the University of Copenhagen and is ment to improve data
analysis of x-ray data. More specifical to improve data analysis of _in situ_ measurements using the Pair 
Distribution Function (PDF).   
This simple program is ment to easy the workload of preprocessing the data before modelling is preformed and to
help the user keep track of all used parameters. This framework is build using:
 
* [PyFAI](https://pyfai.readthedocs.io/en/latest/)<sup>[1](#references)</sup>
* [PDfgetX3](https://www.diffpy.org/products/pdfgetx.html)<sup>[2](#references)</sup>

Calibration and integration is implemented using PyFAI. Since what program to use for these tasks are 
an almost religous question, PyFAI was chosen as it supports the most used ones:  
[Fit2D](http://www.esrf.eu/computing/scientific/FIT2D/)<sup>[3](#references)</sup> and 
[Dioptas](http://www.clemensprescher.com/programs/dioptas)<sup>[4](#references)</sup>. 
PyFAI can load both calibration and mask files from either of those programs while still having its own framework for
handling these tasks. This flexibility made it the obivois choise.     
The two following sections will provide a simple guide to installing and running the program. 
A more complete guide for installing, _how to use_ examples and implementation 
can be found in [PDFconverter_manual.pdf](PDFconverter_manual.pdf).
## Installing
For running this program i recommend using Python 3.7 but it should be compatible down to Python 3.4. If you do not have 
Python installed the easiest way is to install [Anaconda](https://www.anaconda.com/distribution/#windows). Remember to 
add Anaconda to you path when installing it. To verify that python has been installed correctly open your terminal and
type _python --version_, if this does not produce an error then you have installed Python correctly! An example is 
shown below
```
python --version
>>> Python 3.7.4
```
The "hardest" packages to install for this program to work are PyFAI and PDFgetX3. I recommend reading their following 
installation guides, for getting help installing PyFAI [press here](https://pyfai.readthedocs.io/en/latest/operations/index.html#detailed-installation-procedure-on-different-operating-system)
and for PDFgetX3 [press here](https://www.diffpy.org/doc/pdfgetx/2.0.0/install.html). Remember to chose to right operating system!
When these packages are correctly installed then you are practically done, all of the remining packages can simply be
installed using either Anaconda or pip. Unfortunately, the simplest way to install all packages is to run the program
and install the missing package when it gives an error. Examples are shown below.
````
pip install tqdm

conda install tqdm
````
The number of packages needed to run this program depend on how you chose to install Python.
   

## Running Example
This program has three core functions: calibration, integration and background subtraction. 

![GUI example](./img/gui.png )
Center-aligned
{: .text-center}

## Author
* __Emil T. K. Kjær__, PhD student in Nanoscience at the University of Copenhagen   
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
