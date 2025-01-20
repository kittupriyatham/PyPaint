import cv2
import numpy as np
import os
import HandTrackingModule as htm

brushThickness = 15
eraserThickness = 30

folderPath = "Header"

myList = os.listdir(folderPath)
overlayList = []
for inPath in myList:
    image = cv2.imread(f'{folderPath}/{inPath}')
    overlayList.append(image)
print(len(overlayList))

header = overlayList[0]
header = cv2.resize(header, (1280, 124)) 
drawColor = (255, 49, 49)

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = htm.handDetector(detectionCon=0.85)
xp, yp = 0, 0

imgCanvas = np.zeros((720, 1280, 3), dtype=np.uint8) 

while True:

    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:

        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        fingers = detector.fingersUp()

        if fingers[1] and fingers[2]:
            print("Selection Mode")
            if y1 < 124:
                if 50 < x1 < 250:
                    header = overlayList[0]  
                    drawColor = (250, 70, 5)
                elif 370 < x1 < 640:
                    header = overlayList[1]  
                    drawColor = (250, 5, 234) 
                elif 700 < x1 < 970:
                    header = overlayList[2]  
                    drawColor = (56, 182, 255) 
                elif 1050 < x1 < 1280:
                    header = overlayList[3]  
                    drawColor = (0, 0, 0) 

            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor)

        if fingers[1] and fingers[2] == False:
            cv2.circle(img, (x1, y1), 15, drawColor)
            print("Drawing Mode")
            if xp == 0 and yp == 0:
                xp, yp = x1, y1
            if drawColor == (0, 0, 0):  
                mask = cv2.inRange(imgCanvas, drawColor, drawColor)
                imgCanvas = cv2.bitwise_and(imgCanvas, imgCanvas, mask=mask)
            else:  
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)
            xp, yp = x1, y1

    target_width = header.shape[1] 
    img[0:124, 0:target_width] = header 
    img = cv2.add(img.astype(np.float32), imgCanvas.astype(np.float32))
    img = np.clip(img, 0, 255).astype(np.uint8)  

    cv2.imshow("Image", img)
    cv2.waitKey(1)