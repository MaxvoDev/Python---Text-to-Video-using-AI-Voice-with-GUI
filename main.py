import threading
import os
import requests
import base64
import io
from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.config import change_settings
from pydub import AudioSegment
from tkinter import filedialog, messagebox
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from ttkthemes import ThemedTk

change_settings({"IMAGEMAGICK_BINARY": "./magick.exe"})

# CONSTANTS
YOURSCRIPT = """I'm Max, a passionate full-stack web developer based in Vietnam. With a knack for coding and a thirst for learning, I'm always diving into the latest technologies and frameworks to enhance my skills and deliver top-notch solutions. 

Beyond the world of coding, you might catch me creating engaging and informative content on platforms like TikTok and YouTube. Whether it's sharing coding tips, exploring new tech trends, or just having fun, I love connecting with others and spreading knowledge in creative ways.

Join me on this exciting journey as we explore the endless possibilities of technology together!"""
AUDIO_PATH = "audio.mp3"
SUBTITLE_PATH = "subtitle.srt"
OUTPUT_PATH = "output.mp4"

def get_audio_from_api(script):
    url = "https://audio.api.speechify.com/generateAudioFiles"
    payload = {
        "audioFormat": "mp3",
        "paragraphChunks": [script],
        "voiceParams": {
            "name": "matthew",
            "engine": "neural",
            "languageCode": "en-US"
        }
    }
    
    response = requests.post(url, json=payload)

    if response.status_code == 200:
        response_json = response.json()
        return response_json['audioStream'], response_json['speechMarks']['chunks'][0]['chunks']
    else:
        print(f"Error: {response.status_code}")
        return None


def decode_audio(audio_stream):
    audio_data = io.BytesIO(base64.b64decode(audio_stream))
    return AudioSegment.from_mp3(audio_data)


def save_subtitle_file(speechmarks_data):
    srt_content = ""
    counter = 1

    for speechmark in speechmarks_data:
        start_time = speechmark['startTime'] / 1000.0
        end_time = speechmark['endTime'] / 1000.0
        caption_text = speechmark['value']

        start_time_formatted = "{:02}:{:02}:{:02},{:03}".format(
            int(start_time // 3600),
            int((start_time % 3600) // 60),
            int(start_time % 60),
            int((start_time * 1000) % 1000)
        )
        end_time_formatted = "{:02}:{:02}:{:02},{:03}".format(
            int(end_time // 3600),
            int((end_time % 3600) // 60),
            int(end_time % 60),
            int((end_time * 1000) % 1000)
        )

        srt_content += f"{counter}\n{start_time_formatted} --> {end_time_formatted}\n{caption_text}\n\n"
        counter += 1

    with open(SUBTITLE_PATH, "w") as f:
        f.write(srt_content)


def add_subtitle_to_video(video_clip, subtitle_clip):
    return CompositeVideoClip([video_clip, subtitle_clip])


def process_video():
    YOURSCRIPT = text_area.get("1.0", tk.END)
    audio_stream, speechmarks_data = get_audio_from_api(YOURSCRIPT)
    if audio_stream:
        result_audio = decode_audio(audio_stream)
        result_audio.export(AUDIO_PATH, format="mp3")

        save_subtitle_file(speechmarks_data)

        background_audio = AudioFileClip(AUDIO_PATH)
        background_video = VideoFileClip(BGVIDEO_PATH)
        reddit_image = ImageClip(PICTURE_PATH)

        generator = lambda txt: TextClip(txt, font='Arial', fontsize=100, color='yellow')
        subtitles_text = SubtitlesClip(SUBTITLE_PATH, generator)
        subtitles_text = subtitles_text.set_position(("center", "center")).set_duration(background_video.duration)

        reddit_image = reddit_image.resize(width=background_video.w)

        video_with_subtitles = add_subtitle_to_video(background_video.set_audio(background_audio), subtitles_text)
        video_with_subtitles = add_subtitle_to_video(video_with_subtitles, reddit_image.set_position((0, 0)).set_duration(background_video.duration))

        video_with_subtitles.write_videofile(
            OUTPUT_PATH,
            codec="libx264",
            audio_codec="aac",
            audio_bitrate="192k",
            audio_fps=44100,
            fps=24
        )
        
        messagebox.showinfo("Success", "Video processing complete!")
        done()
        
def run():
    start_button.config(text="RUNNING...", state="disabled")
    thread = threading.Thread(target=process_video)
    thread.start()
    

def done():
    start_button.config(text="CREATE VIDEO", state="normal")
    
def select_video_dialog():
    global BGVIDEO_PATH
    BGVIDEO_PATH = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4")])
    
def select_picture_dialog():
    global PICTURE_PATH
    PICTURE_PATH = filedialog.askopenfilename(filetypes=[("PICTURE files", "*.png")])


root = ThemedTk()
root.title("PYTHON - CONVERT TEXT TO VIRAL VIDEO USING AI VOICE")

# Choose a theme
root.set_theme("arc")

# Column One
column1_frame = ttk.Frame(root)
column1_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nswe")

# Select Picture Label and Browse Button
picture_label = ttk.Label(column1_frame, text="Select Picture (.png):")
picture_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
picture_button = ttk.Button(column1_frame, text="Browse", command=select_picture_dialog)
picture_button.grid(row=0, column=1, padx=5, pady=5, sticky="e")

# Select Picture Label and Browse Button
picture_label = ttk.Label(column1_frame, text="Select Video Background (.mp4):")
picture_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
picture_button = ttk.Button(column1_frame, text="Browse", command=select_video_dialog)
picture_button.grid(row=1, column=1, padx=5, pady=5, sticky="e")

# Enter Text Label
text_label = ttk.Label(column1_frame, text="Enter Text for Speech:")
text_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

# Text Area
text_area = scrolledtext.ScrolledText(column1_frame, height=10, width=50)
text_area.insert(tk.END, YOURSCRIPT)  # Insert default text
text_area.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

start_button = ttk.Button(column1_frame, text="CREATE VIDEO", command=run)
start_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

root.mainloop()