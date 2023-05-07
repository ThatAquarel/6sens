import cv2
from deepsparse import Pipeline

# create Pipeline
yolo_pipeline = Pipeline.create(
    task="yolo",
    model_path="./yolov8n.onnx",
)

# Open the video file
video_path = "pedestrians.mp4"
cap = cv2.VideoCapture(video_path)

# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLOv8 inference on the frame
        results = yolo_pipeline(images=frame, iou_thres=0.6, conf_thres=0.001)

        # Visualize the results on the frame
        annotated_frame = results[0]

        # Display the annotated frame
        cv2.imshow("YOLOv8 Inference", frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()
