import cv2
import numpy as np
import sys

# read arguments
if(len(sys.argv) != 7) :
    print(sys.argv[0], ": takes 6 arguments. Not ", len(sys.argv)-1)
    print("Expecting arguments: w1 h1 w2 h2 ImageIn ImageOut.")
    print("Example:", sys.argv[0], " 0.2 0.1 0.8 0.5 fruits.jpg out.png")
    sys.exit()

w1 = float(sys.argv[1])
h1 = float(sys.argv[2])
w2 = float(sys.argv[3])
h2 = float(sys.argv[4])
name_input = sys.argv[5]
name_output = sys.argv[6]

# check the correctness of the input parameters
if(w1<0 or h1<0 or w2<=w1 or h2<=h1 or w2>1 or h2>1) :
    print(" arguments must satisfy 0 <= w1 < w2 <= 1, 0 <= h1 < h2 <= 1")
    sys.exit()

# read image
inputImage = cv2.imread(name_input, cv2.IMREAD_COLOR)

if(inputImage is None) :
    print(sys.argv[0], ": Failed to read image from: ", name_input)
    sys.exit()
# cv2.imshow("input image: " + name_input, inputImage)

# check for color image and change w1, w2, h1, h2 to pixel locations 
rows, cols, bands = inputImage.shape
if(bands != 3) :
    print("Input image is not a standard color image:", inputImage)
    sys.exit()

#Converting the image to LUV
image_luv = cv2.cvtColor(inputImage, cv2.COLOR_BGR2LAB)

W1 = round(w1*(cols-1))
H1 = round(h1*(rows-1))
W2 = round(w2*(cols-1))
H2 = round(h2*(rows-1))

# Class Histogram Equalization
def histogramEq(window_l):
    values, counts = np.unique(window_l, return_counts=True)
    hist = list(zip(values, counts))
    f = []
    for i in range(len(hist)):
        if i > 0:
            f.append(hist[i][1] + f[i - 1])
        else:
            f.append(hist[i][1])
    flr = []
    for j in range(len(hist)):
        if j > 0:
            flr.append(np.floor(((f[j] + f[j - 1]) * 256) / (2 * f[len(f) - 1])))
        else:
            flr.append(np.floor((f[j] * 256) / (2 * f[len(f) - 1])))
    i_floor = dict(zip(values, flr))

    key_val = {}
    for i in range(len(window_l)):
        for j in range(len(window_l[0])):
            window_l[i][j] = i_floor.get(window_l[i][j])
    return window_l

# Applying Class Histogram Equalization only to the window
eqImg = np.copy(image_luv)
eqImg[H1: H2+1, W1: W2+1, 0] = histogramEq(eqImg[H1: H2+1, W1: W2+1, 0])
# cv2.imshow("Equalized Lab Image", eqImg)

eqImg = cv2.cvtColor(eqImg, cv2.COLOR_LAB2BGR)
# cv2.imshow("Equalized BGR Image", eqImg)

# # saving the output - save the Luv Histogram Equalization window image
cv2.imwrite(name_output, eqImg)

# # wait for key to exit
# cv2.waitKey(0)
# cv2.destroyAllWindows()