import math
import os
from pathlib import Path

import cv2


def to_frames(src, parent):
    """Converts the provided video at file path src to all frames in that video."""
    video = cv2.VideoCapture(str(parent / "_output.mp4"))

    frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    intervals = list(range(frames))[0::int(frames / 10)]
    frame = 0

    folder = Path(src).parent.absolute() / "_temp"
    if not os.path.isdir(folder):
        os.makedirs(folder)

    while True:
        success, image = video.read()

        if not success:
            return folder, video

        cv2.imwrite(str(folder / f"{frame}.png"), image)

        if frame in intervals:
            print(f"{math.ceil(frame / frames * 100)}% completed... ({frame} / {frames})")

        frame += 1
