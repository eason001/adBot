from PIL import Image
import os
from skimage.color.adapt_rgb import adapt_rgb, each_channel, hsv_value
from skimage import filters
from skimage.color import rgb2gray
from skimage import feature
from skimage import io
import numpy as np
import matplotlib.pyplot as plt
from skimage.exposure import rescale_intensity
from scipy import ndimage as ndi
import math
from skimage.filters import gaussian
from skimage.segmentation import active_contour
from scipy import misc
from skimage.morphology import skeletonize

path = "/Users/yircheng/Documents/Yi/ad_proj/data/img/"
out_path = "/Users/yircheng/Documents/Yi/ad_proj/out/"

def as_gray(image_filter, image, *args, **kwargs):
    gray_image = rgb2gray(image)
    return image_filter(gray_image, *args, **kwargs)

@adapt_rgb(as_gray)
def original_gray(image):
    return image

@adapt_rgb(as_gray)
def skeleton_gray(image):
    return skeletonize(image)

@adapt_rgb(as_gray)
def canny_gray(image,p):
    return feature.canny(image,sigma=p)

@adapt_rgb(as_gray)
def canny_gray2(image):
    return feature.canny(image,sigma=3)

@adapt_rgb(as_gray)
def sobel_gray(image):
    return filters.sobel(image)

@adapt_rgb(as_gray)
def roberts_gray(image):
    return filters.roberts(image)

@adapt_rgb(each_channel)
def sobel_each(image):
    return filters.sobel(image)


@adapt_rgb(hsv_value)
def sobel_hsv(image):
    return filters.sobel(image)

@adapt_rgb(each_channel)
def roberts_each(image):
    return filters.roberts(image)


@adapt_rgb(hsv_value)
def roberts_hsv(image):
    return filters.roberts(image)


def toprint(image,name):
	#fig = plt.figure(figsize=(14, 7))
	#ax = fig.add_subplot(111, adjustable='box-forced',axisbg='r')
	
	fig = plt.figure()
	ax = fig.add_subplot(111)

	ax.imshow(image, cmap=plt.cm.gray)
	ax.axis('off')
#	ax.set_title('original', fontsize=20)

	fig.tight_layout()
	fig.savefig(out_path + name)
	plt.show()


def reduce():
	cutfile = open('reduced_data', 'w')
	#print(im.getpixel((1,1)))
	#print len(temp[1]), len(temp)

	T_size = (80,20)
	L_size = (35,65)
	R_size = (35,65)
	testbox = (1, 1, 2, 2)
	T_box = (1, 1, 1400, 350)
	L_box = (1, 350, 350, 1000)
	R_box = (1050, 350, 1400, 1000)

	for file in os.listdir(path):

		im = Image.open(path + file)
		cutfile.write(file.split(".")[0])
	#	print(im.format, im.size, im.mode)

	######TOP REGION######	
		region = im.crop(T_box)
		region.thumbnail(T_size)
#		region.save(out_path + file.split(".")[0] + "_t.png")
		region.show()
		imarray = list(region.getdata())
		for item in imarray:
			cutfile.write(" " + str(item[0]) + " " + str(item[1]) + " " + str(item[2]))

	######LEFT REGION######	
		region = im.crop(L_box)
		region.thumbnail(L_size)
#		region.save(out_path + file.split(".")[0] + "_l.png")
	#	region.show()
		imarray = list(region.getdata())
		for items in imarray:
			cutfile.write(" " + str(item[0]) + " " + str(item[1]) + " " + str(item[2]))

	######RIGHT REGION######	
		region = im.crop(R_box)
		region.thumbnail(R_size)
#		region.save(out_path + file.split(".")[0] + "_r.png")
	#	region.show()
		imarray = list(region.getdata())
		for items in imarray:
			cutfile.write(" " + str(item[0]) + " " + str(item[1]) + " " + str(item[2]))

		cutfile.write('\n')

	cutfile.close()

	cutfile = open('reduced_data', 'r')
	for line in cutfile:
		print len(line.split(" "))
	cutfile.close()


def edge():

	#plt.switch_backend('MacOSX')
	image = io.imread(path + "bibme0.png")
	print type(image)
	print image.shape
#	edge_roberts = roberts(image)
#	edge_sobel = sobel(image)

	fig = plt.figure(figsize=(14, 7))
	ax_each = fig.add_subplot(121, adjustable='box-forced')
	ax_hsv = fig.add_subplot(122, sharex=ax_each, sharey=ax_each,
	                         adjustable='box-forced')

	# We use 1 - sobel_each(image)
	# but this will not work if image is not normalized
	ax_each.imshow(rescale_intensity(1 - sobel_gray(image)), cmap=plt.cm.gray)
	#ax_each.imshow(sobel_each(image))
	ax_each.set_xticks([]), ax_each.set_yticks([])
	ax_each.set_title("Sobel filter computed\n on individual RGB channels")
	
	
	# We use 1 - sobel_hsv(image) but this will not work if image is not normalized
	ax_hsv.imshow(rescale_intensity(1 - sobel_gray(image)), cmap=plt.cm.gray)
	ax_hsv.set_xticks([]), ax_hsv.set_yticks([])
	ax_hsv.set_title("Sobel filter computed\n on (V)alue converted image (HSV)")
	
	fig.savefig(out_path + 'sobel_gray.png')
	plt.show()

def edge_canny():

	image = io.imread(path + "bibme0.png")
	edges1 = rescale_intensity(1 - canny_gray(image))
	edges2 = rescale_intensity(1 - canny_gray2(image))

	fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(14, 7),
	                                    sharex=True, sharey=True)

	ax1.imshow(edges1, cmap=plt.cm.gray)
	ax1.axis('off')
	ax1.set_title('Canny filter, $\sigma=1$', fontsize=20)

	ax2.imshow(edges2, cmap=plt.cm.gray)
	ax2.axis('off')
	ax2.set_title('Canny filter, $\sigma=3$', fontsize=20)


	fig.tight_layout()
	fig.savefig(out_path + 'canny_gray.png')
	plt.show()

def skeleton():
	from skimage.morphology import skeletonize


	image = io.imread(path + "bibme0.png")
	gray_image = rgb2gray(image)
	skeleton = skeletonize(gray_image)
	toprint(skeleton,"bibme0_skeleton.png")

def rotate90():
	import matplotlib.pyplot as plt
	from scipy.ndimage.interpolation import rotate
	import scipy.misc
	
	image = io.imread(out_path + 'bibme0_contours.png')
	rotated_image = rotate(image, -90, reshape=True)
	toprint(rotated_image,"bibme0_contours.png")


def contour():
	from skimage.filters import gaussian
	from skimage.segmentation import active_contour
	import scipy
	from skimage import measure
	from skimage import img_as_float

	image = io.imread(path + "bibme0.png")
	image = rgb2gray(image)
	#image = img_as_float(image)
	#print image

	##### OPTION 1

	contours = measure.find_contours(image,0.9)
	#print size(contours)
	#toprint(contours,'bibme0_contours.png')
	fig, ax = plt.subplots()
	#ax.imshow(contours, interpolation='nearest', cmap=plt.cm.gray)

	for n, contour in enumerate(contours):
	    ax.plot(contour[:,0], contour[:,1], linewidth=0.5)
	#print len(contours)

	ax.axis('image')
	ax.set_xticks([])
	ax.set_yticks([])

	fig.savefig(out_path + 'bibme0_contours.png')
	#plt.show()
	rotate90()


	##### OPTION 2

	#s = np.linspace(0, 2*np.pi, 400)
	#x = 220 + 100*np.cos(s)
	#y = 100 + 100*np.sin(s)
	#init = np.array([x, y]).T 

	#snake = active_contour(gaussian(image, 3),init, alpha=0.015, beta=10, gamma=0.001)

	#fig = plt.figure(figsize=(7, 7))
	#ax = fig.add_subplot(111)
	#plt.gray()
	#ax.imshow(image)
	#ax.plot(init[:, 0], init[:, 1], '--r', lw=3)
	#ax.plot(snake[:, 0], snake[:, 1], '-b', lw=3)
	#ax.set_xticks([]), ax.set_yticks([])
	#ax.axis([0, image.shape[1], image.shape[0], 0])

	#fig.savefig(out_path + 'bibme0_contour.png')
	#plt.show()

def togray():

	im = Image.open(path + 'bibme0.png')
	gray_im = rgb2gray(np.array(im))
	toprint(gray_im,"gray_testim.png")

def test():

	im = Image.open(path + 'bibme0.png')
	misc.imsave('sample_original.png',im) # uses the Image module (PIL)
#	misc.imsave('sample_skeleton.png',1-skeleton_gray(np.array(im))) # uses the Image module (PIL)

#	import matplotlib.pyplot as plt
#	plt.imshow(im)
#	plt.show()


if __name__=="__main__":
#	edge()
#	edge_canny()
#	reduce()
#	skeleton()
#	contour()
#	togray()
	test()
