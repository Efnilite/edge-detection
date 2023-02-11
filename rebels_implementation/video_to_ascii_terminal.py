import os
import cv2
import numpy as np
import math
import shutil
import sys

# Get the terminal size
rows, columns = shutil.get_terminal_size()
rows, columns = int(rows), int(columns)

# Load the video
video = cv2.VideoCapture("output_video.mp4")

# Get the total number of frames in the video
total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
#
# ASCII_CHARS = [' ', '.', '*', ':', 'o', '&', '8', '#', '@']
# ASCII_CHARS_COUNT = len(ASCII_CHARS)


def convert_frame_to_ascii(frame, terminal_width, terminal_height, scale_factor=0.5):
    # part of the code for printing to the terminal
    # frame_width, frame_height, _ = frame.shape
    # width_scale_factor = terminal_width / frame_width
    # height_scale_factor = terminal_height / frame_height
    # scale_factor = min(scale_factor, width_scale_factor, height_scale_factor)
    # resized_frame = cv2.resize(frame, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_AREA)

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Normalize the grayscale image to the range [0, 255]
    gray = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX)

    # Create an ASCII character map
    ascii_map = " .:-=+*#%@"

    # Convert the grayscale image to ASCII art
    #TODO: figure out how to do ascii art with the terminal
    # ascii_art = ""
    # for row in gray:
    #     for pixel in row:
    #         ascii_art += ascii_map[int(pixel / 255 * (len(ascii_map) - 1))]
    #     ascii_art += "\n"

    return ascii_art


# Loop through all frames in the video
for i in range(total_frames):
    # Read the current frame
    ret, frame = video.read()
    if not ret:
        break

    # Convert the frame to ASCII
    ascii_frame = convert_frame_to_ascii(frame, rows, columns)

    # Display the ASCII frame in the terminal
    print(ascii_frame)

# Release the video
video.release()
