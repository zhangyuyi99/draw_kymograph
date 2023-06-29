import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Kymograph Generation")  # Add a title to the window
        self.root.geometry("900x720")  # Change the window size
        
        self.canvas = tk.Canvas(root, width=720, height=720, cursor="cross", bg='white')
        self.canvas.pack(side="left", padx=10, pady=10)  # Add padding around the canvas
        
        self.panel = tk.Frame(root, bg='lightgrey')  # Add a background color to the panel
        self.panel.pack(side="right", fill="both", expand=True)
        
        self.instructions = tk.Label(self.panel, text="Instructions: \n\n 1. Click 'Open Video' to select a video file.\n\n"
                                                      "2. Draw a line on the video frame.\n\n"
                                                      "3. Enter the start and end times.\n\n"
                                                      "4. Click 'Draw Kymograph'.", bg='lightgrey')
        self.instructions.pack(padx=10, pady=10)

        self.open_button = tk.Button(self.panel, text="Open Video", command=self.open_video)  # Use ttk for a nicer looking button
        self.open_button.pack(padx=10, pady=10)
        
        self.start_label = tk.Label(self.panel, text="Start time (s)", bg='lightgrey')
        self.start_label.pack()
        self.start_entry = tk.Entry(self.panel)
        self.start_entry.pack(padx=10, pady=10)

        self.end_label = tk.Label(self.panel, text="End time (s)", bg='lightgrey')
        self.end_label.pack()
        self.end_entry = tk.Entry(self.panel)
        self.end_entry.pack(padx=10, pady=10)
        
        self.slowdown_label = tk.Label(self.panel, text="Slowdown Factor")
        self.slowdown_label.pack()
        self.slowdown_entry = tk.Entry(self.panel)
        self.slowdown_entry.pack()
        self.slowdown_entry.insert(0, "1")  # set default value


        self.draw_button = tk.Button(self.panel, text="Draw Kymograph", command=self.draw_kymograph)
        self.draw_button.pack(padx=10, pady=10)
        
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)


        self.start = None
        self.end = None
        self.image = None
        self.video_file = None

    def on_button_press(self, event):
        self.start = (event.x, event.y)

    def on_move_press(self, event):
        if self.start:
            self.canvas.delete("line")
            self.end = (event.x, event.y)
            self.canvas.create_line(*self.start, *self.end, fill="green", tags="line")

    def on_button_release(self, event):
        self.end = (event.x, event.y)

    def open_video(self):
        self.video_file = filedialog.askopenfilename()
        cap = cv2.VideoCapture(self.video_file)
        _, frame = cap.read()
        cap.release()
        cv2.cvtColor(frame, cv2.COLOR_BGR2RGB, frame)
        frame = Image.fromarray(frame)
        frame = ImageTk.PhotoImage(frame)
        self.image = self.canvas.create_image(0, 0, image=frame, anchor="nw")
        self.canvas.image = frame

    def draw_kymograph(self):
        if not self.start or not self.end:
            print("You must draw a line on the video frame first.")
            return
        start_time = float(self.start_entry.get())
        end_time = float(self.end_entry.get())
        line_start = self.start
        line_end = self.end
        slowdown_factor = float(self.slowdown_entry.get())
        # Now you can use these parameters to generate your kymograph
        generate_kymograph(self.video_file, start_time, end_time, line_start, line_end, slowdown_factor)

def generate_kymograph(video_file, start_time, end_time, line_start, line_end, slowdown_factor):
    
    cap = cv2.VideoCapture(video_file)
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    start_frame = int(start_time * fps)
    end_frame = int(end_time * fps)
    
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    kymograph = []
    
    line_length = int(np.sqrt((line_end[1] - line_start[1]) ** 2 + (line_end[0] - line_start[0]) ** 2))
    x_values = np.linspace(line_start[0], line_end[0], line_length).astype(int)
    y_values = np.linspace(line_start[1], line_end[1], line_length).astype(int)
    
    for i in range(start_frame, end_frame):
        ret, frame = cap.read()
        if not ret:
            break
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        intensity_values = gray_frame[y_values, x_values]
        kymograph.append(intensity_values)
    
    cap.release()
    kymograph = np.array(kymograph)

    # Plotting
    fig, ax = plt.subplots()
    im = ax.imshow(kymograph, cmap="gray", aspect="auto")  # store the output of imshow in im
    
    ax.set_xlabel('$Distance, [pixel]$', fontsize=20)
    ax.set_ylabel('$Time, [s]$', fontsize=20)
    
    # Multiply the y_ticks by the slowdown factor
    y_ticks = np.array([0, 1, 2, 3, 4]) * fps 
    ax.set_yticks(y_ticks)
    ax.set_yticklabels(y_ticks / fps / slowdown_factor, fontsize=20)
    
    # Set the x-axis ticks to match the pixel length of the selected line
    x_ticks = np.linspace(0, line_length, 5).astype(int)  # adjust as needed
    ax.set_xticks(x_ticks)
    ax.set_xticklabels(x_ticks, fontsize=20)
    
    plt.colorbar(im)  # pass the mappable object im to colorbar()
    
    plt.tight_layout()
    plt.show()


root = tk.Tk()
app = App(root)
root.mainloop()
