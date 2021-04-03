from logging import debug
import cv2
import numpy as np
import matplotlib.pyplot as plt

from utility import *

class Pre_Processing:

    def __init__(self, img, debug=False):
        self.debug = debug 
        self.original_image =  img

    def getBinaryImage(self):
        gray_image = self.convertColorSpace(self.original_image)
        remove_shadow_image = self.removeShadow(gray_image)
        binary_image = self.convert2binaryImage(remove_shadow_image)
        return binary_image

    def convertColorSpace(self, img):
        image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        if(self.debug):
            showImage(image, 'convert color space')

        return image

    def removeShadow(self, gray_img):
        dilated_img = cv2.dilate(gray_img, np.ones((7,7), np.uint8))
        bg_img = cv2.medianBlur(dilated_img, 99)
        diff_img = 255 - cv2.absdiff(gray_img, bg_img)
        norm_img = diff_img.copy()
        cv2.normalize(diff_img, norm_img, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)


        if(self.debug):
            # showImage(dilated_img, 'dilated image')
            # showImage(bg_img, 'get background')
            showImage(diff_img, 'remove shadow')
        
        return diff_img

    def convert2binaryImage(self, gray_img):

        bilateral = cv2.bilateralFilter(gray_img, 11, 40, 40)
        blur = cv2.GaussianBlur(bilateral,(5,5),0)
        thresh_img = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 35, 10)

        if(self.debug):
            # showImage(bilateral, 'bilateral image')
            # showImage(blur, 'blur')
            showImage(thresh_img, 'thresholding (binary image)')
            
        return thresh_img
    
    def resizeImage(self, img, expect_width=28, expect_height=28):

        height = int(img.shape[0])
        width = int(img.shape[1])

        min_ = min(width,height)

        if(width == min_):
            ratio_w = 1
            ratio_h = width*1/height
            new_dimension = ( int(expect_width*ratio_h / ratio_w), expect_width)
        else:
            ratio_w = width*1/height
            ratio_h = 1
            new_dimension = ( expect_width, int(expect_width*ratio_h / ratio_w))
            
        img_resize = cv2.resize(img, new_dimension, interpolation=cv2.INTER_AREA)

        w, h = 28, 28
        top_pad = int(np.floor((h - img_resize.shape[0]) / 2).astype(np.uint16))
        bottom_pad = int(np.ceil((h - img_resize.shape[0]) / 2).astype(np.uint16))

        right_pad = int(np.ceil((w - img_resize.shape[1]) / 2).astype(np.uint16))
        left_pad = int(np.floor((w - img_resize.shape[1]) / 2).astype(np.uint16))

        img_resize = np.pad(img_resize, [ (top_pad,bottom_pad) , (left_pad,right_pad) ], "constant", constant_values=0)

        if(self.debug):
            #print('img size (width, height): ({},{})'.format(width,height))
            #print('ratio : {},{}'.format(ratio_w, ratio_h))
            #print("pad : (top,bottom) , (left,right) = ({},{}), ({},{})".format(top_pad,bottom_pad,left_pad,right_pad))
            showImage(img_resize, 'resized Image')

        return img_resize
