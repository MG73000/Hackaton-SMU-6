import cv2
import moviepy.editor as mp
import os
import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk

try:
    print("Test: Importing packages...")
    from inference_sdk import InferenceHTTPClient
    print("Test: Imports successful.")
except Exception as e:
    print(f"Test: Failed to import packages: {e}")
    exit(1)

# Debug: Start of the script
print("Starting the script...")

# Create an inference client
try:
    CLIENT = InferenceHTTPClient(
        api_url="https://detect.roboflow.com",
        api_key="v6lRlKHI5RbbU3qW56zk"
    )
    # Debug: Client successfully initialized
    print("Inference client initialized successfully.")
except Exception as e:
    print(f"Error initializing inference client: {e}")
    exit(1)  # Exit the script if client initialization fails

# Define the video path
video_path = "Input.mov"

# Check if the video exists
if not os.path.exists(video_path):
    print(f"Error: Video file '{video_path}' not found.")
    exit(1)  # Exit the script if video is not found

# Debug: Video file exists
print(f"Video file '{video_path}' found. Proceeding with processing...")

# Load the video
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error: Unable to open the video file.")
    exit(1)

frame_count = 0
frames = []

# Process each frame of the video
while cap.isOpened():
    ret, frame = cap.read()
    
    if not ret:
        print("Reached the end of the video or encountered a problem with frame reading.")
        break
    
    # Save the frame as an image (you can adjust the saving frequency if needed)
    frame_filename = f"frame_{frame_count}.png"
    cv2.imwrite(frame_filename, frame)
    
    # Debug: Saving and processing frame
    print(f"Processing frame {frame_count}...")
    
    # Run inference on the saved frame image
    try:
        # Debug: Starting inference
        print(f"Running inference on frame {frame_count}...")
        
        result = CLIENT.infer(frame_filename, model_id="engelli-park-yeri-n7wzb/1")
        
        # Debug: Inference completed
        if result:
            print(f"Inference result for frame {frame_count}:")
            print(result)
            
            # Draw squares around detected objects
            for obj in result['predictions']:
                x, y, w, h = obj['x'], obj['y'], obj['width'], obj['height']
                top_left = (int(x - w / 2), int(y - h / 2))
                bottom_right = (int(x + w / 2), int(y + h / 2))
                cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)
                
        else:
            print(f"No result returned from the API for frame {frame_count}.")
        
    except Exception as e:
        print(f"An error occurred during inference on frame {frame_count}: {e}")
    
    # Append the processed frame to the list
    frames.append(frame)
    
    # Increment frame counter
    frame_count += 1

# Release the video capture object
cap.release()

# Create a video from the processed frames
output_video_path = "output_video.mp4"
clip = mp.ImageSequenceClip([cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) for frame in frames], fps=24)
clip.write_videofile(output_video_path, codec='libx264')

print("Video processing and inference completed.")
print(f"Output video saved as '{output_video_path}'")

# Display the video in a GUI
def play_video():
    cap = cv2.VideoCapture(output_video_path)
    if not cap.isOpened():
        print("Error: Unable to open the video file.")
        return

    def update_frame():
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            lbl.imgtk = imgtk
            lbl.configure(image=imgtk)
            lbl.after(10, update_frame)
        else:
            cap.release()

    root = tk.Tk()
    root.title("Processed Video")
    lbl = Label(root)
    lbl.pack()
    update_frame()
    root.mainloop()

play_video()
