import numpy as np
import wx
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import  astropy.io.fits as pyfits
import os

def preview(filepath, dtype, width, height, skip=0):
    if not os.path.isfile(filepath):
        dlg = wx.MessageDialog(None, "无效路径！请选择一个文件（.fits or .raw)", caption="警告", style=wx.OK)
        dlg.ShowModal()
        return

    if os.path.splitext(filepath)[-1] == ".fits" :
        data = pyfits.getdata(filepath,dtype=dtype)
    if os.path.splitext(filepath)[-1] == ".raw":
        data = np.fromfile(filepath,dtype = dtype)
        data = data[skip:]
        data = np.reshape(data,(width,height))

    fig = plt.figure()
    ax = fig.add_subplot()

    #多帧显示切换
    if np.size(data.shape) == 3:
        fig.subplots_adjust(left=0.1, bottom=0.25)
        i = ax.imshow(data[0,:,:], cmap="gray")
        axFrame = fig.add_axes([0.2, 0.1, 0.5, 0.03])
        sframe = Slider(axFrame, "Frame", valmin=0, valmax=data.shape[0]-1, valinit=0, valstep=1)

        def update(val):
            fra = int(sframe.val)
            i.set_data(data[fra,:,:])
            fig.canvas.draw()
        sframe.on_changed(update)
    else:
        ax.imshow(data, cmap="gray")
    plt.show()


