from PIL import Image
import numpy as np

domain = 'digitaslbi'
path = '/Users/yircheng/Documents/Yi/ad_proj/img/'
format = '.png'


def average(pixel):
    return (int(pixel[0]) + int(pixel[1]) + int(pixel[2])) / 3

def toGrey(img):
    grey_img = np.zeros((img.shape[0], img.shape[1]))

    for rownum in range(len(img)):
        for colnum in range(len(img[rownum])):
            grey_img[rownum][colnum] = average(img[rownum][colnum])

    return grey_img

def toOut(img):
    out_img = Image.fromarray(img)
    out_img.show()
    if out_img.mode != 'RGB':
        out_img = out_img.convert('RGB')
    out_img.save(path + domain + '_grey' + format)

def main():
    ##Read Original Image##
    im = Image.open(path + domain + format)
    img_array = np.array(im)
    print img_array.shape

    ##Transform to GreyScale Image##
    grey_img=toGrey(img_array)

    ##Save##
    toOut(grey_img)


if __name__=="__main__":
	main()