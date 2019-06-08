#!/usr/bin/env python
import roslib,rospy,sys,cv2,time
import numpy as np
import math
roslib.load_manifest('lane_follower')
# from __future__ import print_function
from std_msgs.msg import Int32
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

bridge = CvBridge()
pub = rospy.Publisher('lane_detection', Int32, queue_size=10) #ros-lane-detection
pub_image = rospy.Publisher('lane_detection_image',Image,queue_size=1)

def callback(data):

	# convert image to cv2 standard format
	img = bridge.imgmsg_to_cv2(data)

	# start time
	start_time = cv2.getTickCount()

	# Gaussian Filter to remove noise
	img = cv2.medianBlur(img,5)
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	#orig ( 200,  350, 3)
	#UMSA (1440, 1920, 3)
	rows,cols,channels = img.shape
	#print(rows, cols, channels)

	# ROI (region of interest)
	roi_mask = np.zeros(img.shape,dtype=np.uint8)
	roi_mask[int(rows*.05):rows,0:cols] = 255
	street = cv2.bitwise_and(img,roi_mask)

	stop_roi_mask = np.zeros(gray.shape,dtype=np.uint8)
	stop_roi_mask[1080:rows, 822:] = 255

	right_roi_mask = np.zeros(gray.shape,dtype=np.uint8)
	right_roi_mask[300:rows,960:cols] = 255
	right_roi = cv2.bitwise_and(img,img,mask = right_roi_mask)
	image = bridge.cv2_to_imgmsg(right_roi)
	#pub_image.publish(image)

	left_roi_mask = np.zeros(gray.shape,dtype=np.uint8)
	left_roi_mask[300:rows,0:959] = 255
	left_roi = cv2.bitwise_and(img,img,mask = left_roi_mask)

	# define range of color in HSV
	hsv = cv2.cvtColor(street,cv2.COLOR_BGR2HSV)

	sensitivity = 160 # range of sensitivity=[90,150]
	lower_white = np.array([0,0,255-sensitivity])
	upper_white = np.array([255,sensitivity,255])

	white_mask = cv2.inRange(hsv,lower_white,upper_white)
	white_mask = cv2.erode(white_mask, None, iterations=2)
	white_mask = cv2.dilate(white_mask, None, iterations=2)

        lower_red = np.array([150,70,50])#150
        upper_red = np.array([200,255,255])

        lower_red2 = np.array([0,100,100])
        upper_red2 = np.array([9,255,255])#10

        red_mask1 = cv2.inRange(hsv,lower_red,upper_red)
        red_mask1 = cv2.erode(red_mask1, None, iterations=2)
        red_mask1 = cv2.dilate(red_mask1, None, iterations=2)

        red_mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        red_mask2 = cv2.erode(red_mask2, None, iterations=2)
        red_mask2 = cv2.dilate(red_mask2, None, iterations=2)

        red_mask = cv2.bitwise_or(red_mask1,red_mask2)

	lower_yellow = np.array([0,100,100]) #0,100,100
	upper_yellow = np.array([40,255,255]) #30,255,255

	yellow_mask = cv2.inRange(hsv,lower_yellow,upper_yellow)
	yellow_mask = cv2.erode(yellow_mask, None, iterations=2)
	yellow_mask = cv2.dilate(yellow_mask, None, iterations=2)

	# mask AND original img
	#whitehsvthresh = cv2.bitwise_and(right_roi,right_roi,mask=white_mask)  #only white
	whitehsvthresh = cv2.bitwise_and(street,street,mask=white_mask)  #only white
	yellowhsvthresh = cv2.bitwise_and(street,street,mask=yellow_mask)      #only yellow
	redhsvthresh = cv2.bitwise_and(street,street,mask=red_mask1)           #only red
	#image = bridge.cv2_to_imgmsg(whitehsvthresh)
	#pub_image.publish(image)
	
	#image = bridge.cv2_to_imgmsg(whitehsvthresh)
	#pub_image.publish(image)

	# Canny Edge Detection 
	right_edges = cv2.Canny(whitehsvthresh,100,200)
	left_edges_y = cv2.Canny(yellowhsvthresh,100,200)
	left_edges_w = cv2.Canny(whitehsvthresh,100,200)

	right_edges = cv2.bitwise_and(right_edges,right_roi_mask)
	left_edges_y = cv2.bitwise_and(left_edges_y,left_roi_mask)
	left_edges_w = cv2.bitwise_and(left_edges_w,left_roi_mask)
	left_edges = cv2.bitwise_or(left_edges_y, left_edges_w)
	#image = bridge.cv2_to_imgmsg(left_edges)
	#pub_image.publish(image)

	red_edges_hsv = cv2.Canny(redhsvthresh,100,200)
	red_edges = cv2.bitwise_and(red_edges_hsv,stop_roi_mask)
	
	# Standard Hough Transform
	right_lines = cv2.HoughLines(right_edges,0.8,np.pi/180,35)
	left_lines = cv2.HoughLines(left_edges,0.8,np.pi/180,35)
	red_lines = cv2.HoughLines(red_edges,1,np.pi/180,40)
	#print(right_lines)
	
	xm = cols/2
	ym = rows
	
	# Draw right lane
	x = []
	i = 0
	if right_lines is not None:
		right_lines = np.array(right_lines[0])
		for rho, theta in right_lines:
                        a=np.cos(theta)
                        b=np.sin(theta)
                        x0,y0=a*rho,b*rho
                        y3 = 140
			x3 = int(x0+((y0-y3)*np.sin(theta)/np.cos(theta)))
			x.insert(i,x3)
			i+1
                        pt1=(int(x0+1000*(-b)),int(y0+1000*(a)))
                        pt2=(int(x0-1000*(-b)),int(y0-1000*(a)))
			#print(pt1)
			#print(pt2)
                        cv2.line(img,pt1,pt2,(255,0,0),35)


	if len(x) != 0:
		xmin = x[0]
		for k in range(0,len(x)):
			if x[k] < xmin and x[k] > 0:
				xmin = x[k]
		#kr = int(np.sqrt(((xmin-xm)*(xmin-xm))+((y3-ym)*(y3-ym))))
		kr = int(math.sqrt(((xmin-xm)*(xmin-xm))+((y3-ym)*(y3-ym))))
	else:
		kr = 0
		xmin = 0

	# Draw left lane yellow
	x = []
	i = 0

	if left_lines is not None:
		left_lines = np.array(left_lines[0])
		for rho, theta in left_lines:
                        a=np.cos(theta)
                        b=np.sin(theta)
                        x0,y0=a*rho,b*rho
			y3 = 140
			x3 = int(x0+((y0-y3)*np.sin(theta)/np.cos(theta)))
			x.insert(i,x3)
			i+1
                        pt1=(int(x0+1000*(-b)),int(y0+1000*(a)))
                        pt2=(int(x0-1000*(-b)),int(y0-1000*(a)))
                        cv2.line(img,pt1,pt2,(0,255,0),35)
                        cv2.line(img, (0,0), (1920, 1440), (0, 0, 255), 35)
#Above added June 4 2019 to test coordinates
			print(pt1)
			print(pt2)

        if len(x) != 0:
                xmax = x[0]
                for k in range(0,len(x)):
                        if x[k] > xmax and x[k]<cols:
                                xmax = x[k]
                kl = int(math.sqrt(((xmax-xm)*(xmax-xm))+((y3-ym)*(y3-ym))))
				#changed to math.sqrt 3 June 2019
        else:
                kl = 0
		xmax = 0

	error = kr - kl

	#end time
	end_time = cv2.getTickCount()

	time_count= (end_time - start_time) / cv2.getTickFrequency()
#	rospy.loginfo(time_count)

	if red_lines is not None:
		rospy.loginfo("STOP")
		message = 154 #stop
	elif right_lines is not None and left_lines is not None:
        	rospy.loginfo(error)
		if error > 150:
			error = 150
		elif error < -150:
			error = -150

		message = error

	elif left_lines is not None and right_lines is None:
		rospy.loginfo("Turn Right")
		rospy.loginfo(kl)
		message = 152 #turn right

	elif left_lines is None and right_lines is not None:
		rospy.loginfo("Turn Left")
		message = 153 #turn let
	elif left_lines is None and right_lines is None:
		rospy.loginfo("No line")
		message = 155 #no line found
	else:
		message = 155 #no line found

	pub.publish(message)
	image = bridge.cv2_to_imgmsg(img)
	pub_image.publish(image)

def lane_detection():
	rospy.init_node('lanedetection',anonymous=True)
	rospy.Subscriber("/camera/image_color",Image,callback,queue_size=1,buff_size=2**24)
	try:
		rospy.loginfo("Enetering ROS Spin")
		rospy.spin()
	except KeyboardInterrupt:
		print("Shutting down")

if __name__ == '__main__':
	try:
		lane_detection()
	except rospy.ROSInterruptException:
		pass