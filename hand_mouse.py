import cv2
import numpy as np
import mediapipe as mp
import time
import math
import autopy


class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            min_detection_confidence=float(self.detectionCon),
            min_tracking_confidence=float(self.trackCon))
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12]  # Thumb, Index, Middle

    def findHands(self, img, draw=False):  # Disabled hand skeleton drawing
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        return img

    def findPosition(self, img, handNo=0):
        self.lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy])

                # Draw fingertip dots
                if id in self.tipIds:
                    cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)  # Green dot on fingertips

        return self.lmList

    def fingersUp(self):
        fingers = []
        if len(self.lmList) == 0:
            return fingers  # Return empty list if no hands detected

        # Thumb
        if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        # Other finger
        for id in range(1, 3):
            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers

    def findDistance(self, p1, p2):
        if len(self.lmList) < max(p1, p2):
            return 0  # Avoid errors if hand is not detected
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        return math.hypot(x2 - x1, y2 - y1)


# Camera & Screen Setup
wCam, hCam = 700, 500
frameR = 100  # Frame reduction to limit cursor movement area
smoothening = 10  # Smooth cursor movement
plocX, plocY = 0, 0  # Previous cursor location
clocX, clocY = 0, 0  # Current cursor location
dragging = False  # Track drag & drop state

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = handDetector(maxHands=1)
wScr, hScr = autopy.screen.size()  # Get screen size

while True:
    success, img = cap.read()
    img = cv2.resize(img, (700, 500), interpolation=cv2.INTER_CUBIC)
    img = detector.findHands(img)
    lmList = detector.findPosition(img)

    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]  # Index finger tip
        x2, y2 = lmList[4][1:]  # Thumb tip
        fingers = detector.fingersUp()

        # Bounding box for gesture area
        cv2.rectangle(img, (10, 10), (wCam - 10, hCam - 10), (255, 0, 255), 2)

        # **Cursor Movement** (Only Index Finger Up)
        if fingers[1] == 1 and fingers[2] == 0:
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening
            autopy.mouse.move(wScr - clocX, clocY)  # Move cursor
            plocX, plocY = clocX, clocY  # Update previous location

        # **Left Click** (Pinch Gesture: Index + Thumb)
        if fingers[1] == 1 and fingers[0] == 1:
            length = detector.findDistance(8, 4)
            if length < 20:
                time.sleep(.2)
                autopy.mouse.click()

        # **Right Click** (Pinch Gesture: Middle Finger + Thumb)
        if fingers[2] == 1 and fingers[0] == 1:
            length = detector.findDistance(12, 4)
            if length < 20:
                time.sleep(.2)
                autopy.mouse.click(autopy.mouse.Button.RIGHT)


    # Display output
    img = cv2.flip(img, 1)
    cv2.imshow("Hand Gesture Mouse", img)
    if cv2.waitKey(1) & 0xFF == ord(" "):
        break

cap.release()
cv2.destroyAllWindows()
