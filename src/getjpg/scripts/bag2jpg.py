#! /usr/bin/env python3

import cv2
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
import rospy
import time

class Main():
    def __init__(self):
        
        self.counter = 0
        self.cv_image = None
        self.bridge = CvBridge()
        rospy.Subscriber(rospy.get_param('~image_topic'), Image, self.callback, queue_size=1)
    
    def callback(self, input_image):

        self.cv_image = self.bridge.imgmsg_to_cv2(input_image, desired_encoding="")
    
    def save_image(self):
        
        if self.cv_image is None:
            return
        
        print('-------------------'+str(self.counter))
        cv2.imwrite(rospy.get_param('~output_path')+'data'+str(self.counter).zfill(7)+'.jpg', img=self.cv_image)
        self.counter+=1
        time.sleep(rospy.get_param('~delay_time'))
        self.cv_image = None

def main():

    rospy.init_node("bag2jpg", anonymous=False)

    rospy.loginfo('PLEASE, PLAY SOME BAG FILE')

    main_o = Main()
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        
        main_o.save_image()
        rate.sleep()

if __name__ == '__main__':

    main()