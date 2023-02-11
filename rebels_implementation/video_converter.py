import cv2
import image_converter

# Load the input video
video = cv2.VideoCapture("bad_apple_test.mp4")

# Get the video frames per second (fps) and frame size
fps = video.get(cv2.CAP_PROP_FPS)
frame_size = (int(video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)))

# Define the codec and create the output video
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
output_video = cv2.VideoWriter("output_video.mp4", fourcc, fps, frame_size)

# Process the video frames
while video.isOpened():
    # Read a frame from the video
    ret, frame = video.read()

    # If the frame is not None, process it
    if ret:
        # Convert the frame using the convert_image function
        object = image_converter.convert_image(frame)
        print("I'm converting this frame now")
        # Write the processed frame to the output video
        output_video.write(object)

        # Show the processed frame
        cv2.imshow("Processed frame", object)

        # If the user presses the `q` key, stop the loop
        if cv2.waitKey(25) & 0xFF == ord("q"):
            break

# Release the video and output video objects
video.release()
output_video.release()

# Close all windows
cv2.destroyAllWindows()
