import numpy as np
import cv2
import glob
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.pyplot
import datetime
import copy


# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*8,3), np.float32)
objp[:,:2] = np.mgrid[0:8,0:6].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d points in real world space
imgpoints = [] # 2d points in image plane.

# calibration image
img_orig = cv2.imread('pics/test_img/4c.jpg')
#x = datetime.datetime.now()
#cv2.imwrite( "pics/output_images/test"+str(x)+".jpg", img_orig);
img = copy.copy(img_orig)
undist = copy.copy(img_orig)
nx = 8 # the number of inside corners in x
ny = 6 # the number of inside corners in y

# Find the chessboard corners
gray = cv2.cvtColor(undist,cv2.COLOR_BGR2GRAY) 
ret, corners = cv2.findChessboardCorners(gray, (nx,ny),None)
#print(ret)
#print(corners)

# If found, add object points, image points
if ret == True:
    objpoints.append(objp)
    imgpoints.append(corners)

# calibrate camera
et2,mtx,dist,rvecs,tvecs=cv2.calibrateCamera(objpoints, imgpoints, img.shape[1::-1],None,None)

#undistort
undist = cv2.undistort(img, mtx, dist, None, mtx)
 
cv2.drawChessboardCorners(img_orig, (nx,ny), corners, ret)

src = np.float32([corners[0], corners[nx-1], corners[-1], corners[-nx]])
offset = 100
img_size = (gray.shape[1], gray.shape[0])
dst = np.float32([[offset, offset], [img_size[0]-offset, offset], 
                             [img_size[0]-offset, img_size[1]-offset], 
                             [offset, img_size[1]-offset]])
M = cv2.getPerspectiveTransform(src, dst)
warped = cv2.warpPerspective(undist, M, img_size)
print(M)
# Draw and display the corners

x = datetime.datetime.now()
f, (ax1, ax2) = plt.subplots(1, 2, figsize=(24, 9))
f.tight_layout()
ax1.imshow(img_orig)
ax1.set_title('Original Image', fontsize=50)
ax2.imshow(warped)
ax2.set_title('Warped Image', fontsize=50)
plt.subplots_adjust(left=0., right=1, top=0.9, bottom=0.)
plt.savefig("pics/output_images/"+"warped_check'+str(x)")

def unwarp(img, mtx, dist):
    undist = cv2.undistort(img, mtx, dist, None, mtx)

    src = np.float32([corners[0], corners[nx-1], corners[-1], corners[-nx]])
    offset = 100
    img_size = (gray.shape[1], gray.shape[0])
    dst = np.float32([[offset, offset], [img_size[0]-offset, offset], 
                             [img_size[0]-offset, img_size[1]-offset], 
                             [offset, img_size[1]-offset]])
    M = cv2.getPerspectiveTransform(src, dst)
    warped = cv2.warpPerspective(undist, M, img_size)
    return warped
