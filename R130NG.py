# -*- coding: utf-8 -*-

import cv2
import numpy as np
import image_ccd

def click_and_crop2(event, x, y, flags, param):
	if event == cv2.EVENT_LBUTTONDOWN:
		cv2.destroyWindow("NG")
		rq = image_ccd.client.write_registers(0x7e,[2266],unit=0x01) #R126
		rq = image_ccd.client.write_registers(0x80,[0],unit=0x01)    #R128
		print 666

def run():  # match display
    image = cv2.imread("103NG.jpg")
    cv2.namedWindow("NG", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("NG", cv2.WND_PROP_FULLSCREEN,True) # 螢幕最大化
    cv2.imshow("NG",image)
    cv2.setMouseCallback("NG", click_and_crop2)
    cv2.waitKey(0)
    
if __name__ == "__main__":
    run()
