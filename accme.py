import cv2

# Connect to the default camera (index 0)
cap = cv2.VideoCapture(0)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error opening video stream or file")

while True:
    # Read a frame from the video
    ret, frame = cap.read()

    # If frame is read correctly, ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # Display the frame
    cv2.imshow('Frame', frame)

    # Wait for a key press
    if cv2.waitKey(1) == ord('q'):
        break

# Release the video capture object
cap.release()

# Close all OpenCV windows
cv2.destroyAllWindows()

# from roboflow import Roboflow

# rf = Roboflow(api_key="M7l0563sUMmr5TLOFfPH")
# project = rf.workspace().project("handicap-1uz0n")
# model = project.version("1").model

# job_id, signed_url, expire_time = model.predict_video(
#     "YOUR_VIDEO.mp4",
#     fps=5,
#     prediction_type="batch-video",
# )

# results = model.poll_until_video_results(job_id)

# print(results)