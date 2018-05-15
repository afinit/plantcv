# ROI functions

import cv2
import numpy as np
from plantcv import print_image
from plantcv import plot_image
from plantcv import fatal_error
from plantcv import params


# Create an ROI from a binary mask
def from_binary_image(bin_img, img):
    """Create an ROI from a binary image

    Inputs:
    bin_img       = Binary image to extract an ROI contour from.
    img           = An RGB or grayscale image to plot the ROI on.

    Outputs:
    roi_contour   = An ROI set of points (contour).
    roi_hierarchy = The hierarchy of ROI contour(s).

    :param bin_img: numpy.ndarray
    :param img: numpy.ndarray
    :return roi_contour: list
    :return roi_hierarchy: numpy.ndarray
    """
    # Autoincrement the device counter
    params.device += 1
    # Make sure the input bin_img is binary
    if len(np.unique(bin_img)) != 2:
        fatal_error("Input image is not binary!")
    # Use the binary image to create an ROI contour
    roi_contour, roi_hierarchy = cv2.findContours(np.copy(bin_img), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:]
    # Draw the ROI if requested
    if params.debug is not None:
        _draw_roi(img=img, roi_contour=roi_contour)

    return roi_contour, roi_hierarchy


# Create a rectangular ROI
def rectangle(x, y, h, w, img):
    """Create a rectangular ROI.

    Inputs:
    x             = The x-coordinate of the upper left corner of the rectangle.
    y             = The y-coordinate of the upper left corner of the rectangle.
    h             = The height of the rectangle.
    w             = The width of the rectangle.
    img           = An RGB or grayscale image to plot the ROI on in debug mode.

    Outputs:
    roi_contour   = An ROI set of points (contour).
    roi_hierarchy = The hierarchy of ROI contour(s).

    :param x: int
    :param y: int
    :param h: int
    :param w: int
    :param img: numpy.ndarray
    :return roi_contour: list
    :return roi_hierarchy: numpy.ndarray
    """
    # Autoincrement the device counter
    params.device += 1

    # Get the height and width of the reference image
    height, width = np.shape(img)[:2]

    # Check whether the ROI is correctly bounded inside the image
    if x < 0 or y < 0 or x + w > width or y + h > height:
        fatal_error("The ROI extends outside of the image!")

    # Create the rectangle contour vertices
    pt1 = [x, y]
    pt2 = [x, y + h - 1]
    pt3 = [x + w - 1, y + h - 1]
    pt4 = [x + w - 1, y]

    # Create the ROI contour
    roi_contour = [np.array([[pt1], [pt2], [pt3], [pt4]], dtype=np.int32)]
    roi_hierarchy = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)

    # Draw the ROI if requested
    if params.debug is not None:
        _draw_roi(img=img, roi_contour=roi_contour)

    return roi_contour, roi_hierarchy


# Draw the ROI on a reference image
def _draw_roi(img, roi_contour):
    """Draw an ROI

    :param img: numpy.ndarray
    :param roi_contour: list
    """
    # Make a copy of the reference image
    ref_img = np.copy(img)
    # If the reference image is grayscale convert it to color
    if len(np.shape(ref_img)) == 2:
        ref_img = cv2.cvtColor(ref_img, cv2.COLOR_GRAY2BGR)
    # Draw the contour on the reference image
    cv2.drawContours(ref_img, roi_contour, -1, (255, 0, 0), 5)
    if params.debug == "print":
        # If debug is print, save the image to a file
        print_image(ref_img, (str(params.device) + "_roi.png"))
    elif params.debug == "plot":
        # If debug is plot, print to the plotting device
        plot_image(ref_img)
