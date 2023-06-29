import cv2
import numpy as np
import matplotlib.pyplot as plt


video_file = "/path/to/video/file"

# Set start and end frame
fps = 10 # set the fps of video
start_frame = int(10 * fps)
end_frame = int(15 * fps)

# Load the video
cap = cv2.VideoCapture(video_file)

# Set the video position to the desired start time (10s)
start_time = 10
fps = cap.get(cv2.CAP_PROP_FPS)
cap.set(cv2.CAP_PROP_POS_FRAMES, int(start_time * fps))

# Read the first frame of the selected time range
ret, frame = cap.read()
if not ret:
    print("Failed to read the video file.")
    cap.release()
    exit()

# Resize the frame to fit the screen
screen_res = 720, 720
scale_width = screen_res[0] / frame.shape[1]
scale_height = screen_res[1] / frame.shape[0]
scale = min(scale_width, scale_height)
window_width = int(frame.shape[1] * scale)
window_height = int(frame.shape[0] * scale)
frame = cv2.resize(frame, (window_width, window_height), interpolation=cv2.INTER_AREA)


# Function to handle mouse events
def select_line(event, x, y, flags, param):
    global line_start, line_end, selecting, temp_frame
    
    if event == cv2.EVENT_LBUTTONDOWN:
        if not selecting:
            line_start = (x, y)
            selecting = True
        else:
            line_end = (x, y)
            selecting = False
            cv2.destroyAllWindows()
    elif event == cv2.EVENT_MOUSEMOVE and selecting:
        temp_frame = frame.copy()
        cv2.line(temp_frame, line_start, (x, y), (0, 255, 0), 1)

# Show the first frame and let the user select the line
cv2.namedWindow("Select Line")
cv2.setMouseCallback("Select Line", select_line)

selecting = False
line_start = None
line_end = None
temp_frame = frame.copy()

while line_start is None or line_end is None:
    cv2.imshow("Select Line", temp_frame)
    cv2.waitKey(1)

# Create an empty kymograph array
kymograph = []

# Loop through the video frames
for i in range(start_frame, end_frame):
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Resize the frame
    gray_frame = cv2.resize(gray_frame, (window_width, window_height), interpolation=cv2.INTER_AREA)

    # Extract pixel intensity values along the line of interest
    pt1, pt2 = line_start, line_end
    line_length = int(np.sqrt((pt2[1] - pt1[1]) ** 2 + (pt2[0] - pt1[0]) ** 2))
    x_values = np.linspace(pt1[0], pt2[0], line_length).astype(int)
    y_values = np.linspace(pt1[1], pt2[1], line_length).astype(int)

    intensity_values = gray_frame[y_values, x_values]

    # Append intensity values to the kymograph
    kymograph.append(intensity_values)

# Release the video capture
# Release the video capture object
cap.release()

# Convert the kymograph to a NumPy array
kymograph = np.array(kymograph)

# Plot the kymograph
fig = plt.figure()
plt.imshow(kymograph, cmap="gray", aspect="auto")
# plt.xlabel("Position along the line")
# plt.ylabel("Time (s)")

plt.xlabel('$Distance, [pixel]$', fontsize=20)
plt.ylabel('$Time, [s]$', fontsize=20)  # LaTeX font

# Set y-axis ticks to display time in seconds
frame_duration = 1 / fps
# y_ticks = np.arange(0, kymograph.shape[0], fps // 2)
# y_tick_labels = [f"{tick * frame_duration:.1f}" for tick in y_ticks]
# plt.yticks(y_ticks, y_tick_labels, fontsize=20)

# Set y-axis ticks to display time in seconds
y_ticks = np.array([0, 1, 2, 3, 4])  # Your desired y-tick locations
y_tick_labels = y_ticks  # Create corresponding labels
plt.yticks(y_ticks * fps, y_tick_labels, fontsize=20)  # Apply the new ticks


# Set the font size of xticks
plt.xticks([0,50,100,150], fontsize=20)
plt.colorbar()
# plt.axis('square')

fig.tight_layout()
plt.show()