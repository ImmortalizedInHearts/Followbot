import cv2
import numpy as np

def empty(arg):
    pass

cap = cv2.VideoCapture(0)
cv2.namedWindow("TrackBars")
cv2.resizeWindow("TrackBars", 640, 350)
cv2.createTrackbar("Hue Min", "TrackBars", 20, 179, empty)
cv2.createTrackbar("Sat Min", "TrackBars", 84, 255, empty)
cv2.createTrackbar("Val Min", "TrackBars", 132, 255, empty)
cv2.createTrackbar("Hue Max", "TrackBars", 33, 179, empty)
cv2.createTrackbar("Sat Max", "TrackBars", 255, 255, empty)
cv2.createTrackbar("Val Max", "TrackBars", 255, 255, empty)

def getContours(frame, center):
    contours, hierarchy = cv2.findContours(frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    leftBorder = rightBorder = center
    area = 5000
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 1500:
            cv2.drawContours(frameContours, cnt, -1, (0,255,0), 1)
            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
            objCor = len(approx)
            if objCor > 4:
                x, y, width, hight = cv2.boundingRect(approx)
                cv2.rectangle(frameContours, (x, y), (x + width, y + hight), (0,0,255),3)
                leftBorder = [x , (y + hight)//2]
                rightBorder = [x + width , (y + hight)//2]
                return leftBorder, rightBorder, area
    return leftBorder, rightBorder, area

def bordersDrawing(img):
    shakingConstant = 100
    imgHight, imgWeight, _ = np.shape(img)
    centerOfImg = [int(imgWeight/2), int(imgHight/2)]
    shakingBorders = [centerOfImg[0] + shakingConstant, centerOfImg[0] - shakingConstant]
    return centerOfImg, shakingBorders

def motionManaging(img, left, right, center, shake, area):
    cv2.line(img,(shake[0], 0), (shake[0], center[0] * 2), (255, 255, 255), 3) 
    cv2.line(img,(center[0], 0), (center[0], center[0] * 2), (0, 0, 255), 3) 
    cv2.line(img,(shake[1], 0), (shake[1], center[0] * 2), (255, 255, 255), 3)

    if area <= 3000 and area > 1500:
        print("FORWARD!!!")
    elif area > 10000:
        print("BACKWARD!!!")
    elif left[0] >= shake[0]:
        print("TURN RIGHT!!!")
    elif right[0] <= shake[1]:
        print("TURN LEFT!!!")
    else:
        print("STOP!!!")



while True:
    success, frame = cap.read()
    # frame = cv2.imread("test.png")
    frameContours = frame.copy()
    center, shake = bordersDrawing(frameContours)
    frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frameBlur = cv2.GaussianBlur(frameGray, (7,7), 1)
    frameCanny = cv2.Canny(frameBlur, 50, 50)
    # getContours(frameCanny)
    frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    h_min = cv2.getTrackbarPos("Hue Min", "TrackBars")
    h_max = cv2.getTrackbarPos("Hue Max", "TrackBars")
    s_min = cv2.getTrackbarPos("Sat Min", "TrackBars")
    s_max = cv2.getTrackbarPos("Sat Max", "TrackBars")
    v_min = cv2.getTrackbarPos("Val Min", "TrackBars")
    v_max = cv2.getTrackbarPos("Val Max", "TrackBars")

    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(frameHSV, lower, upper)
    left, right, area = getContours(mask, center)
    frameResult = cv2.bitwise_and(frame,frame, mask=mask)
    motionManaging(frameContours, left, right, center, shake, area)
    cv2.imshow("frame color", frameResult)
    cv2.imshow("frame сanny", frameCanny)
    cv2.imshow("frame contours", frameContours)
    # cv2.imshow("frame", mask)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break