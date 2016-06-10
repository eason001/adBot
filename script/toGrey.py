from scipy import misc
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

def average(pixel):
    return (int(pixel[0]) + int(pixel[1]) + int(pixel[2])) / 3

im = Image.open("/Users/yircheng/Documents/Yi/ad_proj/img/digitaslbi.png")
#image = misc.imread('/Users/yircheng/Documents/Yi/ad_proj/img/google.png')
img_array = np.array(im)
#print img_array[0][0].size #pixel [RGBY]
#print img_array[0].size
#print img_array.size
print img_array.shape
print img_array[0][0]

grey_img = np.zeros((img_array.shape[0], img_array.shape[1]))

for rownum in range(len(img_array)):
   for colnum in range(len(img_array[rownum])):
        grey_img[rownum][colnum] = average(img_array[rownum][colnum])

out_img = Image.fromarray(grey_img)
out_img.show()
if out_img.mode != 'RGB':
    out_img = out_img.convert('RGB')
out_img.save('/Users/yircheng/Documents/Yi/ad_proj/img/digitaslbi_grey.png')
