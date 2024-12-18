# Z-Screen

A simple Python desktop application that allows users to take screenshots and record their screen. The app is built using `Tkinter` for the GUI, `pyautogui` for capturing screenshots, and `mss` for screen recording.

## Features

- **Screenshot Capture**: Take screenshots and save them with unique timestamps.
- **Screen Recording**: Record the screen with a user-defined duration and save the video as an `.avi` file.
- **Timer**: The app includes a timer feature that shows the remaining time for both screenshots and screen recordings.
- **Mini Window**: When recording, a smaller movable window appears to show the timer and stop the recording once the time is up.
- **Save Location**: Select the folder to save the screenshots and recordings, with a default folder created named `ZiglaCity Screenshot_Recorder`.
- **Movable Timer**: The mini window displaying the timer is movable during the recording.

## Requirements

- Python 3.x
- `tkinter` (included with Python)
- `pyautogui`
- `mss`
- `opencv-python`
- `numpy`

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/Z-Screen.git
    cd Z-Screen
    ```

2. Install required dependencies:

    ```bash
    pip install pyautogui mss opencv-python numpy
    ```

## Usage

1. **Take Screenshot**: Click on the "Take Screenshot" button to capture a screenshot. The screenshot will be saved to the selected directory with a unique timestamp as the filename.
   
2. **Record Screen**:
    - Select the maximum recording time using the dropdown menu.
    - Click on the "Start Recording" button to begin screen recording. A mini window will appear, showing the countdown timer.
    - After the recording ends, the file will be saved with a timestamp as the filename.

3. **Stop Recording**: Click on the "Stop Recording" button to stop the recording manually. The app will automatically stop the recording when the set time is up.

4. **Save Location**: Click on "Browse" to choose a custom location to save screenshots and recordings.

## Customization

- **Default Save Location**: The default save location for both screenshots and recordings is `ZiglaCity Screenshot_Recorder` in the current working directory.
- **Timer**: You can customize the recording duration by selecting a value from the dropdown menu.
  
## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Zigla City

