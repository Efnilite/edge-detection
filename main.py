import os
import shutil
from pathlib import Path

import cv2

import to_edged
import to_frames
import to_terminal


def main():
    print("===================================================")
    print("Enter your source video.")

    while True:
        src = input().strip()

        if os.path.exists(src):
            break

        print("That file does not exist. Try again.")

    # get the parent folder to do stuff in
    parent = Path(src).parent.absolute()

    print("Applying edge detection...")

    # convert to edged video
    to_edged.to_edged_video(src, parent)

    print()
    print("Converting frames...")

    # create folder with all frames as pngs
    # isn't done on the fly to ensure the console can play the video at preferred fps
    folder, video = to_frames.to_frames(src, parent)

    print()
    print("All good now. Enjoy the show!")

    to_terminal.play(folder, video)

    # destroy cv2 instances, save the memory
    cv2.destroyAllWindows()
    # remove folder with frames
    shutil.rmtree(folder, ignore_errors=True)


if __name__ == '__main__':
    main()
