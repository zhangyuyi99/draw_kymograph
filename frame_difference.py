import cv2
import numpy as np

video_file = "/path/to/video/file"

# Load the video
cap = cv2.VideoCapture(video_file)

# Get video properties
fps = int(cap.get(cv2.CAP_PROP_FPS))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Create the video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('frame_difference.mp4', fourcc, fps, (width, height), isColor=True)

if not out.isOpened():
    print("Failed to open the video writer.")
    cap.release()
    exit()

# Read the first frame of the video
ret, prev_frame = cap.read()
if not ret:
    print("Failed to read the video file.")
    cap.release()
    exit()

# Convert the first frame to grayscale
prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

# Loop through the video frames
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Calculate the frame difference
    frame_diff = cv2.absdiff(gray, prev_gray)

    # Write the frame difference to the output video
    out.write(cv2.cvtColor(frame_diff, cv2.COLOR_GRAY2BGR))

    # Update the previous frame
    prev_gray = gray

# Release the video capture and writer objects
cap.release()
out.release()
