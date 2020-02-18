from configparser import ConfigParser
import os
import pyFAI, pyFAI.detectors
import fabio, subprocess
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import sys
import shutil
from diffpy.pdfgetx import PDFGetter, loadPDFConfig, findfiles
import argparse


sys.path.append(os.getcwd()+'/Subfolder')

class initProgram:
    """
    Calling the program/class.
    """

    import _DataReduction as dr
    import _DRGUI as GUI

    def __init__(self):
        """
        Structure of the program.
        
        Parameters:
        -----------
            None

        Return:
        -------
            None
        """

        self.root = os.getcwd()  #Defines root. Always return to this
        self.parser()  # Imports config

        if self.importdir != 'None' and self.stem != 'None':
            if not os.path.exists(self.outputdir+'/'+self.stem):  # Creates project folder
                os.makedirs(self.outputdir+'/'+self.stem)
            print('\nDoing integration!')
            self.integrate()  # Calls integrate
            self.configFolder(self.calconfig)
            self.configFolder(self.mask)
            if self.importdir_bg != 'None':  # Updates where the integrated bg files are located
                self.bgdir = self.outputdir+'/'+self.stem+'/'+'Integrated_bg'

        if self.datadir != 'None' and self.bgdir != 'None':
            print('\nDoing Data Reduction!')
            self.qmin, self.qmax = self.dr.datareduction(self)  # Calls data reduction module
            self.configFolder('{}.cfg'.format(self.stem))

        self.configFolder('main_config.init')
        print('\nThank you for converting to PDF\n')


    def createCFG(self):
        config = ConfigParser()  # Setting up the config files
        config.read(self.root+'/Subfolder/main_default.init')  # If var is not in config then default var is used
        config.read(self.root+'/main_config.init')  # User settings

        # [PDFgetX3]
        print("\nCreating .cfg file for PDFgetX3!")
        cfg_name    = '{}.cfg'.format(self.stem)
        dataformat  = config.get('PDFgetX3', 'dataformat')
        outputtypes = config.get('PDFgetX3', 'outputtypes')
        composition = config.get('PDFgetX3', 'composition')
        qmaxinst    = config.get('PDFgetX3', 'qmaxinst')
        qmin        = config.get('PDFgetX3', 'qmin')
        qmax        = config.get('PDFgetX3', 'qmax')
        rmin        = config.get('PDFgetX3', 'rmin')
        rmax        = config.get('PDFgetX3', 'rmax')
        rstep       = config.get('PDFgetX3', 'rstep')
        rpoly       = config.get('PDFgetX3', 'rpoly')
        
        NAMES  = np.array(['dataformat', 'outputtypes', 'composition', 'qmaxinst', 'qmin', 'qmax', 'rmin', 'rmax', 'rstep', 'rpoly'])
        FLOATS = np.array([dataformat, outputtypes, composition, qmaxinst, qmin, qmax, rmin, rmax, rstep, rpoly])
        DAT =  np.column_stack((NAMES, FLOATS))
        np.savetxt(cfg_name, DAT, delimiter=" = ", header='[DEFAULT]',comments='', fmt="%s") 
        print('\nNew cfg file has been created')


    def overwriteCFG(self,obj):
        # [PDFgetX3]
        print("\nOverwriting .cfg file!")
        cfg_name    = '{}.cfg'.format(self.stem)
        dataformat  = obj.cfg.dataformat
        outputtypes = 'iq, sq, fq, gr'
        composition = obj.cfg.composition
        qmaxinst    = obj.cfg.qmaxinst
        qmin        = obj.cfg.qmin
        qmax        = obj.cfg.qmax
        rmin        = obj.cfg.rmin
        rmax        = obj.cfg.rmax
        rstep       = obj.cfg.rstep
        rpoly       = obj.cfg.rpoly
        
        NAMES  = np.array(['dataformat', 'outputtypes', 'composition', 'qmaxinst', 'qmin', 'qmax', 'rmin', 'rmax', 'rstep', 'rpoly'])
        FLOATS = np.array([dataformat, outputtypes, composition, qmaxinst, qmin, qmax, rmin, rmax, rstep, rpoly])
        DAT =  np.column_stack((NAMES, FLOATS))
        np.savetxt(cfg_name, DAT, delimiter=" = ", header='[DEFAULT]',comments='', fmt="%s") 

        return None


    def configFolder(self, copy):
        """
        Copies files to the Config folder. Creates the folder if it does not exist.

        Parameters:
        -----------
            copy : str() name of file being copied.

        Return:
        -------
            None
        """

        if not os.path.exists(self.outputdir+'/'+self.stem+'/Configs'):  # Creates project folder
            os.makedirs(self.outputdir+'/'+self.stem+'/Configs')
        try:
            shutil.copy2(self.root+'/'+copy, self.outputdir+'/'+self.stem+'/Configs/'+copy)
        except:
            pass

        return None

    def parser(self):
        """
        Reads the config files.

        Parameters:
        -----------
            None

        Return:
        -------
            None
        """

        config = ConfigParser()  # Setting up the config files
        config.read(self.root+'/Subfolder/main_default.init')  # If var is not in config then default var is used
        config.read(self.root+'/main_config.init')  # User settings

        # [Calibration and Integration]
        ph = config.get('Calibration and Integration', 'Importdir')  # Dir for data to be imported. If none Calibration and Integration is skiped
        try:
            self.importdir,self.importdir_bg=ph.split(', ')
        except:
            self.importdir = ph
            self.importdir_bg = None
        
        self.outputdir = config.get('Calibration and Integration', 'Outputdir')  # Where should the project-folder be saved
        self.stem = config.get('Calibration and Integration', 'Stemname')  # Stem name of all produced files. Bg files can have another name
        self.calconfig = config.get('Calibration and Integration', 'Calibrationconfig')  # Import poni og fit2d calibration file, pyfai calib need implementation
        self.mask = config.get('Calibration and Integration', 'Mask')  # Name of the mask

        self.points = config.getint('Calibration and Integration', 'Points')  # Number of data points after integration
        self.correctSolidAngle = config.getboolean('Calibration and Integration', 'CorrectSolidAngle')  # Decrease intensity as a function of q if True
        self.units = config.get('Calibration and Integration', 'Unit')  # q_A^-1 or q_nm^-1, q_nm^-1 is not tested yet
        self.filetype = config.get('Calibration and Integration', 'Filetype')  # Exstension of the data

        # [Data Reduction]
        self.datadir = config.get('Data Reduction', 'Datadir')  # Dir for loaded data files.
        self.bgdir = config.get('Data Reduction', 'Bgdir')  # Dir for loaded bg files. If None it treates data as bg files
        self.bgname = config.get('Data Reduction', 'Bgname')  # Stem of bg files, if None self.stem + '_bg' is used
        self.subtract = config.getint('Data Reduction', 'Subtract')  # How the bg subtraction is done

        if self.bgname == 'None':
            self.bgname = self.stem+'_bg'
        return None        


    def integrate(self):
        """
        Integrates defined data as specified within the config file.

        Parameters:
        -----------
            None

        Return:
        -------
            None
        """



        if self.calconfig[-5:].upper() == 'FIT2D':  # Load Fit2D config
            config = ConfigParser()
            config.read(self.root+'/calibration.fit2d')
            self.directDist = config.getfloat('Calibration Fit2D', 'directDist')
            self.centerX = config.getfloat('Calibration Fit2D', 'centerX')
            self.centerY = config.getfloat('Calibration Fit2D', 'centerY')
            self.tilt = config.getfloat('Calibration Fit2D', 'tilt')
            self.tiltPlanRotation = config.getfloat('Calibration Fit2D', 'tiltPlanRotation')
            self.pixelX = config.getfloat('Calibration Fit2D', 'pixelX')
            self.pixelY = config.getfloat('Calibration Fit2D', 'pixelY')
            self.wavelength = config.getfloat('Calibration Fit2D', 'wavelength')

            ai = pyFAI.AzimuthalIntegrator(wavelength=self.wavelength)            
            ai.setFit2D(self.directDist, self.centerX, self.centerY, tilt=self.tilt,
                        tiltPlanRotation=self.tiltPlanRotation, pixelX=self.pixelX, pixelY=self.pixelY) 

        elif self.calconfig[-4:].upper() == 'PONI':  # Load Dioptas poni
            ai = pyFAI.AzimuthalIntegrator()
            ai = pyFAI.load(self.calconfig)

        if self.mask != 'None':  # Loads mask
            mask = fabio.open(self.root+'/'+self.mask).data
       
            
        # Integrates data
        if not os.path.exists(self.outputdir+'/'+self.stem+'/'+'Integrated'):  # Create integrations folder
            os.makedirs(self.outputdir+'/'+self.stem+'/'+'Integrated')
        os.chdir(self.outputdir+'/'+self.stem+'/'+'Integrated')  # Goes to project folder
        
        data = os.listdir(self.importdir)  # Gets all files in folder
        dataList = [file for file in data if file[-4:].upper() == '.{}'.format(self.filetype.upper())]  # Removes everything but tif
        dataList = [file for file in dataList if 'test' not in file]  # Removes test files
        dataList = [file for file in dataList if 'dark' not in file]  # Removes dark files
        dataList = sorted(dataList)
        pbar = tqdm(total=len(dataList))
        for i, data in enumerate(dataList):
            pbar.set_description("Integrating: %s" % data)
            img = np.flipud(fabio.open(self.importdir+'/'+data).data)  # Tif files are flipped
            if self.mask == 'None':  # Loads mask
                res = ai.integrate1d(img, self.points, filename='{}_{:05d}.dat'.format(self.stem,i), 
                     correctSolidAngle=self.correctSolidAngle, mask=None, unit=self.units)
            else:
                res = ai.integrate1d(img, self.points, filename='{}_{:05d}.dat'.format(self.stem,i), 
                                 correctSolidAngle=self.correctSolidAngle, mask=mask, unit=self.units)
            pbar.update(1)
        pbar.close()

        # Integrates background
        if self.importdir_bg != 'None':

            if not os.path.exists(self.outputdir+'/'+self.stem+'/'+'Integrated_bg'):  # Create integrations folder
                os.makedirs(self.outputdir+'/'+self.stem+'/'+'Integrated_bg')    
            os.chdir(self.outputdir+'/'+self.stem+'/'+'Integrated_bg')

            data = os.listdir(self.importdir_bg)  # Gets all files in folder
            dataList = [file for file in data if file[-4:].upper() == '.{}'.format(self.filetype.upper())]  # Removes everything but tifs
            dataList = [file for file in dataList if 'test' not in file]  # Removes test files
            dataList = [file for file in dataList if 'dark' not in file]  # Removes dark files
            dataList = sorted(dataList)
            if self.bgname != 'None':
                ph_name = self.bgname
            else: 
                ph_name = self.stem

            pbar = tqdm(total=len(dataList))
            for i, data in enumerate(dataList):
                pbar.set_description("Integrating: %s" % data)
                img = np.flipud(fabio.open(self.importdir_bg+'/'+data).data)  # Tif files are flipped
                if self.mask == 'None':  # Loads mask
                    res = ai.integrate1d(img, self.points, filename='{}_{:05d}.dat'.format(ph_name,i), 
                         correctSolidAngle=self.correctSolidAngle, mask=None, unit=self.units)
                else:
                    res = ai.integrate1d(img, self.points, filename='{}_{:05d}.dat'.format(ph_name,i), 
                                     correctSolidAngle=self.correctSolidAngle, mask=mask, unit=self.units)
                pbar.update(1)
        pbar.close()

        os.chdir(self.root)  # Goes back to root

        # 
        # Implement pyFAI integration
        #

        return None


def argParse():
    """
    Checking for commandos before the program is called. Use the help function to get possible commandos.
    If a commando is added the program will terminate after executing that command. 
    To run structural refinement no commando can be present.

    Parameters:
    -----------
        None

    Return:
    -------
        None
    """


    parser = argparse.ArgumentParser(prog='NanostructureUCPH')
    parser.add_argument("-c", "--create", help="Create can take 4 different input or a combination of the 4.\nfit2D, search, cfg or main.")  # Defines new command
    args = parser.parse_args()  # Get commands
    
    if args.create != None:

        if 'FIT2D' in args.create.upper():  # Checks if command is defined
            print("Creating .Fit2D calibration file!")
            Fit2D_name    = 'new.fit2D'
    
            directDist = None 
            centerX = None 
            centerY = None 
            tilt = None 
            tiltPlanRotation = None 
            pixelX = None 
            pixelY = None 
            wavelength = None 

            NAMES  = np.array(['pixelX', 'pixelY', 'wavelength', 'directDist', 'centerX', 'centerY', 'tilt', 'tiltPlanRotation'])
            FLOATS = np.array([pixelX, pixelY, wavelength, directDist, centerX, centerY, tilt, tiltPlanRotation])
            DAT =  np.column_stack((NAMES, FLOATS))
            np.savetxt(Fit2D_name, DAT, delimiter=" = ", header='[Calibration Fit2D]',comments='', fmt="%s") 
            print('\nNew cfg file has been created')

        if 'SEARCH' in args.create.upper():  # Checks if command is defined
            print("\nCreating config file for specified database search!")

        if 'CFG' in args.create.upper():  # Checks if command is defined
            print("\nCreating .cfg file for PDFgetX3!")
            cfg_name    = 'new.cfg'
            dataformat  = 'QA'
            outputtypes = 'iq, sq, fq, gr'
            composition = 'H2 O'
            qmaxinst    = 25
            qmin        = 0.7
            qmax        = 20.0
            rmin        = 0.0
            rmax        = 30.0
            rstep       = 0.01
            rpoly       = 0.9
            
            NAMES  = np.array(['dataformat', 'outputtypes', 'composition', 'qmaxinst', 'qmin', 'qmax', 'rmin', 'rmax', 'rstep', 'rpoly'])
            FLOATS = np.array([dataformat, outputtypes, composition, qmaxinst, qmin, qmax, rmin, rmax, rstep, rpoly])
            DAT =  np.column_stack((NAMES, FLOATS))
            np.savetxt(cfg_name, DAT, delimiter=" = ", header='[DEFAULT]',comments='', fmt="%s") 
            print('\nNew cfg file has been created')

        if 'MAIN' in args.create.upper():  # Checks if command is defined
            print("\nCreating main_config.init file!")

    else:
        obj = initProgram()


if __name__ =='__main__':
    argParse()
