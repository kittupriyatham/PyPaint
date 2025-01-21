import cv2
import numpy as np
import os
import HandTrackingModule as htm

cap = None
print("Press 'Ctrl + C' to exit the program")
try:
    brushThickness = 15
    eraserThickness = 30
    folderPath = "images/header"
    myList = os.listdir(folderPath)
    overlayList = []
    for inPath in myList:
        image = cv2.imread(f'{folderPath}/{inPath}')
        overlayList.append(image)

    header = overlayList[0]
    header = cv2.resize(header, (1280, 124))
    drawColor = tuple(map(int, header[62][80]))
    print("initial colour selected: violet")

    folderPath2 = "images"
    myList2 = os.listdir(folderPath2)
    # print("mylist", myList2)
    overlayList2 = []
    for inPath2 in myList2:
        # print("inpath2", inPath2)
        image2 = cv2.imread(f'{folderPath2}/{inPath2}')
        overlayList2.append(image2)

    # print("overlaylist2", overlayList2)

    closer = overlayList2[0]
    closer = cv2.resize(closer, (160, 422))

    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)

    xp, yp = 0, 0
    detector = htm.handDetector(detectionCon=0.85)
    imgCanvas = np.zeros((720, 1280, 3), dtype=np.uint8)

    while True:
        print("Press 'Ctrl + C' to exit the program")
        print("initial colour selected: violet")
        success, img = cap.read()
        img = cv2.flip(img, 1)
        img = detector.findHands(img)
        lmList = detector.findPosition(img, draw=False)

        if len(lmList) != 0:

            x1, y1 = lmList[8][1:]
            x2, y2 = lmList[12][1:]
            fingers = detector.fingersUp()

            if fingers[1] and fingers[2]:
                # print("Selection Mode")
                if y1 < 124:
                    if  0 <= x1 < 160:
                        print("violet")
                        header = overlayList[0]
                        drawColor = tuple(map(int, header[62][80]))#(250, 70, 5)
                    elif 160 <= x1 < 320:
                        print("indigo")
                        header = overlayList[1]
                        drawColor = tuple(map(int, header[62][240]))#(250, 5, 234)
                    elif 320 <= x1 < 480:
                        print("blue")
                        header = overlayList[2]
                        drawColor = tuple(map(int, header[62][400]))#(56, 182, 255)
                    elif 480 <= x1 < 640:
                        print("green")
                        header = overlayList[3]
                        drawColor = tuple(map(int, header[62][560]))#(56, 182, 255)
                    elif 640 <= x1 < 800:
                        print("yellow")
                        header = overlayList[4]
                        drawColor = tuple(map(int, header[62][720]))#(56, 182, 255)
                    elif 800 <= x1 < 960:
                        print("orange")
                        header = overlayList[5]
                        drawColor = tuple(map(int, header[62][880]))#(56, 182, 255)
                    elif 960 <= x1 < 1120:
                        print("red")
                        header = overlayList[6]
                        drawColor = tuple(map(int, header[62][1040]))#(56, 182, 255)
                    elif 1120 <= x1 <= 1280:
                        print("eraser")
                        header = overlayList[7]
                        drawColor = (0, 0, 0)
                elif y1 > 422:
                    if x1 > 1120:
                        print("closing")
                        cv2.destroyAllWindows()
                        cap.release()
                        exit()

                cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor)

            if fingers[1] and fingers[2] == False:
                cv2.circle(img, (x1, y1), 15, drawColor)
                # print("Drawing Mode")
                if xp == 0 and yp == 0:
                    xp, yp = x1, y1
                if drawColor == (0, 0, 0):
                    mask = cv2.inRange(imgCanvas, drawColor, drawColor)
                    imgCanvas = cv2.bitwise_and(imgCanvas, imgCanvas, mask=mask)
                else:
                    cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)
                    print("line drawn from", (xp, yp), "to", (x1, y1), "on imgcanvas with color", drawColor,  "and thickness", brushThickness)
                xp, yp = x1, y1

        target_width = header.shape[1]
        img[0:124, 0:target_width] = header
        img = cv2.add(img.astype(np.float32), imgCanvas.astype(np.float32))
        img = np.clip(img, 0, 255).astype(np.uint8)

        target_width2 = closer.shape[1]
        img[298:, 1120:] = closer
        img = cv2.add(img.astype(np.float32), imgCanvas.astype(np.float32))
        img = np.clip(img, 0, 255).astype(np.uint8)

        cv2.imshow("Image", img)
        cv2.waitKey(1)
except KeyboardInterrupt:
    cv2.destroyAllWindows()
    cap.release()
    exit()
except Exception as e:
    print(e)
    # cv2.destroyAllWindows()
    # cap.release()
    exit()
