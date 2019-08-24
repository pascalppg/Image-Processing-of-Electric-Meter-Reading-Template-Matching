# import the necessary packages
from imutils.perspective import four_point_transform
import pytesseract
import imutils
import cv2
import matplotlib.pyplot as plt
import numpy as np
import glob
from imutils import contours
from PIL import Image
import collections
import operator


image = cv2.imread("template6.JPG")

image = cv2.resize(image,(1768,768))

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
edged = cv2.Canny(blurred, 50, 200, 255)

cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
displayCnt = None


for c in cnts:
	peri = cv2.arcLength(c, True)
	approx = cv2.approxPolyDP(c, 0.02 * peri, True)
	if len(approx) == 4:
		displayCnt = approx
		break

output = four_point_transform(image, displayCnt.reshape(4, 2))
output = cv2.resize(output,(475,225))
output = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
output = cv2.bilateralFilter(output,9,20,20)

kernel = np.ones((8, 8), np.uint8)

opening = cv2.morphologyEx(output, cv2.MORPH_OPEN, kernel)

thresh = cv2.threshold(opening, 200, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

ret, thresh_image = cv2.threshold(thresh, 0, 255, cv2.THRESH_BINARY_INV)
new, conts, hierarchy = cv2.findContours(thresh_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
digitCnts = contours.sort_contours(conts, method="left-to-right")[0]


files1= glob.glob("tmp/*.jpg")

template_data={}
angka = []
output=[]
for (i,myfile) in enumerate (files1):
    imageTemp = cv2.imread(myfile,0)
    template_data[i]=imageTemp
hasil=[]
kirim=[]
ada=0
for cnt in digitCnts:
    ada = ada + 1
    x, y, w, h = cv2.boundingRect(cnt)
    out = thresh[y:y+h-2,x:x+w-2]
    out = cv2.resize(out, (94, 274))
    if ada <= 10 :
        cv2.imshow("Hasil.png", out)
        cv2.waitKey(0)
        groupOutput = []
        scores = []
        for (digit, tmp) in template_data.items():
            res = cv2.matchTemplate(out,tmp, cv2.TM_CCOEFF_NORMED)
            (_, score, _, _) = cv2.minMaxLoc(res)
            scores.append(score)
        groupOutput.append(str(np.argmax(scores)))
        print groupOutput
        hasil.extend(groupOutput)
kirim.append(hasil)
print("{}".format("".join(hasil)))
cv2.imshow("Stand Meter",thresh)
cv2.waitKey(0)
print kirim