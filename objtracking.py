import cv2
import numpy as np
from tkinter import *
from tkinter import colorchooser

def getColor():
	import tkinter as tk
	from tkinter.colorchooser import askcolor
	win = None
	if not tk._default_root:
		win = tk.Tk()
		win.wm_withdraw()
	color = askcolor()
	if win is not None: 
		win.destroy()
	return color

rgb, hexcode = getColor()
print(rgb, hexcode)

color = np.uint8([[[rgb[2], rgb[1], rgb[0]]]])

hsv_color = cv2.cvtColor(color, cv2.COLOR_BGR2HSV)

hue = hsv_color[0][0][0]
print(hue)


low = np.array([hue-10, 60, 10])
high = np.array([hue+10, 255, 255])
print(low, high)

#change parameter to zero to capture from webcam
vid = cv2.VideoCapture('vid.mp4')

filter = np.ones((5,5),np.uint8)

s, videoFrame= vid.read()
height , width , layers =  videoFrame.shape
print(height, width)


fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
out = cv2.VideoWriter('output.mp4', fourcc, 10.0, (width, height))
outC = cv2.VideoWriter('outputC.mp4', fourcc, 10.0, (width, height))
dir_path = '.'
while(True):
	ret, frame = vid.read()
	if ret == False:
		break
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

	b = cv2.GaussianBlur(frame, (41, 41), 0)
	# blurred = cv2.medianBlur(b,31)
	hsv = cv2.cvtColor(b, cv2.COLOR_BGR2HSV)

	# cv2.imshow(" ", hsv)
	# cv2.waitKey()
	# break;

	mask = cv2.inRange(hsv, low, high)
	mask = cv2.erode(mask, filter, iterations=4)
	mask = cv2.dilate(mask, filter, iterations=4)

	image=cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
	# cv2.imshow(" ", image)
	# cv2.waitKey()
	# break;
	out.write(image)
	contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
	if contours:
		contours=cv2.drawContours(frame.copy(), contours, -1, (255,0,255), 3)
	else:
		contours=cv2.drawContours(frame.copy(), [np.array([[0,0], [0,0], [0,0]])], -1, (0,255,0), 3)
	cv2.imshow('Frame',contours)

	outC.write(contours)

vid.release()
out.release()
cv2.destroyAllWindows()