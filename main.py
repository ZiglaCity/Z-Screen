import tkinter as tk
from os.path import join, exists
from os import getcwd, makedirs
from tkinter.ttk import Entry, Button, Label
from tkinter import filedialog
from tkinter.ttk import Combobox
from tkinter.messagebox import showinfo, showerror
from pyautogui import screenshot as take_shot, position
from datetime import datetime
from mss import mss
import cv2
import numpy as np
from threading import Thread


class ScreenApp:
    global height, width
    height = 350
    width = 350
    def __init__(self, root):
        self.root = root
        self.root.title("Z-Screen")
        self.root.geometry(f"{width}x{height}")
        # self.root.config(bg="#333333")

        self.is_recording = False
        self.max_time = tk.IntVar(value=10)
        self.save_location = tk.StringVar(value=join(getcwd(), "ZiglaCity-ZScreen"))
        
        if not exists(self.save_location.get()):
            makedirs(self.save_location.get())
 
        Label(root, text="Max Recording Time (seconds):").pack(pady=10)
        
        self.combo = Combobox(root, values=list(range(5, 61, 5)), textvariable=self.max_time, state="normal")
        self.combo.pack(pady=5)
        
        Label(root, text="Save Location:").pack(pady=10)
        self.save_location_entry = Entry(root, textvariable=self.save_location, width=40, state="readonly")
        self.save_location_entry.pack(pady=5)
        Button(root, text="Browse", command=self.browse_save_location).pack(pady=5)
        
        self.start_button = Button(root, text="Start Recording", command=self.start_recording)
        self.start_button.pack(pady=5)
        
        self.stop_button = Button(root, text="Stop Recording", command=self.stop_recording, state="disabled")
        self.stop_button.pack(pady=5)
        
        self.screenshot_button = Button(root, text="Take Screenshot", command=self.take_screenshot)
        self.screenshot_button.pack(pady=5)

    
    def browse_save_location(self):
        directory = filedialog.askdirectory(title="Select Save Location")
        if directory:
            self.save_location.set(directory)
        

    def take_screenshot(self):
        try:
            self.root.after(500, self.minimize_app)
            timestamp = datetime.now().strftime("%Y_%m_%d %H-%M-%S")
            save_path = join(self.save_location.get(), f"screenshot_{timestamp}.png")
            
            self.root.after(1000, self.capture_screenshot, save_path)

        except Exception as e:
            showerror("Error!", f"Failed to take screenshot: {e}")


    def capture_screenshot(self, save_path):
        screenshot = take_shot()
        screenshot.save(save_path)
        showinfo("Success!", f"Screenshot saved {save_path}")


    def minimize_app(self):
        self.root.iconify()


    def start_recording(self):
        self.is_recording = True
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.record_screen()

        
    def stop_recording(self):
        self.is_recording = False
        self.stop_button.config(state="disabled")
        self.start_button.config(state="normal")
        self.recording_window.destroy()

    
    def record_screen(self):
        max_time = self.max_time.get()
        
        self.root.after(100, self.minimize_app)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_file = join(self.save_location.get(), f"screenrecord_{timestamp}.avi")

        self.root.after(300, self.start_recording_process, output_file, max_time)

    
    def start_recording_process(self, output_file, max_time):
        self.recording_window = tk.Toplevel(self.root)
        self.recording_window.title("Recording...")
        self.recording_window.geometry("180x80")

        self.recording_window.attributes("-topmost", True)
        self.recording_window.protocol("WM_DELETE_WINDOW", self.stop_recording)

        self.timer_label = Label(self.recording_window, text=f"Time Left: {max_time//60}m {max_time%60}s", font=("Arial", 10))
        self.timer_label.pack()

        self.stop_recording_button = Button(self.recording_window, text="🛑", command=self.stop_recording)
        self.stop_recording_button.pack(pady=10)
        
        self.time_left = max_time
        self.update_timer()

        self.recording_window.bind("<Button-1>", self.start_drag)
        self.recording_window.bind("<B1-Motion>", self.on_drag)

        Thread(target=self.record_screen_in_background, args=(output_file, max_time), daemon=True).start()


    def start_drag(self, event):
        self.drag_data ={'x': event.x, 'y': event.y}
    

    def on_drag(self, event):
        old_x = event.x - self.drag_data['x']
        old_y = event.y - self.drag_data['y']
        new_x = old_x + self.recording_window.winfo_x()
        new_y = old_y + self.recording_window.winfo_y()
        self.recording_window.geometry(f"+{new_x}+{new_y}")


    def update_timer(self):
        if self.is_recording and self.time_left > 0:
            self.timer_label.config(text=f"Time Left: {self.time_left//60}m {self.time_left%60}s")
            self.time_left -= 1
            self.recording_window.after(1000, self.update_timer)
        elif self.time_left == 0:
            self.stop_recording()

    
    def add_mouse_pointer(self, screen, mouse_x, mouse_y):
        cv2.circle(screen, (mouse_x, mouse_y), 7, (255, 255, 255), -1)
        return screen
    

    def record_screen_in_background(self, output_file, max_time):
        """Record the screen in the background while updating the timer."""
        with mss() as sct:
            monitor = sct.monitors[1]  # Main monitor
            width, height = monitor["width"], monitor["height"]
            
            # Set up OpenCV video writer
            """
            fourcc: The codec for the video file (XVID in this case).
            VideoWriter object from OpenCV, used to write frames to the video file.
            20.0: The frame rate for the video (20 frames per second). 
            """           
            fourcc = cv2.VideoWriter_fourcc(*"XVID")
            out = cv2.VideoWriter(output_file, fourcc, 20.0, (width, height))

            frame_count = 0
            try:
                while self.is_recording and frame_count < 20 * max_time:  # 20 FPS
                    """
                    sct.grab(monitor): Capture the screen.
                    np.array(): Convert the captured image to a NumPy array.
                    cv2.cvtColor(): Convert the image from BGRA to BGR format (required by OpenCV).
                    """
                    frame = np.array(sct.grab(monitor))
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
                    mouse_x, mouse_y = position() 
                    frame = self.add_mouse_pointer(frame, mouse_x, mouse_y)
                    out.write(frame) #writes the captured frame to the video file.
                    frame_count += 1 #increase frame counter so that we don't record pass the max time setted
                
                out.release()  #Ensures the video writer releases the file and resources properly.
                self.stop_recording() 
                if not self.is_recording:
                    showinfo("Success", f"Recording saved as '{output_file}'")
                
            except Exception as e:
                showerror("Error", f"Failed to record: {e}")
    


if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenApp(root)
    root.mainloop()
