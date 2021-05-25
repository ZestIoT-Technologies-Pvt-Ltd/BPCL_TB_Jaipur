import cv2
import numpy as np

x_prev, y_prev = 0, 0

def helmet(img) :
	global x_prev, y_prev
	number_motion = 0
	mask = np.zeros(img.shape[:2], np.uint8)
	#pts = np.array([[566,504],[590,264], [870,305],[870,504]])
	#pts = np.array([[535,365],[660,360], [650,432],[534,439]]) #jaipur_new
	#pts = np.array([[508,352],[660,342], [666,435],[508,442]]) #jaipur_new
	pts = np.array([[420,367],[760,340], [760,451],[410,453]]) #jaipur_neww
	cv2.drawContours(mask, [pts], -1, (255, 255, 255), -1, cv2.LINE_AA)
	dst = cv2.bitwise_and(img, img, mask=mask)
	dst = cv2.cvtColor(dst, cv2.COLOR_BGR2HSV)
	lower = np.array([22, 70, 0], dtype="uint8")
	upper = np.array([45, 255, 255], dtype="uint8")
	dst = cv2.inRange(dst, lower, upper)
	pixels = np.sum(dst == 255)
	#print("pixels=====>",pixels)
	if pixels > 2000 :
		output = True
		cnts = cv2.findContours(dst, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		cnts = cnts[0] if len(cnts) == 2 else cnts[1]

		c = max(cnts, key = cv2.contourArea)
		x,y,w,h = cv2.boundingRect(c)
		x = x + (w/2)
		y = y + (h/2)
		x_abs = abs(x - x_prev)
		y_abs = abs(y - y_prev)
		x_prev = x
		y_prev = y

		if x_abs >= 5 or y_abs >=5 :
			number_motion = 1
	else :
		output = False
	return output, number_motion

