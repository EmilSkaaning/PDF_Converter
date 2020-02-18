# Pair Distribution Function converter
## Introduction
This code was developed as part of my M.Sc. thesis at the University of Copenhagen and is ment to improve data
analysis of x-ray data. More specifical to improve data analysis of _in situ_ measurements using the Pair 
Distribution Function (PDF).   
This simple program is ment to easy the workload of preprocessing the data before modelling is preformed and to
help the user keep track of all used parameters. This framework is build using:
 
* [PyFAI](https://pyfai.readthedocs.io/en/latest/)<sup>[1](#references)</sup>
* [PDfgetX3](https://www.diffpy.org/products/pdfgetx.html)

PyFAI is mainly used for integration, since there are several good calibration and masking tools such as 
[Fit2D](http://www.esrf.eu/computing/scientific/FIT2D/) and [Dioptas](http://www.clemensprescher.com/programs/dioptas). 
PyFAI can load both calibration and mask files from either of those programs. To calculate the PDFs from the integrated
scattering patterns  

## Installing

A more complete guide for installation and _how to use_ examples can be found in [PDFconverter_manual.pdf](PDFconverter_manual.pdf).

## Example

![GUI example](./img/gui.png)


## Author
Should there be any question, desired improvement or bugs please contact me.


## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## References 







