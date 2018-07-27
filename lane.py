import numpy as np
import cv2
import glob
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.pyplot



# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*9,3), np.float32)
objp[:,:2] = np.mgrid[0:9,0:6].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d points in real world space
imgpoints = [] # 2d points in image plane.

# Make a list of calibration images

#images = glob.glob('camera_cal/calibration*.jpg')
#image = glob.glob('camera_cal/calibration1.jpg')
img = cv2.imread('camera_cal/calibration2.jpg')
img_orig = img.copy()
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

# Find the chessboard corners
ret, corners = cv2.findChessboardCorners(gray, (9,6),None)
#print(ret,corners)
# If found, add object points, image points
if ret == True:
    objpoints.append(objp)
    imgpoints.append(corners)

# Draw and display the corners
img_corners = cv2.drawChessboardCorners(img_orig, (9,6), corners, ret)
f, (ax1, ax2) = plt.subplots(1, 2, figsize=(24, 9))
f.tight_layout()
ax1.imshow(img)
ax1.set_title('Original Image', fontsize=50)
ax2.imshow(img_corners)
ax2.set_title('Original with drawn corners', fontsize=50)
plt.subplots_adjust(left=0., right=1, top=0.9, bottom=0.)
plt.show()

plt.figure()
plt.imshow(img_orig)
plt.show()