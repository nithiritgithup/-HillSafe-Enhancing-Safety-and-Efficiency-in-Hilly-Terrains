import cv2
import numpy as np
net = cv2.dnn.readNetFromDarknet('yolov4.cfg', 'yolov4.weights')
cap = cv2.VideoCapture("test.mp4")

# Get the names of all COCO classes
with open('coco.names', 'r') as f:
    classes = [line.strip() for line in f.readlines()]

# Get the index of the "car" class
car_index = classes.index('car')

# # Create an output video writer
# fourcc = cv2.VideoWriter_fourcc(*'mp4v')
# out = cv2.VideoWriter('output_video.mp4', fourcc, 30, (int(cap.get(3)), int(cap.get(4))))

def det(frame):
    blob = cv2.dnn.blobFromImage(frame, 1/255, (416, 416), swapRB=True, crop=False)

    # Set the input to the network
    net.setInput(blob)
    
    # Get the network's output
    output_layers = net.getUnconnectedOutLayersNames()
    layer_outputs = net.forward(output_layers)
    
    # Loop through the detections for each layer output
    for output in layer_outputs:
        for detection in output:
            # Get the class ID and confidence score for this detection
            class_id = np.argmax(detection[5:])
            confidence = detection[5:][class_id]
            
            # If this detection is for a car and its confidence is high enough, draw a bounding box around it
            if class_id == car_index and confidence > 0.5:
                center_x = int(detection[0] * frame.shape[1])
                center_y = int(detection[1] * frame.shape[0])
                width = int(detection[2] * frame.shape[1])
                height = int(detection[3] * frame.shape[0])
                x = int(center_x - width/2)
                y = int(center_y - height/2)
                
                cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 255, 0), 2)
                cv2.putText(frame,"not move",(x,y),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2,cv2.LINE_AA)

subtractor = cv2.createBackgroundSubtractorMOG2(history=200, varThreshold=10, detectShadows=True)

while True:
    _, frame = cap.read()

    mask = subtractor.apply(frame)
    mask_rgb = cv2.bitwise_not(frame,frame,mask=mask)
    det(frame)
    
    # Write the annotated frame to the output video
    #out.write(frame)

    cv2.imshow("Frame", frame)
    #cv2.imshow("mask", mask)
    #cv2.imshow("Difference", mask_rgb)
    #press "q" to exit
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
