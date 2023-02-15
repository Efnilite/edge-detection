import time
import tkinter as tk

import cv2


# from image_converter import convert_image

def ascii_to_frame(ascii_frame, width, height):
    root = tk.Tk()
    root.geometry(f"{width}x{height}")
    label = tk.Label(root)
    label.pack()

    lines = ascii_frame.split("\n")

    def update_frame():
        label.config(text=ascii_frame)
        root.update()
        root.after(33, update_frame)

    root.after(0, update_frame)
    root.mainloop()


def video_to_frames(video_path):
    # Assuming that the video frames can be read and converted to ASCII art here

    # load the input video
    cap = cv2.VideoCapture(video_path)

    # Get the fps and frame size input video
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    while cap.isOpened():
        ret, frame = cap.read()

        if ret:
            ascii_frame = convert_frame_to_ascii(frame, frame_width, frame_height)
            ascii_to_frame(ascii_frame, frame_width, frame_height)
            time.sleep(1 / fps)
        else:
            break


def convert_frame_to_ascii(frame, width, height):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX)

    ascii_map = " .:-=+*#%@"

    ascii_art = ""
    for row in gray:
        for pixel in row:
            ascii_art += ascii_map[int(pixel / 255 * (len(ascii_map) - 1))]
        ascii_art += "\n"

    return ascii_art


video_to_frames('./output_video.mp4')
