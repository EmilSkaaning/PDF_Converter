import os
import time
import errno
import pickle
import configparser
import h5py
import heapq
import sys
import ast
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt

from prompter import yesno
from tqdm import tqdm
from diffpy.pdfgetx import PDFGetter, loadPDFConfig, findfiles
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

import matplotlib

plt.style.use('ggplot')
colorcycle = plt.rcParams['axes.prop_cycle'].by_key()['color']

LINE_SIZE   = 4
MARKER_SIZE = 10
SMALL_SIZE  = 18
MEDIUM_SIZE = 20
BIGGER_SIZE = 35
FIGSIZE = (12,9)

matplotlib.rcParams['font.family'] = "Arial"
plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=BIGGER_SIZE)    # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('xtick.major', width=LINE_SIZE/2, size=LINE_SIZE)    # x ticks and size
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick.major', width=LINE_SIZE/2, size=LINE_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title
plt.rc('figure', figsize=FIGSIZE)
plt.rcParams['lines.linewidth'] = LINE_SIZE  # fontsize of the figure title
plt.rcParams['lines.markersize'] = MARKER_SIZE  # fontsize of the figure title
matplotlib.rcParams['font.family'] = "Arial"


def load_cfg(self):
    """
    """

    ph = os.listdir(self.root)  # Files ph
    cfgph = [item for item in ph if item[-3:]=='cfg']  # Find cfg file
    try:
        self.cfg = loadPDFConfig(cfgph[0])
    except:
        self.createCFG()
        self.cfg = loadPDFConfig('{}.cfg'.format(self.stem))
    return None

def load_data(self):
    """
    """

    if self.importdir != 'None':  # Importdir is for integrations while datadir is for subtraction
        self.datadir = self.outputdir+'/'+self.stem+'/'+'Integrated'

    datalist = os.listdir(self.datadir)
    
    if len(datalist) > 1:
        datalist = sorted(datalist)  # XXX should be sorted

        datalist = [data for data in datalist if data[0] != '.']  # Removes hidden files
    elif datalist[0] == '.':
        print('\nNo files in data directory!')
        os.exit()
    else:
        pass

    if self.bgdir != 'None':
        bglist = os.listdir(self.bgdir)
        if len(bglist) > 1:
            bglist = sorted(bglist)  # Sort list
            bglist = [data for data in bglist if data[0] != '.']  # Removes hidden files
        elif bglist[0] == '.':
            print('\nNo files in data directory!')
            os.exit()
        else:
            pass

    print("\nLoading data: {}".format(self.datadir))
    x,y = _importdata(self.datadir,datalist)
    y = np.asarray(y)

    if self.bgdir != 'None':
        print("\nLoading backgrounds: {}".format(self.bgdir))
        x_bg,y_bg =_importdata(self.bgdir,bglist)
        y_bg = np.asarray(y_bg)
        if len(y_bg) < len(y):  # If there are more data than bg
            print('\nExtending background matrix:')
            y_bg_ph = np.zeros((len(y),len(y[0])))

            for i in range(len(y)):
                if i >= len(y_bg):
                    y_bg_ph[i] = y_bg[-1]
                else:
                    y_bg_ph[i] = y_bg[i]
            y_bg = y_bg_ph
        elif len(y_bg) > len(y):  # More bg than data XXX
            pass
        else:  # Same amount
            pass
        
    else:
        x_bg = x
        y_bg = y*0

    return x,y,x_bg,y_bg


def _importdata(dir, vals):
    """
    """

    y_vals = []
    skip = 0
    
    for i in tqdm(range(len(vals))):
        while True:
            try:
                frame_data = np.loadtxt(dir+'/'+vals[i],skiprows=skip)
                if i == 0:
                    x_val=frame_data[:,0]
                y_vals.append(frame_data[:,1])
                break
            except:
                skip += 1
       
    return x_val, y_vals


def backgroundSingleAuto(x,y,x_bg,y_bg,qmin,qmax):
    """
    """

    scale = 9999
    print('\nCalculating scaling factor:')
    for li1, li2 in tqdm(zip(y, y_bg)):

        diff_index = [] + heapq.nsmallest(len(li1), range(len(li1)), key=lambda i: ((li1[i] - li2[i])/(li1[i]+0.0000001)))  # Finds index for largest difference

        scan_ph = 1  # Search til it finds a value within qmin and qmax
        i       = 0 
        while scan_ph == 1:

            if qmin < x[diff_index[i]] and qmax > x[diff_index[i]] and li1[diff_index[i]] != 0:
                scale_ph = (li1[diff_index[i]] / li2[diff_index[i]]) * 0.99  # Scales the background a bit further down
                scan_ph = 0
            else:
                i += 1

        if scale_ph < scale:
            scale = scale_ph


    if scale < 0:
        scale = 0
        print('\nOne frame contains only zeros.')
        print('Use auto scate to finde frame or delete last frame and recalculate single-scaling.')

    print('\nScaling factor = {:.3f}'.format(scale))
   
    y_diff = np.multiply(y, scale)
    scale = np.zeros((len(y))) + scale

    return y_diff, scale


def backgroundMultiAuto(x,y,x_bg,y_bg, qmin, qmax):
    '''
    Auto scaling for each frame must be implemented here.
    A plot over the scaling factor should be produced, so that the user can see if unnatural jumps occur
    '''

    count = 0
    scale_list = []
    for li1, li2 in zip(y, y_bg):

        scale = 0
        diff_index = [] + heapq.nsmallest(len(li1), range(len(li1)), key=lambda i: ((li1[i] - li2[i])/(li1[i]+0.00001)))  # Finds index for largest difference between li1 and li2
        scan_ph = 1  # Search til it finds a value within qmin and qmax
        i       = 0 
        while scan_ph == 1:
            if qmin < x[diff_index[i]] and qmax > x[diff_index[i]] and li1[diff_index[i]] != 0:
                scale = (li1[diff_index[i]] / li2[diff_index[i]]) * 0.99  # Scales the background a bit further down
                scan_ph = 0
            
            i += 1
        scale_list.append(scale)
        count += 1

    y_diff = np.zeros((len(y), len(y[0])))
    scaled_bg = np.zeros((len(y), len(y[0])))
    for i in range(len(scale_list)):
        scaled_bg[i] = y_bg[i] * scale_list[i] 
        y_diff[i] = y[i] - scaled_bg[i]

    y_diff = np.array(y_diff)
    scale_list = np.array(scale_list)

    return y_diff, scale_list       



def writePDF(self, x,y_diff,info):
    """
    """
    if info[0] == True:
        if not os.path.exists(self.outputdir+'/'+self.stem+'/'+'Iq'):  # Create integrations folder
            os.makedirs(self.outputdir+'/'+self.stem+'/'+'Iq')
    if info[1] == True:
        if not os.path.exists(self.outputdir+'/'+self.stem+'/'+'Sq'):  # Create integrations folder
            os.makedirs(self.outputdir+'/'+self.stem+'/'+'Sq')
    if info[2] == True:
        if not os.path.exists(self.outputdir+'/'+self.stem+'/'+'Fq'):  # Create integrations folder
            os.makedirs(self.outputdir+'/'+self.stem+'/'+'Fq')
    if info[3] == True:
        if not os.path.exists(self.outputdir+'/'+self.stem+'/'+'Gr'):  # Create integrations folder
            os.makedirs(self.outputdir+'/'+self.stem+'/'+'Gr')


    head_name = ['# Qmax = {}'.format(self.cfg.qmax)]
    head_vals = ['']
    header     = np.column_stack((head_name, head_vals))
    pg = PDFGetter(config=self.cfg)

    print('\nWritting specified files:') 
    for i in tqdm(range(len(y_diff))):
        data_gr = pg(x, y_diff[i]) 
        if info[0] == True:
            saving_dat = np.column_stack((pg.iq[0],pg.iq[1])) 
            saveThis = (np.vstack(((header).astype(str), (saving_dat).astype(str))))
            np.savetxt(self.outputdir+'/'+self.stem+'/'+'Iq/{}_{:05d}.iq'.format(self.stem,i), saveThis, fmt='%s')
        if info[1] == True:
            saving_dat = np.column_stack((pg.sq[0],pg.sq[1])) 
            saveThis = (np.vstack(((header).astype(str), (saving_dat).astype(str))))
            np.savetxt(self.outputdir+'/'+self.stem+'/'+'Sq/{}_{:05d}.sq'.format(self.stem,i), saveThis, fmt='%s')
        if info[2] == True:
            saving_dat = np.column_stack((pg.fq[0],pg.fq[1])) 
            saveThis = (np.vstack(((header).astype(str), (saving_dat).astype(str))))
            np.savetxt(self.outputdir+'/'+self.stem+'/'+'Fq/{}_{:05d}.fq'.format(self.stem,i), saveThis, fmt='%s')
        if info[3] == True:
            saving_dat = np.column_stack((pg.gr[0],pg.gr[1])) 
            saveThis = (np.vstack(((header).astype(str), (saving_dat).astype(str))))
            np.savetxt(self.outputdir+'/'+self.stem+'/'+'Gr/{}_{:05d}.gr'.format(self.stem,i), saveThis, fmt='%s')

    return None


def tempPDFcalc(self,x,y_diff,cfg=None):
    if cfg == None:
        pg = PDFGetter(config=self.cfg)
    else:
        pg = PDFGetter(config=cfg)
    iqMat = []
    fqMat = []
    grMat = []
    for i in tqdm(range(len(y_diff))):
        try:
            pg(x, y_diff[i])
        except:
            pg(x, y_diff[0][i])
        if i == 0:
            qGrid = pg.fq[0]
            rGrid = pg.gr[0]

        iqMat.append(pg.iq[1])
        fqMat.append(pg.fq[1])
        grMat.append(pg.gr[1])

    iqMat = np.asarray(iqMat)
    fqMat = np.asarray(fqMat)
    grMat = np.asarray(grMat)

    return qGrid, iqMat, fqMat, rGrid, grMat, pg
        

def normData(x,y,point):
    closeVal = min(x, key=lambda x:abs(x-point))  # Finds closest element to x
    where = np.where(x == closeVal)  # Finds index
    ph_y = np.asarray((len(y),len(y[0])))
    for ydata in y:
        ph_y = ydata / ydata[where]

    return y


def insituPlot(x,y,thisDir,unit='AA',colormap='magma'):  # viridis

    plt.rc('axes', labelsize=MEDIUM_SIZE+5)    # fontsize of the x and y labels
    plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
    plt.rc('xtick.major', width=LINE_SIZE/2, size=LINE_SIZE)    # x ticks and size
    plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
    plt.rc('ytick.major', width=LINE_SIZE/2, size=LINE_SIZE)    # fontsize of the tick labels

    frame = np.arange(1,len(y)+1)
    fig, ax = plt.subplots()
    cmap = plt.get_cmap(colormap)
    X, Y = np.meshgrid(x, frame)
    Z = (y)
    thisPlot = plt.pcolormesh(X, Y, Z, cmap=cmap) 

    plt.ylabel('Frame')
    if unit=='AA':
        plt.xlabel('r [$\AA$]')
        name='insitu_Gr.png'
    elif unit=='nm':
        pass
    elif unit=='A^-1':
        plt.xlabel('q [$\AA^{-1}$]')
        name='insitu_Fq.png'

    maxVal = y[np.unravel_index(y.argmax(), y.shape)]
    minVal = y[np.unravel_index(y.argmin(), y.shape)]
    
    if abs(maxVal) >= abs(minVal):  # Findes largest abs value
        absVal = abs(maxVal)
    else: 
        absVal = abs(minVal)

    cbar = plt.colorbar(thisPlot,ticks=[0],aspect=10)

    cbar.set_ticklabels(['Zero'])  # vertically oriented colorbar
    plt.tick_params(axis='x')
    plt.tick_params(axis='y')
    plt.tight_layout(rect=(0,0,1.08,1))
    os.chdir(thisDir)
    plt.savefig(name, format='png', dpi=300)

    return None


def correlationPlot(data,thisDir,colormap='magma'):
    plt.rc('axes', labelsize=MEDIUM_SIZE+5)    # fontsize of the x and y labels
    plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
    plt.rc('xtick.major', width=LINE_SIZE/2, size=LINE_SIZE)    # x ticks and size
    plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
    plt.rc('ytick.major', width=LINE_SIZE/2, size=LINE_SIZE)    # fontsize of the tick labels

    test = []
    for i in range(len(data)):
        for j in range(len(data)):
            ph, _ = stats.pearsonr(data[i], data[j]) 
            test.append(ph)  
    
    frame = np.arange(1,len(data)+1)
    fig, ax = plt.subplots(figsize=(12,10))
    cmap = plt.get_cmap(colormap)
    X, Y = np.meshgrid(frame, frame)
    test = np.array(test).reshape((len(data), len(data)))
    Z = test
    thisPlot = plt.pcolormesh(X, Y, Z, cmap=cmap,vmin=-1, vmax=1) 
    plt.ylabel('Frame')
    plt.xlabel('Frame')
    cbar = plt.colorbar(aspect=10)
    plt.tick_params(axis='x')
    plt.tick_params(axis='y')
    plt.tight_layout(rect=(0,0,0.98,1))
    os.chdir(thisDir)
    plt.savefig('FrameCorrelation.png', format='png', dpi=300)

    return None


def datareduction(self):
    """
    """
    from _DRGUI import DRinterface
    x,y,_,y_bg=load_data(self)
    raw_y = y 
    raw_y_bg = y_bg
    load_cfg(self)

    y = normData(x,y, self.cfg.qmax)
    y_bg = normData(x,y_bg, self.cfg.qmax)

    if self.bgdir != 'None':
        if self.subtract == 0:
            y_diff, scale_list = backgroundSingleAuto(x,y,x,y_bg, self.cfg.qmin, self.cfg.qmax)
        elif self.subtract == 1:
            y_diff, scale_list = backgroundMultiAuto(x,y,x,y_bg, self.cfg.qmin, self.cfg.qmax)
        elif self.subtract == 2:
            pass
        elif self.subtract == 3:
            pass
    else:
        sys.exit()
        pass
        #calcPDF(self, x, y)


    qGrid, iqMat, fqMat, rGrid, grMat, pg = tempPDFcalc(self,x,y_diff)

    runGUI = DRinterface(x, y, y_bg, y_diff, qGrid, fqMat, rGrid, grMat, scale_list, self.cfg, raw_y, raw_y_bg,self.subtract)
    self.cfg=runGUI.cfg  # Updates cfg between the two objects
    self.overwriteCFG(runGUI) 
    correlationPlot(runGUI.gr,self.outputdir+'/'+self.stem+'/')
    writePDF(self,runGUI.qGrid,runGUI.iq_diff,runGUI.checkBoxFunc())
    if runGUI.checkBoxFunc()[3]==True:
        insituPlot(runGUI.rGrid,runGUI.gr,self.outputdir+'/'+self.stem+'/')
    if runGUI.checkBoxFunc()[2]==True:
        insituPlot(runGUI.fqGrid,runGUI.fq,self.outputdir+'/'+self.stem+'/',unit='A^-1')


    return self.cfg.qmin, self.cfg.qmax


