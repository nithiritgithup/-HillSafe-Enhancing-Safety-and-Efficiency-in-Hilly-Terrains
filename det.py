import cv2
import numpy as np

# Constants
BLOB_SIZE = (416, 416)
CONFIDENCE_THRESHOLD = 0.5
CLASS_NAME = 'car'

net = cv2.dnn.readNetFromDarknet('E:\\BATCH 4\\project code\\yolov4.cfg', 'E:\\BATCH 4\\project code\\yolov4.weights')
cap = cv2.VideoCapture("E:\\BATCH 4\\project code\\test.mp4")

# Get the names of all COCO classes
with open('E:\\BATCH 4\\project code\\coco.names', 'r') as f:
    classes = [line.strip() for line in f.readlines()]

# Get the index of the class
class_index = classes.index(CLASS_NAME)

# Create a Background Subtractor
subtractor = cv2.createBackgroundSubtractorMOG2(history=200, varThreshold=10, detectShadows=True)

def detect_objects(frame):
    blob = cv2.dnn.blobFromImage(frame, 1 / 255, BLOB_SIZE, swapRB=True, crop=False)

    # Set the input to the network
    net.setInput(blob)

    # Get the network's output
    output_layers_names = net.getUnconnectedOutLayersNames()
    layer_outputs = net.forward(output_layers_names)

    # Loop through the detections for each layer output
    for output in layer_outputs:
        for detection in output:
            # Get the class ID and confidence score for this detection
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            # If this detection is for the specified class and its confidence is high enough, draw a bounding box around it
            if class_id == class_index and confidence > CONFIDENCE_THRESHOLD:
                center_x = int(detection[0] * frame.shape[1])
                center_y = int(detection[1] * frame.shape[0])
                width = int(detection[2] * frame.shape[1])
                height = int(detection[3] * frame.shape[0])
                x = int(center_x - width / 2)
                y = int(center_y - height / 2)

                cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 255, 0), 2)
                cv2.putText(frame, "not move", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

    return frame

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Apply background subtraction
    mask = subtractor.apply(frame)
    mask_rgb = cv2.bitwise_not(frame, frame, mask=mask)

    # Perform object detection on the frame
    frame = detect_objects(mask_rgb)

    # Show the annotated frame
    cv2.imshow("Frame", frame)

    # Press "q" to exit
    if cv2.waitKeyEx(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
