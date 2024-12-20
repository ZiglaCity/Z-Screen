import tkinter as tk
import os
from tkinter import ttk, filedialog


class ScreenApp:
    global height, width
    height = 300
    width = 400
    def __init__(self, root):
        self.root = root
        self.root.title("Z-Screen")
        self.root.geometry(f"{width}x{height}")

        self.is_recording = False
        self.max_time = tk.IntVar(value=10)
        self.save_location = tk.StringVar(value=os.path.join(os.getcwd(), "ZiglaCity-ZScreen"))
        
        if not os.path.exists(self.save_location.get()):
            os.makedirs(self.save_location.get())

        
        ttk.Label(root, text="Max Recording Time (seconds):").pack(pady=10)
        
        self.combo = ttk.Combobox(root, values=list(range(5, 61, 5)), textvariable=self.max_time, state="readonly")
        self.combo.pack(pady=5)
        
        ttk.Label(root, text="Save Location:").pack(pady=10)
        self.save_location_entry = ttk.Entry(root, textvariable=self.save_location, width=40)
        self.save_location_entry.pack(pady=5)
        ttk.Button(root, text="Browse", command=self.browse_save_location).pack(pady=5)
        
        self.start_button = ttk.Button(root, text="Start Recording", command=self.start_recording)
        self.start_button.pack(pady=5)
        
        self.stop_button = ttk.Button(root, text="Stop Recording", command=self.stop_recording, state="disabled")
        self.stop_button.pack(pady=5)
        
        self.screenshot_button = ttk.Button(root, text="Take Screenshot", command=self.take_screenshot)
        self.screenshot_button.pack(pady=5)

    
    def browse_save_location(self):
        directory = filedialog.askdirectory(title="Select Save Location")
        if directory:
            self.save_location.set(directory)
        

    def take_screenshot(self):
        pass

    def capture_screenshot():
        pass

    def stop_recording(self):
        pass

    def start_recording(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenApp(root)
    root.mainloop()
