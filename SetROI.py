# -*- coding: utf-8 -*-

import ConfigParser
import cv2,os
import numpy as np
video = cv2.VideoCapture(0)

k = 2

def get_ROI(k=1): # 畫ROI
	global point
	point = []
	def click_and_crop(event, x, y, flags, param):
		global point
		if event == cv2.EVENT_LBUTTONDOWN:
			point.append([x, y])

		if len(point) == 1:
			newImage = img1.copy()
			if k == 3 or k == 33:
				cv2.rectangle(newImage, (point[0][0],point[0][1]), (x,y), (255, 0, 0), 2)
			else:
				cv2.rectangle(newImage, (point[0][0],point[0][1]), (x,y), (0, 255, 0), 2)
			cv2.imshow("image",newImage)
		if event == cv2.EVENT_LBUTTONUP:
			point.append([x, y])
		if len(point) == 2:
			if point[0][1]<point[1][1]:
				y1 = point[0][1]
				y2 = point[1][1]
			else:
				y1 = point[1][1]
				y2 = point[0][1]
			if point[0][0]<point[1][0]:
				x1 = point[0][0]
				x2 = point[1][0]
			else:
				x1 = point[1][0]
				x2 = point[0][0]
			roi = image[y1:y2,x1:x2]
			if k == 3:  #  設定 template 1
				cv2.imwrite('ROI1.png',roi)
				config = ConfigParser.ConfigParser()
				config.optionxform = str
				config.read('ROI.ini')
				total_section = config.sections()
				config.set("R1", "key_x1_image_1", str(point[0][0]))
				config.set("R1", "key_x2_image_1", str(point[1][0]))
				config.set("R1", "key_y1_image_1", str(point[0][1]))
				config.set("R1", "key_y2_image_1", str(point[1][1]))
				config.write(open('ROI.ini', 'wb'))
			if k == 33:  #  設定 template 2
				cv2.imwrite('ROI2.png',roi)
				config = ConfigParser.ConfigParser()
				config.optionxform = str
				config.read('ROI.ini')
				total_section = config.sections()
				config.set("R1", "key_x1_image_2", str(point[0][0]))
				config.set("R1", "key_x2_image_2", str(point[1][0]))
				config.set("R1", "key_y1_image_2", str(point[0][1]))
				config.set("R1", "key_y2_image_2", str(point[1][1]))
				config.write(open('ROI.ini', 'wb'))
			elif k == 2: # 設定 ROI 1  
				config = ConfigParser.ConfigParser()
				config.optionxform = str
				config.read('ROI.ini')
				total_section = config.sections()
				config.set("R1", "key_x1_roi_1", str(point[0][0]))
				config.set("R1", "key_x2_roi_1", str(point[1][0]))
				config.set("R1", "key_y1_roi_1", str(point[0][1]))
				config.set("R1", "key_y2_roi_1", str(point[1][1]))
				config.write(open('ROI.ini', 'wb'))
			elif k == 22: # 設定 ROI 1  
				config = ConfigParser.ConfigParser()
				config.optionxform = str
				config.read('ROI.ini')
				total_section = config.sections()
				config.set("R1", "key_x1_roi_2", str(point[0][0]))
				config.set("R1", "key_x2_roi_2", str(point[1][0]))
				config.set("R1", "key_y1_roi_2", str(point[0][1]))
				config.set("R1", "key_y2_roi_2", str(point[1][1]))
				config.write(open('ROI.ini', 'wb'))
		if len(point) == 3:
			cv2.destroyWindow("image")
	cf = ConfigParser.ConfigParser()
	cf.read("ROI.ini")
	# ------------------------------- # 
	if k == 3 or k == 2: # 射出前
		img1 = cv2.imread("102.png")
		image = img1.copy()
	elif k == 33 or k == 22:# 閉模前
		img1 = cv2.imread("104.png")
		image = img1.copy()
	cv2.namedWindow("image", cv2.WND_PROP_FULLSCREEN)
	cv2.imshow("image", img1)
	cv2.setWindowProperty("image", cv2.WND_PROP_FULLSCREEN,True) # 螢幕最大化
	cv2.setMouseCallback("image", click_and_crop)
	cv2.waitKey(0)



if __name__ == "__main__":
	get_ROI(33)
