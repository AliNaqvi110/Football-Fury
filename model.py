import os
import sqlite3
import av
from ultralytics import YOLO
import numpy as np
from collections import defaultdict
from collections import deque
import supervision as sv
import cv2
from create_database import create_table, insert_data



#Store data points in a database
def store_databse(X, Y):
    # Database connection (replace with your desired path)
    db_path = "data.db"

    # Check if database file exists (optional)
    if not os.path.exists(db_path):
        # Create the database file if it doesn't exist
        conn = sqlite3.connect(db_path)
        # print("Database created successfully!")  # Optional: Confirmation 
        
        # Table definition
        table_name = "Football_data"

        # Create the table if it doesn't exist
        create_table(conn, table_name)
        # print("Table created successfully!")  # Optional: Confirmation 
        conn.close()

    else:
        # insert data into table
        conn = sqlite3.connect(db_path)
        table_name = "Football_data"
        insert_data(conn, table_name, X, Y)
        print("Inserted")
        conn.close()


def callback(frame):
    img = frame.to_ndarray(format="bgr24")

    conf = 0.3
    iou = 0.7
    # Load YOLOv8 model
    model = YOLO("yolov8s.pt")
    # Create ByteTrack object for tracking
    byte_track = sv.ByteTrack(frame_rate=25, track_activation_threshold=conf)

    print(-1)
    thickness = sv.calculate_dynamic_line_thickness(resolution_wh=(frame.width, frame.height))
    text_scale = sv.calculate_dynamic_text_scale(resolution_wh=(frame.width, frame.height))
    bounding_box_annotator = sv.BoundingBoxAnnotator(thickness=thickness)
    label_annotator = sv.LabelAnnotator(
        text_scale=text_scale, text_thickness=thickness, text_position=sv.Position.BOTTOM_CENTER
    )
    trace_annotator = sv.TraceAnnotator(
    thickness=thickness, trace_length=50, position=sv.Position.BOTTOM_CENTER
    )

    # Dictionary to store coordinates for speed calculation
    coordinates = defaultdict(lambda: deque(maxlen=25))

    print(0)


    # Perform object detection with YOLO
    result = model(img, classes=[0, 32])[0]
    print(1)

    # Convert detections to supervision format (assuming you're using supervision)
    detections = sv.Detections.from_ultralytics(result)
    # print(detections)
    # print(detections.data['class_name'])
    # Extract the class name array from the data attribute
    class_names = detections.data['class_name']

    # Now, class_names contains the array of class names
    print(class_names)
    # Iterate over class names and check if they are 'sports ball'
    for i, name in enumerate(class_names):
        if name == 'sports ball':
            # Extract XY coordinates for the detected 'sports ball'
            xy_coordinates = detections.xyxy[i:i+1]  # Extract coordinates for the i-th detection only

            # Calculate center X and center Y coordinates for the 'sports ball'
            center_x = (xy_coordinates[:, 0] + xy_coordinates[:, 2]) / 2  # (x_min + x_max) / 2
            center_y = (xy_coordinates[:, 1] + xy_coordinates[:, 3]) / 2  # (y_min + y_max) / 2
            store_databse(center_x, center_y)
    print(2)


    # Skip detections below confidence threshold (optional)
    detections = detections[detections.confidence > conf]
    print(3)

    # Update tracks with detections
    detections = byte_track.update_with_detections(detections=detections)
    print(4)

    # Get Y-coordinates of bottom center points for speed calculation
    points = detections.get_anchors_coordinates(anchor=sv.Position.BOTTOM_CENTER)
    print(5)
    print(detections)
    # for class_name in detections["class_name"]:
    #     if class_name == 'sports ball':
    #         print("Football")
    # Update coordinates dictionary and calculate speed
    labels = []  # Initialize labels list within the loop
    for tracker_id, [_, y] in zip(detections.tracker_id, points):
        coordinates[tracker_id].append(y)

        # if len(coordinates[tracker_id]) < video_info.fps / 2:
        #     continue

        coordinate_start = coordinates[tracker_id][-1]
        coordinate_end = coordinates[tracker_id][0]
        distance = abs(coordinate_start - coordinate_end)
        time = len(coordinates[tracker_id]) / 25
        print("Distance = ", distance)
        print("Time = ", time)
        speed = (distance / time) 
        print(speed)

        # Prepare label with tracker ID and speed
        label = f"{int(speed)} m/s"
        print("kkkkkkkkkkkkkk")
        print(label)
        labels.append(label)

    # Annotate frame with bounding boxes, labels, and traces
    annotated_frame = img.copy()
    annotated_frame = trace_annotator.annotate(scene=annotated_frame, detections=detections)
    annotated_frame = bounding_box_annotator.annotate(scene=annotated_frame, detections=detections)
    annotated_frame = label_annotator.annotate(scene=annotated_frame, detections=detections, labels=labels)

    # # Prepare labels with confidence scores
    # labels = [f"{class_name} ({confidence:.2f})" 
    #  for class_name, confidence in zip(detections.data['class_name'], detections.confidence)]


    # # Annotate frame with supervision (assuming compatible format)
    # annotated_frame = img.copy()
    # annotated_frame = bounding_box_annotator.annotate(scene=annotated_frame, detections=detections)
    # annotated_frame = label_annotator.annotate(scene=annotated_frame, detections=detections, labels=labels)
    print(6)

    # Convert the annotated frame back to av.VideoFrame format
    annotated_frame = annotated_frame[:, :, ::-1]  # Convert BGR to RGB
    annotated_frame = annotated_frame.copy(order='C')  # Ensure contiguous memory layout
    print(7)
    
    # Save the annotated frame to an image file
    cv2.imwrite('annotated_frame.jpg', annotated_frame)
    print(8)
    return av.VideoFrame.from_ndarray(annotated_frame, format="rgb24")

