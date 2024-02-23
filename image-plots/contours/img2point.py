
import sys
import os
import numpy as np
import cv2 as cv



def print_usage():
    print(sys.argv[0] + " <img-name>")

def main():
#    print(sys.argv[0])

    if (len(sys.argv) == 1):
        print_usage()
        sys.exit(100)

    img_fname = sys.argv[1]
    if (not os.path.exists(img_fname)):
        print("[" + img_fname + "] not found.")
        sys.exit(101)

    # get contours
    input_img = cv.imread(img_fname)
    imgray = cv.cvtColor(input_img, cv.COLOR_BGR2GRAY)
    ret, thresh = cv.threshold(imgray, 127, 255, 0)
    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    print(contours)

    # Create black empty images
    W = 800
    size = W, W, 3
    bg_img = np.zeros(size, dtype=np.uint8)
#    print(bg_img)

    # Draw a diagonal blue line with thickness of 5 px
    cv.line(bg_img, (0, 0), (511, 511), (255, 0, 0), 5)
    # draw contours in green, 1 px
    cv.drawContours(bg_img, contours, -1, (0, 255, 0), 1)

    # show img
    cv.imshow("test", bg_img)
    cv.waitKey(0)
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()
