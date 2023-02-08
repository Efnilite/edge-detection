import cv2


def convert_to_frames(src, save_to):
    """Converts the provided video at file path src to all frames in that video with the specified path save_to.
    The frame index is passed to save_to, making it possible to use '%d' in the save_to path to get the frame index."""
    capture = cv2.VideoCapture(src)
    frame = 0

    while True:
        success, image = capture.read()

        if not success:
            return

        cv2.imwrite(save_to % frame, image)

        print(f"Frame: {frame} 🗸")

        frame += 1


convert_to_frames("resources/bad_apple/bad_apple_src.mp4", "resources/bad_apple/%d.png")
