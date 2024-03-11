# Text-To-Video Converter

## Overview
This Python application converts text input into a video with embedded subtitles. It utilizes various libraries such as MoviePy and PyDub for video and audio processing, respectively. The user interface is built using Tkinter, providing a simple GUI for users to select background video files and input text for conversion.

## Features
- Converts text input into speech using an API endpoint
- Embeds the generated speech as subtitles onto a selected background video
- Provides a simple and intuitive graphical interface for users

## Requirements
- Python 3.6 or higher
- External libraries (install via `pip install -r requirements.txt`):
  - moviepy
  - pydub
  - requests
  - ttkthemes

## GUI
![GUI](GUI.png "GUI")

## Usage
1. Clone the repository to your local machine.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Run the application using `python main.py`.
4. Use the GUI to select a background video file and input text for conversion.
5. Click on the "CREATE VIDEO" button to generate the video output.
6. Once the processing is complete, the resulting video will be displayed in the application.

## Contributing
Contributions are welcome! Feel free to submit pull requests or open issues for any bugs or feature requests.

## Author
Max Vo
