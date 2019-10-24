import matplotlib.pyplot as plt
from matplotlib.widgets import Button, CheckButtons, TextBox, RadioButtons, Slider
import numpy as np
import matplotlib
import random

from math import floor
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

def createButtons(self):
    # Creating the buttons
    ###
    # 
    # First row
    #
    ###
    axbox = plt.axes([0.65, 0.82, 0.13, 0.16])

    index = [i for i,x in enumerate(self.method) if x == True]
    self.radioBox = RadioButtons(axbox, ['Method 1','Method 2','Method 3','Method 4'], activecolor='k')
    self.radioBox.set_active(index[0])

    axbox = plt.axes([0.65, 0.76, 0.13, 0.04])
    self.recalcBut = Button(ax=axbox,
                    label='Recalculate scaling',
                    color='darkgray',
                    hovercolor='whitesmoke')

    axbox = plt.axes([0.65, 0.70, 0.13, 0.04])
    self.qminBox = TextBox(axbox, '$q_{min}$ ', initial='{}'.format(self.cfg.qmin))

    axbox = plt.axes([0.65, 0.64, 0.13, 0.04])
    self.qmaxBox = TextBox(axbox, '$q_{max}$ ', initial='{}'.format(self.cfg.qmax))

    axbox = plt.axes([0.65, 0.58, 0.13, 0.04])
    self.rminBox = TextBox(axbox, '$r_{min}$ ', initial='{}'.format(self.cfg.rmin))

    axbox = plt.axes([0.65, 0.52, 0.13, 0.04])
    self.rmaxBox = TextBox(axbox, '$r_{max}$ ', initial='{}'.format(self.cfg.rmax))

    axbox = plt.axes([0.65, 0.46, 0.13, 0.04])
    self.rstepBox = TextBox(axbox, '$r_{step}$ ', initial='{}'.format(self.cfg.rstep))

    axbox = plt.axes([0.65, 0.40, 0.13, 0.04]) #left, bottom, width, height
    self.gridBut = Button(ax=axbox,
                    label='Set q and r range',
                    color='darkgray',
                    hovercolor='whitesmoke')

    axbox = plt.axes([0.65, 0.34, 0.13, 0.04])
    self.fframeBox = TextBox(axbox, 'First ', initial='{}'.format(self.firstFrame))

    axbox = plt.axes([0.65, 0.28, 0.13, 0.04])
    self.lframeBox = TextBox(axbox, 'Last ', initial='{}'.format(self.lastFrame))

    axbox = plt.axes([0.65, 0.22, 0.13, 0.04]) #left, bottom, width, height
    self.framesBut = Button(ax=axbox,
                    label='Chose frames',
                    color='darkgray',
                    hovercolor='whitesmoke')

    axbox = plt.axes([0.65, 0.16, 0.13, 0.04])
    self.scaleBox = TextBox(axbox, 'Scale ', initial='{}'.format(self.scale))

    axbox = plt.axes([0.65, 0.10, 0.13, 0.04]) #left, bottom, width, height
    self.calBut = Button(ax=axbox,
                    label='Calculate',
                    color='darkgray',
                    hovercolor='whitesmoke')

    axbox = plt.axes([0.65, 0.04, 0.13, 0.04]) #left, bottom, width, height
    self.clearBut = Button(ax=axbox,
                    label='Clear',
                    color='darkgray',
                    hovercolor='whitesmoke')

    ###
    # 
    # Second row
    #
    ###

    axbox = plt.axes([0.85, 0.82, 0.13, 0.16])
    self.checkBox = CheckButtons(axbox, ['I(q)','S(q)','F(q)','G(r)'], [True,True,True,True])
    
    axbox = plt.axes([0.85, 0.76, 0.13, 0.04])
    self.dataformatBox = TextBox(axbox, 'Dataformat ', initial='{}'.format(self.cfg.dataformat))

    axbox = plt.axes([0.85, 0.7, 0.13, 0.04])
    self.compositionBox = TextBox(axbox, 'Composition ', initial='{}'.format(self.cfg.composition))

    axbox = plt.axes([0.85, 0.64, 0.13, 0.04])
    self.qinstBox = TextBox(axbox, '$q_{maxinst}$ ', initial='{}'.format(self.cfg.qmaxinst))

    axbox = plt.axes([0.85, 0.58, 0.13, 0.04])
    self.rpolyBox = TextBox(axbox, '$r_{poly}$ ', initial='{}'.format(self.cfg.rpoly))

    axbox = plt.axes([0.85, 0.46, 0.13, 0.1])
    self.nyquistBox = CheckButtons(axbox,['Nyquist sampling'], [False])

    axbox = plt.axes([0.85, 0.40, 0.13, 0.04])
    self.scaleSliderBox = TextBox(axbox, 'Relative scale ', initial='{}'.format(1.))

    axbox = plt.axes([0.85, 0.34, 0.13, 0.04])
    self.scaleSliderBar = Slider(axbox, 'Relative scale ', valmin=0., valmax=2., valinit=1.)

    axbox = plt.axes([0.85, 0.22, 0.13, 0.1]) #left, bottom, width, height
    self.delBut = Button(ax=axbox,
                    label='Delete last frame',
                    color='darkgray',
                    hovercolor='whitesmoke')

    axbox = plt.axes([0.85, 0.04, 0.13, 0.04]) #left, bottom, width, height
    self.conBut = Button(ax=axbox,
                    label='Continue',
                    color='forestgreen',
                    hovercolor='limegreen')

    """
    Appear depending on method chosen 
    self.method1 = plt.axes([0.85, 0.10, 0.1, 0.04]) #left, bottom, width, height
    self.clearBut = Button(ax=self.method1,
                    label='Clear',
                    color='darkgray',
                    hovercolor='whitesmoke')
    self.method1.set_visible(False)
    self.method1.set_visible(True)
    """

    # Connecting the buttons
    self.radioBox.on_clicked(self.radioBoxFunc)
    self.recalcBut.on_clicked(self.recalc)

    self.qminBox.on_submit(self.qminBoxFunc)
    self.qmaxBox.on_submit(self.qmaxBoxFunc)
    self.rminBox.on_submit(self.rminBoxFunc)
    self.rmaxBox.on_submit(self.rmaxBoxFunc)
    self.rstepBox.on_submit(self.rstepBoxFunc)
    self.gridBut.on_clicked(self.setRange)
    self.fframeBox.on_submit(self.fframeBoxFunc)
    self.lframeBox.on_submit(self.lframeBoxFunc)
    self.framesBut.on_clicked(self.setFrame)
    self.scaleBox.on_submit(self.scaleBoxFunc)
    self.calBut.on_clicked(self.calculate)
    self.clearBut.on_clicked(self.clear)


    self.dataformatBox.on_submit(self.dataformatBoxFunc)
    self.compositionBox.on_submit(self.compositionBoxFunc)
    self.qinstBox.on_submit(self.qinstBoxFunc)
    self.rpolyBox.on_submit(self.rpolyBoxFunc)
    self.nyquistBox.on_clicked(self.nyquistBoxFunc)
    self.scaleSliderBox.on_submit(self.scaleSliderBoxFunc)
    self.scaleSliderBar.on_changed(self.scaleSliderBarFunc)
    self.delBut.on_clicked(self.delButFunc)
    self.conBut.on_clicked(self.conButFunc)


    return None