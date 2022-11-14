from itertools import count
from pickle import TRUE
from django.conf import settings
from attendence_system.settings  import BASE_DIR
import threading
import cv2,os
import time

face_detection_videocam = cv2.CascadeClassifier('C:/Users/Admin/Downloads/Deeplearning/src/data/haarcascade_frontalface_alt2.xml')
temp_img = os.path.join(BASE_DIR,'attendence/temp')
class VideoCamera(object):
	def __init__(self):
		self.video = cv2.VideoCapture(0)

	def __del__(self):
		self.video.release()
		os.remove(str(BASE_DIR)+"\yahya.jpeg")

	def get_frame(self):
		success, image = self.video.read()
		# We are using Motion JPEG, but OpenCV defaults to capture raw images,
		# so we must encode it into JPEG in order to correctly display the
		# video stream.
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		# time.sleep(10)
		faces_detected = face_detection_videocam.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
		for (x, y, w, h) in faces_detected:
			# cv2.rectangle(image, pt1=(x, y), pt2=(x + w, y + h), color=(255, 0, 0), thickness=2)
			roi_gray = gray[y:y+h,x:x+w]
			img_name = "yahya.jpeg"
			cv2.imwrite(img_name,roi_gray)
			
		frame_flip = cv2.flip(image,1)
		ret, jpeg = cv2.imencode('.jpg', frame_flip)
		return jpeg.tobytes()