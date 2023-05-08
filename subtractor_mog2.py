import cv2
import numpy as np

cap = cv2.VideoCapture("test.mp4")

subtractor = cv2.createBackgroundSubtractorMOG2(history=200, varThreshold=190, detectShadows=True)

while True:
    _, frame = cap.read()

    mask = subtractor.apply(frame)
    mask_rgb = cv2.bitwise_not(frame,frame,mask=~mask)
    mask_sub = cv2.bitwise_not(mask_rgb,mask,mask=mask)

    cv2.imshow("Frame", frame)
    cv2.imshow("mask", mask)
    cv2.imshow("Difference", mask_sub)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
