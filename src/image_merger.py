#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image, CompressedImage
from PIL import Image as PilImage
import io

class ImageMerger(object):
    def __init__(self):
        self.img_width = 640*5
        self.img_height = 480
        self.buffer = PilImage.new('RGB', (self.img_width, self.img_height))
        self.merged_pub = rospy.Publisher('merged_image', CompressedImage, queue_size=10)


    def callback(self, image, index):
        self.buffer.paste(PilImage.open(io.BytesIO(bytearray(image.data))), ((640*index), 0))

        #Compose a ROS message of the buffer
        outgoing = CompressedImage()
        outgoing.header = image.header #TODO this is bullshit
        outgoing.format = "png"
        img_byte_arr = io.BytesIO()
        self.buffer.save(img_byte_arr, format="png")
        outgoing.data = img_byte_arr.getvalue()

        # Make it everybody's problem 
        self.merged_pub.publish(outgoing)

if __name__ == '__main__':
    rospy.init_node('image_merger')
    composer = ImageMerger()
    rospy.Subscriber("/cam0/image_raw/compressed", CompressedImage, lambda msg: composer.callback(msg, 0))
    rospy.Subscriber("/cam1/image_raw/compressed", CompressedImage, lambda msg: composer.callback(msg, 1))
    rospy.Subscriber("/cam2/image_raw/compressed", CompressedImage, lambda msg: composer.callback(msg, 2))
    rospy.Subscriber("/cam3/image_raw/compressed", CompressedImage, lambda msg: composer.callback(msg, 3))
    rospy.Subscriber("/cam4/image_raw/compressed", CompressedImage, lambda msg: composer.callback(msg, 4))
    rospy.spin()
