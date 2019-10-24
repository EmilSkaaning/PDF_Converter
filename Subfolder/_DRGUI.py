import matplotlib.pyplot as plt
from matplotlib.widgets import Button, CheckButtons, TextBox, RadioButtons
import numpy as np
import matplotlib
import random

from math import floor
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import _DRGUIsetup as gui
from _DataReduction import tempPDFcalc, normData, backgroundSingleAuto, backgroundMultiAuto
plt.style.use('ggplot')
colorcycle = plt.rcParams['axes.prop_cycle'].by_key()['color']

LINE_SIZE   = 2
MARKER_SIZE = 10
SMALL_SIZE  = 10
MEDIUM_SIZE = 12
BIGGER_SIZE = 25
FIGSIZE = (16,8)

matplotlib.rcParams['font.family'] = "Arial"
plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=BIGGER_SIZE)    # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE+3)    # fontsize of the tick labels
plt.rc('xtick.major', width=LINE_SIZE/2, size=LINE_SIZE)    # x ticks and size
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick.major', width=LINE_SIZE/2, size=LINE_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE+4)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title
plt.rc('figure', figsize=FIGSIZE)
plt.rcParams['lines.linewidth'] = LINE_SIZE  # fontsize of the figure title
plt.rcParams['lines.markersize'] = MARKER_SIZE  # fontsize of the figure title



class DRinterface():
    def __init__(self, q, iq_data, iq_bg, iq_diff, fqGrid, fq, r, gr, scale, cfg,raw_y,raw_y_bg,method):
        self.cfg = cfg
        self.method = [True if method == i else False for i in range(4)] # 4 is the number of scaling methods

        self.qGrid = q
        self.fqGrid = fqGrid
        self.rGrid = r
        self.iq_data = iq_data  
        self.iq_bg = iq_bg       
        self.iq_diff = iq_diff   
        self.fq = fq   
        self.gr = gr   
        self.scaleMat = np.asarray(scale)
        self.raw_y = raw_y
        self.raw_y_bg = raw_y_bg

        self.firstFrame = 1
        self.lastFrame = len(self.scaleMat)
        self.scale = 0.99
        self.relScale = 1.
        self.phFrames = False
        self.current_xval = 1

        self.fig, (self.ax4, self.ax3,self.ax2, self.ax1) = plt.subplots(4,1,figsize=FIGSIZE, gridspec_kw={'height_ratios': [15,15,15,4]})

        self.setupax4()
        self.setupax3()
        self.setupax2()
        self.setupax1()

        plt.tight_layout(h_pad=-0.1)
        plt.subplots_adjust(right=0.6)
        
        gui.createButtons(self)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_move)  # Updates canvas
        plt.show()


    def setupax4(self, index=1):
        self.ax4.set_title("Frame {} - Scaling {:.3f}".format(index, self.scaleMat[index-1]))
        self.ax4.plot(self.qGrid,self.iq_data[index-1],label='$Y_{data}$', color=colorcycle[1])
        self.ax4.plot(self.qGrid,self.iq_bg[index-1]*self.scaleMat[index-1],label='$Y_{bg}$', color=colorcycle[0])
        self.ax4.plot(self.qGrid,self.iq_diff[index-1], label='$Y_{diff}$', color=colorcycle[5])

        self.ax4.set_ylabel("I(q) [a.u.]")

        if self.cfg.dataformat == 'QA':
            self.ax4.set_xlabel("q [$\AA^{-1}$]")
            self.ax4.set_xlim(self.cfg.qmin, self.cfg.qmax)
        elif self.cfg.dataformat == 'Qnm':
            self.ax4.set_xlabel("q [$nm^{-1}$]")
            self.ax4.set_xlim(self.cfg.qmin*10, self.cfg.qmax*10)
        self.ax4.set_yticklabels('')
        self.ax4.tick_params(axis='y', which='both', left=False)

        self.ax4.legend(loc='upper right')

        return None


    def setupax3(self, index=1):
        self.ax3.plot(self.fqGrid,self.fq[index-1], color=colorcycle[5])
        self.ax3.set_ylabel("F(q) [a.u.]")
        self.ax3.set_xlabel("q [$\AA^{-1}$]")
        self.ax3.set_yticklabels('')
        self.ax3.tick_params(axis='y', which='both', left=False)

        self.ax3.set_xlabel("q [$\AA^{-1}$]")
        self.ax3.set_xlim(self.cfg.qmin, self.cfg.qmax)


        return None


    def setupax2(self, index=1):
        self.ax2.plot(self.rGrid,self.gr[index-1], color=colorcycle[5])
        self.ax2.set_ylabel("G(r) [a.u.]")
        self.ax2.set_yticklabels('')
        self.ax2.tick_params(axis='y', which='both', left=False)

        self.ax2.set_xlabel("r [$\AA$]")
        self.ax2.set_xlim(self.cfg.rmin, self.cfg.rmax)


        return None


    def setupax1(self):
        self.ax1.plot(np.arange(1,len(self.scaleMat)+1),self.scaleMat, color=colorcycle[5])
        self.ax1.set_ylabel("Scale")
        self.ax1.set_xlabel("Frame")
        self.ax1.set_yticklabels('')
        self.ax1.tick_params(axis='y', which='both', left=False)
        self.ax1.set_xlim(1,len(self.scaleMat))

        return None

 
    def on_move(self,event):  # Hover function, only takes y coordinate into account
        if event.inaxes is self.ax1:
            event_xval = floor(event.xdata)
            id_xval = int(event_xval)

            if id_xval != self.current_xval:
                self.current_xval = id_xval
                self.ax4.cla()
                self.ax3.cla()
                self.ax2.cla()
                self.setupax4(self.current_xval)
                self.setupax3(self.current_xval)
                self.setupax2(self.current_xval)
                self.fig.canvas.draw_idle()

        return None


    def radioBoxFunc(self, input):
        self.method = [True if int(input[-1]) == i+1 else False for i in range(4)]  # 4 is the number of methods

        return None


    def recalc(self, event):
        self.iq_data = normData(self.qGrid,self.raw_y,self.cfg.qmax)
        self.iq_bg = normData(self.qGrid,self.raw_y_bg,self.cfg.qmax)
        
        if self.method[0] == True:
            self.iq_diff, self.scaleMat = backgroundSingleAuto(self.qGrid,self.iq_data,self.qGrid,self.iq_bg, self.cfg.qmin, self.cfg.qmax)
        elif self.method[1] == True:
            self.iq_diff, self.scaleMat = backgroundMultiAuto(self.qGrid,self.iq_data,self.qGrid,self.iq_bg, self.cfg.qmin, self.cfg.qmax)
        elif self.method[2] == True:
            pass
        elif self.method[3] == True:
            pass

        self.ax4.cla()
        self.setupax4(self.current_xval)
        self.ax3.cla()
        self.setupax3(self.current_xval)
        self.ax2.cla()
        self.setupax2(self.current_xval)
        self.ax1.cla()
        self.setupax1()

        return None



    def qminBoxFunc(self,input):
        try:
            input = np.float(input)
            if input < 0 or input >= self.cfg.qmax:
                self.qminBox.set_val(self.cfg.qmin)
            else:
                self.qminBox.set_val(input)
                self.cfg.qmin = input
        except:
            print('Input must be positive float.')
            self.qminBox.set_val(self.cfg.qmin)

        return None
        

    def qmaxBoxFunc(self,input):
        try:
            input = np.float(input)
            if input < 0 or input <= self.cfg.qmin:  
                self.qmaxBox.set_val(self.cfg.qmax)
            else:
                self.qmaxBox.set_val(input)
                self.cfg.qmax = input
        except:
            print('Input must be positive float.')
            self.qmaxBox.set_val(self.cfg.qmax)

        return None


    def rminBoxFunc(self,input):
        try:
            input = np.float(input)
            if input < 0 or input >= self.cfg.rmax:  # Cannot be lower than qmin
                self.rminBox.set_val(self.cfg.rmin)
            else:
                self.rminBox.set_val(input)
                self.cfg.rmin = input
        except:
            print('Input must be positive float.')
            self.rminBox.set_val(self.cfg.rmin)   

        return None


    def rmaxBoxFunc(self,input):
        try:
            input = np.float(input)
            if input < 0 or input <= self.cfg.rmin:  # Cannot be lower than qmin
                self.rmaxBox.set_val(self.cfg.rmax)
            else:
                self.rmaxBox.set_val(input)
                self.cfg.rmax = input

        except:
            print('Input must be positive float.')
            self.maxBox.set_val(self.cfg.rmax)

        return None


    def rstepBoxFunc(self,input):
        try:
            input = np.float(input)
            if input <= 0:
                self.rstepBox.set_val(self.cfg.rstep)
                print('\nInput must be positive float.')
            else:
                self.cfg.rstep = input
            nyquistVal = round(np.pi / self.cfg.qmax,3)
            if input != nyquistVal and self.nyquistBox.get_status()[0] == True:
                self.nyquistBox.set_active(0)
            elif input > nyquistVal:
                print('\nRstep is larger than the recommended Nyquist sampling interval.')
                print('Reconsider Rstep as structural information will be lost during Fourier Transformation!')
        except:
            print('\nInput must be positive float.')
            self.rstepBox.set_val(self.cfg.rstep)

        return None


    def fframeBoxFunc(self,input):
        try:
            input = np.int(input)
            if input < 1 or input > self.lastFrame:  
                self.fframeBox.set_val(self.firstFrame)
            else:
                self.fframeBox.set_val(input)
                self.firstFrame = input
        except:
            print('Input must be positive integer.')
            self.fframeBox.set_val(self.firstFrame)

        return None

    def lframeBoxFunc(self,input):
        try:
            input = np.int(input)
            if input < 1 or input < self.firstFrame:  
                self.lframeBox.set_val(self.lastFrame)
            else:
                self.lframeBox.set_val(input)
                self.lastFrame = input
        except:
            print('Input must be positive integer.')
            self.lframeBox.set_val(self.lastFrame)

        return None


    def scaleBoxFunc(self,input):
        try:
            input = np.float(input)
            if input <= 0:  
                self.scaleBox.set_val(self.scale)
            else:
                self.scaleBox.set_val(input)
                self.scale = input
        except:
            print('Input must be positive float.')
            self.scaleBox.set_val(self.scale)

        if input != self.scale:
            self.phScale = input
        return None


    def setRange(self,event):
        self.ax4.set_xlim(self.cfg.qmin, self.cfg.qmax)
        self.ax3.set_xlim(self.cfg.qmin, self.cfg.qmax)
        self.ax2.set_xlim(self.cfg.rmin, self.cfg.rmax)
        # XXX Set grid spacing
        return None

    def setFrame(self,event):
        if self.phFrames == True:
            self.clear(event)
        
        self.ax1.axvspan(self.firstFrame-1, self.lastFrame, facecolor='0.5', alpha=0.3, zorder=-100)
        self.phFrames = True
        return None

    def calculate(self,event):
        if self.phFrames == True:  # Only change scale if frames are chosen
            self.scaleMat[self.firstFrame-1:self.lastFrame] = self.scale
            ph = np.multiply(self.iq_bg, self.scaleMat[:, np.newaxis])
            y_diffph = np.zeros((len(ph), len(ph[0])))
            for i in range(len(ph)):
                y_diffph[i] = self.iq_data[i] - ph[i]

            self.iq_diff = np.array(y_diffph)
            self.phFrames = False

        elif self.relScale != 1:
            print (type(self.relScale))
            print(type(self.scaleMat),'<--- Mat')
            self.scaleMat = self.scaleMat[:] * self.relScale
            self.relScale = 1.
            self.scaleSliderBox.set_val(self.relScale)
            self.scaleSliderBar.set_val(self.relScale)
        
        self.fqGrid, _, self.fq, self.rGrid, self.gr,_ = tempPDFcalc(self,self.qGrid,self.iq_diff,cfg=self.cfg)
        self.ax4.cla()
        self.ax3.cla()
        self.ax2.cla()
        self.ax1.cla()
        self.setupax4()
        self.setupax3()
        self.setupax2()
        self.setupax1()

        self.fig.canvas.draw_idle()

        return None
    
    def clear(self,event):
        self.phFrames = False
        self.ax1.cla()
        self.setupax1()
        return None

    def checkBoxFunc(self):
        return self.checkBox.get_status()

    def dataformatBoxFunc(self,event):
        if event.upper() == 'TWOTHETA':
            self.dataformatBox.set_val('twotheta')
            self.cfg.dataformat = 'twotheta'
        elif event.upper() == 'QA': 
            if self.cfg.dataformat == 'Qnm': 
                self.qGrid = self.qGrid[:] / 10

            self.dataformatBox.set_val('QA')
            self.cfg.dataformat = 'QA'

        elif event.upper() == 'QNM':
            if self.cfg.dataformat == 'QA': 
                self.qGrid = self.qGrid[:] * 10

            self.dataformatBox.set_val('Qnm')
            self.cfg.dataformat = 'Qnm'
        else:
            print('\nDataformat not understood.')
            print('Possible dataformats are: twotheta, QA, Qnm.')
            self.dataformatBox.set_val(self.cfg.dataformat)

        return None


    def compositionBoxFunc(self,event):
        self.cfg.composition = event
        return None


    def qinstBoxFunc(self,event):
        try:
            event = np.float(event)
            if self.cfg.qmax < event:
                self.cfg.qmaxinst = event
                self.qinstBox.set_val(event)
            else:
                print('\nInput must be larger than qmax.') 
                self.qinstBox.set_val(self.cfg.qmaxinst)   
        except:
            print('\nInput must be positive float.')
            self.qinstBox.set_val(self.cfg.qmaxinst)
        return None


    def rpolyBoxFunc(self,event):
        try:
            event = np.float(event)
            self.cfg.rpoly = event
            self.rpolyBox.set_val(event)
        except:
            print('\nInput must be float.')
            self.rpolyBox.set_val(self.cfg.rpoly)        
        return None


    def nyquistBoxFunc(self,event):
        if self.nyquistBox.get_status()[0] == True:
            nyquistVal = round(np.pi / self.cfg.qmax,3)
            self.rstepBox.set_val(nyquistVal)
            self.cfg.rstep = nyquistVal

        return None


    def scaleSliderBoxFunc(self,input):
        try:
            input = np.float(input)
            input = round(input,3)

            if input <= 0. or input >=2.:  
                self.scaleSliderBox.set_val(self.relScale)
                self.scaleSliderBar.set_val(self.relScale)
            else:
                self.scaleSliderBox.set_val(input)
                self.scaleSliderBar.set_val(input)
                self.relScale = input
        except:
            print('Input must be float between 0-2.')
            self.scaleSliderBox.set_val(self.relScale)
        return None


    def scaleSliderBarFunc(self,event):
        even = np.float(event)
        self.relScale = event
        self.scaleSliderBox.set_val(event)
        return None


    def delButFunc(self,event):
        print ('Deleting last frame!')
        self.iq_data = np.delete(self.iq_data,-1,0)  
        self.iq_bg = np.delete(self.iq_bg,-1,0)       
        self.iq_diff = np.delete(self.iq_diff,-1,0)   
        self.fq = np.delete(self.fq,-1,0)   
        self.gr = np.delete(self.gr,-1,0)   
        self.scaleMat = np.delete(self.scaleMat,-1)
        self.raw_y = np.delete(self.raw_y,-1,0)
        self.raw_y_bg = np.delete(self.raw_y_bg,-1,0)

        self.ax4.cla()
        self.ax3.cla()
        self.ax2.cla()
        self.ax1.cla()
        self.setupax4()
        self.setupax3()
        self.setupax2()
        self.setupax1()
        return None


    def conButFunc(self,event):
        plt.close()
        return None


if __name__ =='__main__':
    testObj=DRinterface()