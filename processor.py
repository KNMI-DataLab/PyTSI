import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

im = Image.open("images/20180309081800.jpg")
pix = im.load()
print(im.size)
print(im.getbands())
#print(pix[100,100])
#print(list(im.getdata()), sep='\n')

plt.hist(list(im.histogram()),bins='auto')
plt.savefig("histogram.jpg")
