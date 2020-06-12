import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
import astropy.io.fits as pyfits

data = pyfits.getdata('Dark.fits')

fig = plt.figure()
ax = fig.add_subplot(111)
fig.subplots_adjust(left=0.1, bottom=0.25)
i = ax.imshow(data[0,:,:], cmap="gray")

axframe = fig.add_axes([0.2, 0.1, 0.5, 0.03])

minFrame = 0
maxFrame = data.shape[0]

sframe = Slider(axframe, 'Freq', minFrame, maxFrame-1, valinit=minFrame, valstep=1)

def update(val):
    fra = int(sframe.val)
    i.set_data(data[fra,:,:])
    fig.canvas.draw()

sframe.on_changed(update)

resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', hovercolor='0.975')


def reset(event):
    sframe.reset()

button.on_clicked(reset)

plt.show()
