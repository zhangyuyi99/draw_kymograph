# Kymograph Generation

This project provides a graphical user interface (GUI) for generating kymographs from video files. A kymograph is a visual method for representing movement in space and time, and it is often used in the field of cell biology to examine the motion of particles within cells. The user can manually draw a line on a video frame, and the pixel intensities along that line are plotted as a function of time to produce the kymograph.

The project consists of three main Python files:

- `draw_kymograph_gui.py`: This script provides a GUI where users can open a video file, select a start and end time, and draw a line on a video frame to select the region of interest for the kymograph.
- `draw_kymograph.py`: This script allows users to generate a kymograph by manually entering the video file path and the start and end times directly into the script. A window will pop up allowing users to draw a line on the video frame to select the region of interest.
- `frame_difference.py`: This script calculates the difference between adjacent frames in a given video file and generates a new video file that visually represents these frame differences.

## Usage

To use the GUI for generating kymographs, run the `draw_kymograph_gui.py` script. Use the "Open Video" button to select your video file. Input the start and end times in the respective fields, and then draw a line on the video frame by clicking and dragging the mouse. Click the "Draw Kymograph" button to generate the kymograph.

To generate a kymograph without the GUI, you can use the `draw_kymograph.py` script. Edit the script to input your video file path and the start and end times directly into the code.

To create a video showing the differences between adjacent frames, use the `frame_difference.py` script. Input your video file path directly into the script.

## Requirements

The project requires Python and the following libraries: 

- tkinter
- opencv-python (cv2)
- numpy
- PIL (Python Imaging Library)
- matplotlib

