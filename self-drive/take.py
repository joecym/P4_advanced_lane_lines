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

import datetime



global i
i = 0

def callback(data):
    global i
    while i < 3 :
		x = datetime.datetime.now()
        # convert image to cv2 standard format
		img = bridge.imgmsg_to_cv2(data)
		cv2.imwrite( "pics/cal_image"+str(x)+str(i)+".jpg", img);
		i += 1 


def take():
	rospy.init_node('take',anonymous=True)
	rospy.Subscriber("/camera/image_color",Image,callback,queue_size=1,buff_size=2**24)
	try:
		rospy.loginfo("Taking_pic")
		rospy.spin()
	except KeyboardInterrupt:
		print("Shutting down")

if __name__ == '__main__':
	try:
		take()
	except rospy.ROSInterruptException:
		pass
