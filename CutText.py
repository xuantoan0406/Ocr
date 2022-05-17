import cv2
import numpy as np
import imutils
import os

from vietocr.tool.predictor import Predictor
from vietocr.tool.config import Cfg
from PIL import Image
import time


def get_region(pathImg):
	folder, file = os.path.split(pathImg)
	img = cv2.imread(pathImg)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	th, threshed = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 25))
	dilation = cv2.dilate(threshed, kernel=kernel, iterations=1)
	opening = cv2.morphologyEx(threshed, cv2.MORPH_OPEN, kernel, iterations=4)
	
	contours, _ = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	for cnt in contours:
		if cv2.contourArea(cnt)>500:
			x, y, w, h = cv2.boundingRect(cnt)
			cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
	cv2.imwrite(f"region/{file}",img)
# config = Cfg.load_config_from_name('vgg_seq2seq`')
# config['device'] = 'cpu'
# detector = Predictor(config)

# img = 'Screenshot 2022-04-20 161451.png'
# img = Image.open(img)
# # dự đoán
# st=time.time()
# s = detector.predict(img, return_prob=True)
st=time.time()
def draw_boundingBox(pathImg):
	imagePil=Image.open(pathImg)
	folder,file=os.path.split(pathImg)
	img = cv2.imread(pathImg)
	# 1682*2378

	img=cv2.resize(img,(1682,2378))
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	th, threshed = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
	
	blurred = cv2.GaussianBlur(gray, (5, 5), 0)
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 3))
	dilation = cv2.dilate(threshed, kernel=kernel, iterations=1)
	# kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 1))
	opening = cv2.morphologyEx(threshed, cv2.MORPH_OPEN, kernel, iterations=4)
	
	contours, _ = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	# contours=sorted(contours, key=lambda x: x[0])
	# cv2.drawContours(img,contours,-1,(0,0,255),2)
	fullBox=[]
	fullText=[]
	j=0
	for cnt in contours:
		if cv2.contourArea(cnt)>900:
			x, y, w, h = cv2.boundingRect(cnt)
			fullBox.append((x,y,x+w,y+h))
			cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
	
	fullBox = sorted(fullBox, key=lambda x: x[1])
	# for box in fullBox:
	# 	imageN = imagePil.crop(box)
	# 	# imageN.show()
	# 	text = detector.predict(imageN, return_prob=True)
	# 	print(text[0])
	# 	j += 1
	# 	fullText.append(text[0])
	# print(len(fullText))
	cv2.imwrite(f"boxOut/{file}",img)
for path in os.listdir("image"):
	print(path)
	draw_boundingBox(os.path.join("image", path))
## (2) threshold
# th, threshed = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
# pts = cv2.findNonZero(threshed)
# ret = cv2.minAreaRect(pts)
#
# (cx, cy), (w, h), ang = ret
# if w > h:
# 	w, h = h, w
# 	ang += 90
#
# ## (4) Find rotated matrix, do rotation
# M = cv2.getRotationMatrix2D((cx, cy), ang, 1.0)
# rotated = cv2.warpAffine(threshed, M, (img.shape[1], img.shape[0]))
# rotated=cv2.rotate(rotated, cv2.ROTATE_180)
# cv2.imshow("a",imutils.resize(img,height=900))
# cv2.waitKey()

draw_boundingBox("image/letter_21.png")
print(time.time()-st)