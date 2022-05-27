# <a href="https://thinkinfi.com/basic-python-opencv-tutorial-function/" data-internallinksmanager029f6b8e52c="14" title="OpenCV" target="_blank" rel="noopener">opencv</a> object tracking
# object detection and tracking <a href="https://thinkinfi.com/basic-python-opencv-tutorial-function/" data-internallinksmanager029f6b8e52c="14" title="OpenCV" target="_blank" rel="noopener">opencv</a>

import cv2
import numpy as np


    

 
# Loading image

 
# Load Yolo
def yolo(imag):
    yolo_weight = 'yolov3-obj_30000.weights'#'./weights/yolov3.weights'
    yolo_config = 'yolov3-obj.cfg'#'yolov3-obj.cfg'#'.
    coco_labels = 'data/coco.names'
    net = cv2.dnn.readNet(yolo_weight, yolo_config)
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
    
    classes = []
    with open(coco_labels, "r") as f:
        classes = [line.strip() for line in f.readlines()]
    
    # print(classes)
    
    # # Defining desired shape
    fWidth = 320
    fHeight = 320 
    # Resize image in opencv

    #img = cv2.imread('45118af1-37d2-4a02-92af-656e76685986.jpg')
    #imag = cv2.resize(imag,(500,500))
    img = cv2.cvtColor(imag,cv2.COLOR_BGR2HSV)
    #img = imag 
    height, width, channels = img.shape

    # Convert image to Blob
    blob = cv2.dnn.blobFromImage(img, 1/255, (fWidth, fHeight), (0, 0, 0), True, crop=False)
    # Set input for YOLO object detection
    net.setInput(blob)

    # Find names of all layers
    layer_names = net.getLayerNames()
    # print(layer_names)
    # Find names of three output layers
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    # print(output_layers)

    # Send blob data to forward pass
    outs = net.forward(output_layers)
    # print(outs[0].shape)
    # print(outs[1].shape)
    # print(outs[2].shape)

    # Generating random color for all 80 classes
    #colors = np.random.uniform(0, 255, size=(len(classes), 3))

    # Extract information on the screen
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        i = 0 
        for detection in out:
            # Extract score value
            scores = detection[5:]
            # Object id
            class_id = np.argmax(scores)
            # Confidence score for each object ID
            confidence = scores[class_id]
            # if confidence > 0.5 and class_id == 0:
            if confidence > 0.5:
                # Extract values to draw bounding box
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                #cv2.rectangle(img, (x, y), (x + w, y + h), [255,0,0], 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)


    #Draw bounding box with text for each object
    font = cv2.FONT_HERSHEY_DUPLEX
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            if True :#label != 'person':
                confidence_label = int(confidences[i] * 100)
                if confidence_label>90 and w*h <20000:
                    #color = colors[i]
                    #i = i+1
                    #print(i)
                    cv2.rectangle(imag, (x, y), (x + w, y + h), [0,0,255], 2)
                    box1 = img[y:y+h,x:x+w]
                    #center = Circle_ded(box1,[],x,y)
                    #print()
                    #cv2.putText(img, f'{label, confidence_label}', (x-25, y + 75), font, 1, [255,0,0], 2)
    return imag
    #cv2.imshow('img',img)