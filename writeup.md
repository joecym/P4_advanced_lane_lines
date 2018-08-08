# P4 Advanced Lane Lines Writeup
## Joe Cymerman
## 8 August 2018
The goals / steps of this project are the following:

* Compute the camera calibration matrix and distortion coefficients given a set of chessboard images.
* Apply a distortion correction to raw images.* Use color transforms, gradients, etc., to create a thresholded binary image.
* Apply a perspective transform to rectify binary image ("birds-eye view").
* Detect lane pixels and fit to find the lane boundary.
* Determine the curvature of the lane and vehicle position with respect to center.
* Warp the detected lane boundaries back onto the original image.
* Output visual display of the lane boundaries and numerical estimation of lane curvature and vehicle position.

[//]: # (Image References)

[image1]: ./output_images/warped_check.png "Warped Chess Board"
[image2]: ./output_images/warped0.jpg "Warped Image 1"
[image3]: ./output_images/warped1.jpg "Warped Image 2"
[image4]: ./output_images/warped2.jpg "Warped Image 3"
[image5]: ./output_images/warped3.jpg "Warped Image 4"
[image6]: ./output_images/warped4.jpg "Warped Image 5"
[image7]: ./output_images/warped5.jpg "Warped Image 6"
[image8]: ./output_images/warped6.jpg "Warped Image 7"
[image9]: ./output_images/warped7.jpg "Warped Image 8"
[image10]: ./output_images/thresh_binary.JPG "Threshold Binary Image"
[image11]: ./output_images/perspective_transform_confirm.JPG "Confirm Perspective Transform"
[image12]: ./output_images/top_dowm_wpoly.JPG "Top-Down w/ Polynomial"
[image13]: ./output_images/curvature_values.JPG "Radius of Curvature"
[image14]: ./output_images/poly0.jpg "Poly Image 1"
[image15]: ./output_images/poly1.jpg "Poly Image 2"
[image16]: ./output_images/poly2.jpg "Poly Image 3"
[image17]: ./output_images/poly3.jpg "Poly Image 4"
[image18]: ./output_images/poly4.jpg "Poly Image 5"
[image19]: ./output_images/poly5.jpg "Poly Image 6"
[image20]: ./output_images/poly6.jpg "Poly Image 7"
[image21]: ./output_images/poly7.jpg "Poly Image 8"

## [Rubric](https://review.udacity.com/#!/rubrics/571/view) Points

### Here I will consider the rubric points individually and describe how I addressed each point in my implementation.  

 ---

### Writeup / README

#### 1. Provide a Writeup / README that includes all the rubric points and how you addressed each one.   

You're reading it!

### Camera Calibration

#### 1. Briefly state how you computed the camera matrix and distortion coefficients. Provide an example of a distortion corrected calibration image.

The code for this step is contained in the first code cell of the IPython notebook located in "./P4_advanced_lane_lines.ipynb."
I start by preparing "object points", which will be the (x, y, z) coordinates of the chessboard corners in the world. Here I am assuming the chessboard is fixed on the (x, y) plane at z=0, such that the object points are the same for each calibration image.  Thus, `objp` is just a replicated array of coordinates, and `objpoints` will be appended with a copy of it every time I successfully detect all chessboard corners in a test image.  `imgpoints` will be appended with the (x, y) pixel position of each of the corners in the image plane with each successful chessboard detection.  

oliI then used the output `objpoints` and `imgpoints` to compute the camera calibration and distortion coefficients using the `cv2.calibrateCamera()` function.  I applied this distortion correction to the test image using the `cv2.undistort()` function and obtained this result: 

n![alt text][image1]

### Pipeline (single images)

#### 1. Provide an example of a distortion-corrected image.

In this step, I used the same mtx and dist that I found from the chessboard calibration. Here are the results of my unwarped images:

![alt text][image2]
![alt text][image3]
![alt text][image4]
![alt text][image5]
![alt text][image6]
![alt text][image7]
![alt text][image8]
![alt text][image9]

#### 2. Describe how (and identify where in your code) you used color transforms, gradients or other methods to create a thresholded binary image.  Provide an example of a binary image result.

In the 5th input box of my notebook, I consolidated the various transform functions from the lessons, and then applied each to all of the test images, forming a grid of images and the effects. 

After some thought and review of the lessons, I abandoned this approach and used the built-in OpenCV functions for the HLS and Sobel transforms. I then used thresholds for the x gradient and color channel and combined the effects on a single binary image. Here is the result:


![alt text][image10]

#### 3. Describe how (and identify where in your code) you performed a perspective transform and provide an example of a transformed image.

The code for my perspective transform includes a function called `unwarp_lane()` in the 8th code cell of the IPython notebook.  The function takes as inputs an image (`img`), as well as source (`mtx`) and destination (`dist`) points because the undistorting occurs inside as well. The `src` and `dst` points are contained within the function, which took a little trial and error. I plotted the trapezoid with the `src` points to help get it lined up, shown below with the result:

![alt text][image11]

#### 4. Describe how (and identify where in your code) you identified lane-line pixels and fit their positions with a polynomial?

Then I then used the implementation from the lessons to fit a polynomial to the found lane pixels with the window method. Here is the result:

![alt text][image12]

#### 5. Describe how (and identify where in your code) you calculated the radius of curvature of the lane and the position of the vehicle with respect to center.

In the 20th code box, I defined a function to evaluate the curvature and here are the resulting left and right curvatures for each of the eight test images:

![alt text][image13]

Also, the position of the vehicle can be related by extracting the coordinates of the start of the left and right lane curves, and then comparing the differnece to the coordinate of the center of the image. 

#### 6. Provide an example image of your result plotted back down onto the road such that the lane area is identified clearly.

I defined a function `polyfil` to create the shaded green area on my test images, shown here:

![alt text][image14]
![alt text][image15]
![alt text][image16]
![alt text][image17]
![alt text][image18]
![alt text][image19]
![alt text][image20]
![alt text][image21]

---

### Pipeline (video)

#### 1. Provide a link to your final video output.  Your pipeline should perform reasonably well on the entire project video (wobbly lines are ok but no catastrophic failures that would cause the car to drive off the road!).

Here's a [link to my video result](./project_video.mp4)

---

### Discussion

#### 1. Briefly discuss any problems / issues you faced in your implementation of this project.  Where will your pipeline likely fail?  What could you do to make it more robust?

Here I'll talk about the approach I took, what techniques I used, what worked and why, where the pipeline might fail and how I might improve it if I were going to pursue this project further.  
