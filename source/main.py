#!/usr/bin/python

import sys
import cv2
from Inpainter import Inpainter

if __name__ == "__main__":
    """
    Usage: python main.py pathOfInputImage pathOfMaskImage [,halfPatchWidth=4].
    """
    if not len(sys.argv) == 3 and not len(sys.argv) == 4:
        print('Usage: python main.py pathOfInputImage pathOfMaskImage [,halfPatchWidth].')
        exit(-1)

    if len(sys.argv) == 3:
        halfPatchWidth = 4
    elif len(sys.argv) == 4:
        try:
            halfPatchWidth = int(sys.argv[3])
        except ValueError:
            print('Unexpected error:', sys.exc_info()[0])
            exit(-1)

    # image File Name
    imageName = sys.argv[1]
    # CV_LOAD_IMAGE_COLOR: loads the image in the RGB format TODO: check RGB sequence
    originalImage = cv2.imread(imageName)
    if originalImage is None:
        print('Error: Unable to open Input image.')
        exit(-1)

    # mask File Name
    maskName = sys.argv[2]
    inpaintMask = cv2.imread(maskName)
    inpaintMask = cv2.cvtColor(inpaintMask, cv2.COLOR_RGB2GRAY)
    if inpaintMask is None:
        print('Error: Unable to open Mask image.')
        exit(-1)

    i = Inpainter(originalImage, inpaintMask, halfPatchWidth)
    if (chek_result := i.checkValidInputs()) == i.CHECK_VALID:
        i.inpaint()
        cv2.imwrite("../tests/result.jpg", i.result)
        cv2.namedWindow("result")
        cv2.imshow("result", i.result)
        cv2.waitKey()
    else:
        print(f'Error: invalid parameters. Check result is {chek_result}')
