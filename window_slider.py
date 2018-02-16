"""
Process:
    1. process entire image (adaptiveThreshold, contour detection, bounding rect, rotate, etc.)
    2. Slide and slice based on tone and variety
    3. predict from data set
"""

import os
import glob
import cv2
import imutils
import matplotlib.pyplot as plt
import numpy as np
import time

os.chdir("C:\\Users\\grant\\IS\\IS552\\JSPapersBookofTheLawoftheLord\\RotationsApplied")

def show_images(images, cols = 2, titles = None):
    assert((titles is None)or (len(images) == len(titles)))
    n_images = len(images)
    if titles is None: titles = ['Image (%d)' % i for i in range(1,n_images + 1)]
    fig = plt.figure()
    for n, (image, title) in enumerate(zip(images, titles)):
        a = fig.add_subplot(cols, np.ceil(n_images/float(cols)), n + 1)
        if image.ndim == 2:
            plt.gray()
        plt.imshow(image)
        a.set_title(title)
    fig.set_size_inches(np.array(fig.get_size_inches()) * n_images)
    mng = plt.get_current_fig_manager()
    mng.window.state('zoomed')
    plt.show()

def variety_check(img, w):
    """
    Scan the middle 20 percent of the image for variety of tone
    Converts to black and white.
    Then verifies minimum of 2 changes to color tone
    Intended for small crops of images
    """
    block_size = w
    while block_size %2 != 1:
        block_size -= 1

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # (thresh, img_bw) = cv2.threshold(img_gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    # using 10 here to eliminate rows with faint lines
    img_bw = cv2.adaptiveThreshold(img_gray,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,block_size,10)
    (horizontal, vertical) = img_bw.shape
    h_lower = int(.4 * horizontal)
    h_upper = int(.6 * horizontal)
    v_lower = int(.4 * vertical)
    v_upper = int(.6 * vertical)

    # sum total changes accross the bw array. If none of middle x percentof  arrays contain more than one color change, discard entire boundary
    contained_variety = 0
    for horiz in img_bw[h_lower:h_upper]:
        row_value_changes = 0
        value_in_row = horiz[0]
        for vert_value in horiz[v_lower:v_upper]:
            if vert_value != value_in_row:
                row_value_changes += 1
                value_in_row = vert_value
        if row_value_changes > 2: # a change and back (we want more than one line)
            contained_variety += 1
    if contained_variety > 0:
        # print("Contained variety: ", contained_variety)
        return True
    else:
        return False

def tone_check(crop_rgb_img, h, w, base_tone=100):
    """
    Verify color tone of image passes minimum threshold.
    255 is brightest
    0 is darkest
    Intended for small crops of images
    """
    crop_val = 0
    for line in crop_rgb_img:
        for pixel in line:
            for rgb_val in pixel:
                crop_val += rgb_val
    if crop_val > (h*w*3*base_tone):
        # print("VALID TONE")
        # cv2.imshow('var', img_bw)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        return True
    else:
        # print("INVALID TONE")
        # cv2.imshow('var', crop_rgb_img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        return False

def window_slicer(img, w, h, increment_percentage, file_name):
    """
    params:
        img = color image
        w = desired crop width
        h = desired crop heigth
        increment percentage = amount frames will advance from w
        file_name = for output purposes
    """
    w_increment = increment_percentage * w
    h_increment = increment_percentage * h
    img_count = 0
    for y_index, col_val in enumerate(img):
        if y_index % (h_increment) == 0:
            # if len(crops) > 40:
                # show_images(crops, 5)
                # crops = []
            for x_index, row_val in enumerate(col_val):
                if x_index % (w_increment) == 0:
                    crop = img[y_index:y_index+h, x_index:x_index+w]
                    # print("Created crop")
                    if tone_check(crop, h, w) and variety_check(crop, w):
                        out = "C:\\Users\\grant\\IS\\IS552\\JSPapersBookofTheLawoftheLord\\RotationsApplied\\windows\\"+file_name+str(img_count)+".jpg"
                        img_count += 1
                        cv2.imwrite(out, crop)

for file in glob.glob("*.jpg"):
    print("reading img: ", file)
    img = cv2.imread(file)
    window_slicer(img, 40, 60, .25, str(file))