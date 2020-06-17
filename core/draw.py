import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import core.load as load
import numpy as np

def preview(MainFrame):
    filepath = MainFrame.fViewCtrl.GetPath()
    data = load.getData(MainFrame, filepath)
    if data is None:
         return

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


