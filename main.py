import tkinter as tk
import os


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
        

if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenApp(root)
    root.mainloop()
