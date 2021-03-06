# Pair Distribution Function Converter
## Introduction
This code was developed as part of my M.Sc. thesis at the University of Copenhagen and is meant to improve data
analysis of x-ray data. More specifical to improve data analysis of _in situ_ measurements using the Pair 
Distribution Function (PDF).   
This simple program is meant to ease the workload of preprocessing the data before modeling is preformed and to
help the user keep track of all used parameters making data reproducible.   
This framework is built using the following two packages:
 
* [PyFAI](https://pyfai.readthedocs.io/en/latest/)<sup>[1](#references)</sup>
* [PDfgetX3](https://www.diffpy.org/products/pdfgetx.html)<sup>[2](#references)</sup>

Calibration and integration is implemented using PyFAI. What program to use for these tasks are 
an almost religous question, PyFAI was chosen as it supports the most used ones:  
[Fit2D](http://www.esrf.eu/computing/scientific/FIT2D/)<sup>[3](#references)</sup> and 
[Dioptas](http://www.clemensprescher.com/programs/dioptas)<sup>[4](#references)</sup>. 
PyFAI can load both calibration and mask files from either of those programs while still having its own framework for
handling these tasks. This flexibility made it the obvious choice.     
The two following sections will provide a simple guide to installing and running the program. 
A more complete guide for installing, how to use examples and implementation can be found in 
[PDFconverter_manual.pdf](PDFconverter_manual.pdf).  
The __README.md__ file consist of the following sections:

1. [Installing PDF Converter](#Installing-pdf-converter)
2. [Running the code](#running-the-code)
3. [The GUI](#the-gui)
4. [Argparse](#argparse)
5. [License](#license)
6. [Author](#author)
7. [References](#references)

## Installing PDF Converter
For running this program I recommend using Python 3.7 but it is compatible down to Python 3.4. If you do not have 
Python installed the easiest way is to install [Anaconda](https://www.anaconda.com/distribution/#windows). Remember to 
add Anaconda to your path when installing it. To verify that python has been installed correctly after installing Anaconda
open your terminal and type _python --version_, if this does not produce an error then you
have installed Python correctly!
```
python --version
>>> Python 3.7.4
```
The "hardest" packages to install for this program are PyFAI and PDFgetX3. I recommend reading their
installation guides on their homapages, for getting help installing
PyFAI [press here](https://pyfai.readthedocs.io/en/latest/operations/index.html#detailed-installation-procedure-on-different-operating-system)
and for PDFgetX3 [press here](https://www.diffpy.org/doc/pdfgetx/2.0.0/install.html). Remember to choose the right operating system!
When these packages are correctly installed then you are practically done, all of the remaining packages can simply be
installed using either Anaconda or pip, which ever you prefer. Remember only to install the needed packages with either 
of them and not both of them, as it will confuse Python! 
````
pip install tqdm
or
conda install tqdm
````
Unfortunately, the simplest way to install the remaining packages, 
is to run the program and install the missing packages when the following error is produced:
````
>>> Traceback (most recent call last):
>>>   File "<stdin>", line 1, in <module>
>>> ModuleNotFoundError: No module named 'prompter'
````
The number of packages needed to run this program depends on how you chose to install Python. If you chose Anaconda
then you should only have to install 2-3 additional packages.

## Running the code
This program has three core functions: calibration, integration and background subtraction. It is so far
recommended to use Fit2D for calibration.  
The __main_config.init__ is used to configure the program. To run only the program only three parameters are needed,
*Importdir*, *Outputdir* and *Calibrationconfig*. If nothing else is specified default values will be imported from __main_default.init__. 
To ignore/use default values within the program either use '#' at the beginning of the line, set the variable to None or simply delete it
from __main_config.init__.  
The first parameter that needs to be specific is *Importdir*.
````
Importdir = /Home/Folder/Data, /Home/Folder/Background
or
Importdir = /Home/Folder/Data
````
All '.tif' files within these two directories will be imported. The first specified directory is data of interest while 
the second is background data. It is not necessary to specify a background directory, hence no background will be subtracted
from the data.    
The second parameter is the *Outputdir* variable.
````angular2
Outputdir = /Home/Folder
```` 
This is the directory where the __project folder__ will be created. The __project folder__ will be named after 
the parameter _Stemname_ and is where all generated data and used configurations are saved.   
The calibration and mask file is specified through the parameters _Calibrationconfig_ and _Mask_.


## The GUI
To get a better overview of how background subtraction and change in parameters affect the PDFs a simple GUI was implemented.
The GUI consist of 4 different plots, different possibilities for automated background subtraction and easy access to 
the parameters needed for the Fourier Transformation. 

![GUI example](./img/gui.png)

On the left side of the GUI 4 different plots are present and the header shows the current plotted data set and its 
scaling factor. From the top and down I(q), F(q), G(r) and scaling factors as a function of time. By hovering the scaling
plot the 3 top graphs will change to the corresponding timeframe hovered. E.g. This gives the possibility of deciding the best 
Q<sub>max</sub> and to remove unique atom-atom distances from the PDF through the background subtraction.  
The __method box__ is an automatic way of calculating the scaling factor/factors for a large dataset. The different 
methods are explained in the table below. When a method is chosen and __Recalculating scaling__ is pressed, then the
program will calculate the highest possible scaling factor/factors within within the range of Q<sub>min</sub> 
and Q<sub>max</sub>.  
 
| Method | Description |
| :---: | --- |
| __1__ | One scaling factor is calculated |
| __2__ | A scaling factor for each data frame is calculated. |
| __3__ | Not implemented, room for improvement. |
| __4__ | Not implemented, room for improvement. |

All scaling factors can be altered by the __relative scale__, either by giving a float or changing the scale bar. 
The chance is committed by pressing the __Calculate__ button. Furthermore, specific time areas of the data set can be 
adjusted by using the __First__ and __Last__ box and then pressing __Choose frames__. This will mark an area on the 
4<sup>th</sup> plot indicating which frames will have their scaling factors changed by the next __Calculate__. Scaling
factors can also be set to absolute values by using the __Scale__ field and then pressing __Calculate__. To remove
miss selected frames the __Clear__ button can be pressed.  
Parameters such as Q<sub>min</sub>, Q<sub>max</sub>, r<sub>step</sub> etc. determine the range of how the scaling factors
are determined and how the Fourier transformation is done. By pressing __Set q and r range__ the plots will be redrawn.  
In the upper right corner, 4 checkboxes are shown. Here the outputs generated are determined. In the example shown below 
only F(q) and G(r) are save in the __project folder__. 

* [ ] I(q) 
* [ ] S(q)   
* [X] F(q)
* [X] G(r)   

The GUI is closed and outputs are created by pressing __Continue__.
## Argparse
Possible arguments for PDF Converter.

| Arg | Description |
| --- | --- |
| `-h` or `--help` | Prints help message. |
| `-c` or `--create` | Create can take 2 different inputs or a combination of them. <br/> `fit2D` or `cfg` |

The create argument can create two types of files, either a cfg file or a fit2d calibration file. A '.cfg' file is needed 
for PDFgetX3 to specify required parameters for calculating the PDFs. The `fit2D` is a file where calibration configurations
from Fit2D can be store for future calibration.
````angular2
python __init__.py --create fit2d
>>> Creating .Fit2D calibration file!
````
## Author
* __Emil T. S. Kjær__, Ph.D. student in Nanoscience at the University of Copenhagen   
* Supervisor __Kirsten M. Ø. Jensen__, associate professor at the University of Copenhagen.  
 
Should there be any question, desired improvement or bugs please contact me on GitHub or 
through my email __etsk@chem.ku.dk__.

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## References 
1. Ashiotis, G., Deschildre, A., Nawaz, Z., Wright, J. P., Karkoulis, D., Picca, F. E. & Kieffer, J. (2015). J. Appl. Cryst. 48, 510-519.
2. Juhas, P., Davis, T., Farrow, C. L. & Billinge, S. J. L. (2013). J. Appl. Cryst. 46, 560-566.
3. Hammersley, A. P. (2016). J. Appl. Cryst. 49, 646-652.
4. Clemens Prescher & Vitali B. Prakapenka (2015). High Pressure Research, 35:3, 223-230
