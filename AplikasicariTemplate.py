# import the necessary packages
from imutils.perspective import four_point_transform
import imutils
import cv2
import matplotlib.pyplot as plt
import numpy as np
from imutils import contours

image = cv2.imread("citrabaru9.jpg")

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



thresh = cv2.threshold(opening, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
cv2.imwrite("thresh10.jpg",thresh)
ret, thresh_image = cv2.threshold(thresh, 0, 255, cv2.THRESH_BINARY_INV)
digitCnts = cv2.findContours(thresh_image.copy(), cv2.RETR_EXTERNAL,
                             cv2.CHAIN_APPROX_SIMPLE)
digitCnts = digitCnts[0] if imutils.is_cv2() else digitCnts[1]
digitCnts = contours.sort_contours(digitCnts, method="left-to-right")[0]
ada=0

for cnt in digitCnts:
    ada = ada + 1
    x, y, w, h = cv2.boundingRect(cnt)
    out = thresh[y:y+h-2,x:x+w-2]
    out = cv2.resize(out,(94,274))
    nf ="D:/template/" +str(ada)+".jpg"
    cv2.imwrite(nf,out)
plt.imshow(output)
plt.show()

# cv2.rectangle(warped, (x,y),(x + w, y + h), (255,192,128),2)