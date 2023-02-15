import math

import cv2
import numpy as np


def find_edges(image):
    """Converts the provided image to one where only edges are visible."""
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)

    # Perform Canny edge detection
    edges = cv2.Canny(blurred, 25, 200)

    # Perform dilation to fill in gaps in the edge map
    kernel = np.ones((5, 5), np.uint8)
    # dilated = cv2.dilate(edges, kernel, iterations=1)
    closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

    # Find contours in the edge map
    contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Create a mask using the contours
    mask = np.zeros_like(closed)
    cv2.drawContours(mask, contours, -1, 255, -1)

    # Extract the object using the mask
    object = cv2.bitwise_and(image, image, mask=mask)

    # return the object
    return object


def to_edged_video(src, parent):
    # Load the input video
    video = cv2.VideoCapture(src)

    # Get the video frames per second (fps) and frame size
    fps = video.get(cv2.CAP_PROP_FPS)
    frame_size = (int(video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    # the current frame
    frame_idx = 0
    frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    intervals = list(range(frames))[0::int(frames / 10)]

    # Define the codec and create the output video
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    output_video = cv2.VideoWriter(str(parent / "_output.mp4"), fourcc, fps, frame_size)

    # Process the video frames
    while video.isOpened():
        # Read a frame from the video
        success, frame = video.read()

        # If the frame is not None, process it
        if not success:
            break

        # Convert the frame using the find_edges function
        object = find_edges(frame)

        # Write the processed frame to the output video
        output_video.write(object)

        if frame_idx in intervals:
            print(f"{math.ceil(frame_idx / frames * 100)}% completed... ({frame_idx} / {frames})")

        frame_idx += 1

    # Release the video and output video objects
    video.release()
    output_video.release()

    return output_video
