<div style="text-align: center">

# 2022-2023 Informatics Practical Assignment 6 Programming

**[Showcase](https://youtu.be/SwfUHPLyQmo)** | 
**[Full source](https://github.com/Efnilite/edge-detection)** | 
by **[Roham Koohestani](https://github.com/RebelOfDeath)** and 
**[Rens Verstappen](https://github.com/Efnilite)**

</div>

## Summary

We have created a program which transforms a video file (mp4 format) into an
ASCII-character representation of the edges that gets printed to the command prompt.
When the main.py file gets run, the user is prompted to select a video file.
After a valid file has been selected, the program will first convert the video to
a temporary video file, where only edges are visible.
Then, the program converts this video to all its frames,
by creating a temporary folder and storing all frames of the video in PNG files.
When this has been completed, the program will print each frame individually,
as if the video is playing naturally. What gets printed is an ASCII-fied version of
each frame. This tool has been created using Python 3.11 and several Python libraries,
including ones which are not shipped by default: opencv, PIL, pathlib and numpy.

## Mark

We believe the tool we have created exceeds the expectations of this project.
We believe we went a step above how most people in our grade will experience Python.
We used external libraries and complex logic that are not easy to think of on your own,
if you've never used Python. Respectfully, we believe that no one in our class is able
to complete a project of this complexity. Therefore, as discussed with our teacher,
our preferred mark is a 10.

## Technical Summary

- The user runs main.py.
- The user has to select a valid file.
    - If the entered file is not valid, the program asks the user to enter another file.
- The source mp4 gets converted to a temporary mp4 where only edges are visible. (to_edged/to_edged_video)
    - All the video's frames are retrieved.
    - Each has several effects applied. (to_edged/find_edges)
    - Each affected frame is compiled to a new mp4 file, called _output.mp4.
- All the output mp4's frames are compiled to PNGs in a folder, called _temp. (to_frames/to_frames)
    - All the output video's frames are retrieved.
    - Each frame gets saved to a PNG with its name being the frame index.
- Each frame gets individually printed to the console. (to_terminal/play)
    - Video info is gathered. (fps, frame count, video duration)
    - Each image gets converted to an ASCII representation of all pixels and printed (to_ascii/print_frame)
        - First, the image gets put into memory using PIL. (to_ascii/to_image)
            - If image is not found, stop printing of video.
        - Each pixel of the image instance is converted to a luminance value (grayscale value, range: 0-255). (
          to_ascii/to_luminance)
            - First, to optimize for performance and console printing, the image is resized.
            - The resized images' pixels are converted to luminance values.
            - The pixels are compiled to a 2D-array for easier printing.
        - Each pixel's luminance value is converted to an ASCII character. (to_ascii/to_char)
            - This is done by scaling the luminance value to a list of ASCII characters we have compiled.
                - The higher the luminance value, the whiter it is, so the character should fill more of the space.
    - Between frames, to ensure the same fps as the source video, the main thread is paused by
      the time it took to get the ASCII representation and print it.
- Information about the entire process gets displayed: how many seconds it took to print the entire video,
  how much % this differs from the actual video length and which frames were "dropped" (not displayed)
  if the processing took too long.
- The _temp folder is deleted and opencv has all memory released.

# Todo update on final day~
## Full Code

### main.py

```python
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

    # remove folder with frames
    shutil.rmtree(folder, ignore_errors=True)


if __name__ == '__main__':
    main()

```

### to_edged.py

```python
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

```

### to_frames.py

```python
import math
import os
from pathlib import Path

import cv2


def to_frames(src, parent):
    """Converts the provided video at file path src to all frames in that video."""
    # gets the video
    video = cv2.VideoCapture(str(parent / "_output.mp4"))

    frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    intervals = list(range(frames))[0::int(frames / 10)]  # for the ... completed messages
    frame = 0

    folder = Path(src).parent.absolute() / "_temp"
    if not os.path.isdir(folder):
        os.makedirs(folder)  # create folder

    while True:
        success, image = video.read()

        # if frame is not found, stop and return data to be used in the rest of the code
        if not success:
            return folder, video

        cv2.imwrite(str(folder / f"{frame}.png"), image)

        if frame in intervals:
            print(f"{math.ceil(frame / frames * 100)}% completed... ({frame} / {frames})")

        frame += 1

```

### to_terminal.py

```python
import time

import cv2

import to_ascii


def play(folder, video):
    """Prints a video to the console."""
    # options
    fps = video.get(cv2.CAP_PROP_FPS)
    frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
    sec_time = frames / fps

    ns_between_frames = 1 / fps * 10 ** 9
    ns_init_sleep = 1_000_000  # time to initiate sleep

    result = 0
    frame = 0
    dropped_frames = []
    begin = time.time_ns()

    while result is not None:
        before = time.time_ns()

        result = to_ascii.print_frame(str(folder / f"{frame}.png"))

        # to ensure video plays at 30 fps we need to calculate the time it has taken to print and reduce this
        # from wait so the next frame plays on time
        elapsed_time = time.time_ns() - before

        # initiating sleep causes some ns to pass. remove this from time_to_wait to reduce inaccuracy from
        # ~2.5% (224 secs in execution) to ~-0.3% (218 secs in execution)
        ns_to_wait = ns_between_frames - elapsed_time - ns_init_sleep

        # if the ns to wait is negative, aka the reading took too long, add this frame to the "dropped'
        if ns_to_wait < 0:
            dropped_frames.append(frame)
            # can't wait negative amount of time
            ns_to_wait = 0

        frame += 1

        time.sleep(ns_to_wait * 10 ** -9)

    end = time.time_ns()

    # measure time it took to actually play video
    deltasecs = (end - begin) / 10 ** 9

    # stats
    print(f"Took: {deltasecs} | "
          f"Accuracy: {(deltasecs - sec_time) / sec_time * 100}% | "
          f"Dropped frames: {dropped_frames}")

```

### to_ascii.py

```python
from PIL import Image


def to_image(src):
    """Returns a new Image instance to perform operations on."""
    return Image.open(src)


def to_luminance(image):
    """Returns a 2D-list of all rgba values mapped to the specified detail level."""
    width = int(220)
    height = int(63)

    image = image.resize((width, height)).convert("L")

    pixels = list(image.getdata())
    final = []

    for y in range(height):
        final.append(pixels[(y * width):((y + 1) * width)])

    return final


grays = "#@$%&?!*~^;:'+=-_,.` "


# grays = "#W@$8%M&0GRBENHFKSAX?PQD45O3YZ62TLC7UVJI1!*~wmikltbdfheagypqsjzxnrvouc^;:'+=-_,.` "
# i just used all the keys on my keyboard lol
# i prefer the smaller version since letters are distracting but if extended palette is needed you can uncomment it


def to_char(luminance):
    """Transforms a luminance value to an ASCII character."""
    return grays[int((1 - luminance / 255) * (len(grays) - 1))]


def print_grid(pixels):
    """Prints the final pixel grid with the provided pixels at the provided positions."""
    to_chars = list(map(lambda row: list(map(to_char, row)), pixels))

    total = ""

    for row in to_chars:
        total += "".join(row) + "\n"

    print(total)


def print_frame(file):
    """Prints the specified file."""
    try:
        img = to_image(file)
    except FileNotFoundError:
        return None

    dots = to_luminance(img)

    print_grid(dots)

    return True

```

## Code Explanation

### main.py

```python
import os
import shutil
from pathlib import Path

import cv2

import to_edged
import to_frames
import to_terminal
```

This code imports all the modules we need to run the main procedure of our program. 
Importing these modules gives our code access to these modules' features.
Importing has two steps: first, the module name is found. Then, that module
gets bound to a local variable. The module name is the part after `import`. 
Syntax: `import (module name)`

The first four import statements are used to import external modules. 
The last three are used to import local program files.
The `from pathlib import Path` import statement imports a specific class from a module. 
Syntax: `from (module name) import (names of classes)`
---

```python
def main():
    print("===================================================")
    print("Enter your source video.")
```

In the above code, a function called `main` with no arguments is defined. Syntax: 
`def function_name(arguments seperated by a ,):`
After the `:`, every line of code that has been "indented" (preceded by a tab/spaces) will be executed
when the function is called. 
In this case, the `print` function is called. 
Print prints the provided arguments to the standard output. Syntax: `function_name(arguments seperated by a ,)` 
The arguments are, in this case, a string literal. A string is text which has been surrounded
by quotation marks (a.k.a. air commas). Syntax: `"your text here"`. This snippet features 2 `print` statements.

---

```python
    while True:
        src = input().strip()

        if os.path.exists(src):
            break

        print("That file does not exist. Try again.")
```

The above code starts with a while-loop. Syntax: `while (condition):` 
A while-loop is a form of loop: it activates the code within the body
over and over again, until the condition is false. The condition has to be a boolean value:
`True` or `False`. `False` is the opposite of `True`. When the condition is true, the code within the body will be repeated
until the condition becomes `False`. If it is `False`, it will not again execute the body. 
In this case, the value is set to `True`. `True` is a constant value which does not equal `False`. 
Therefore, the body will be repeated indefinitely.

The second line consists of a variable assignment. Variables are a way to easily associate data with 
a callable identifier. Syntax: `variable_name = data`. In this case, the variable is named `src`, which means `source`.
This variable will contain the source video. The data, in this case, is equal to `input().strip()`. Like print,
these are 2 function calls. 
- `input` asks the user to input some text. In this case, we want the user to input the source video.
- `strip` removes any trailing and leading spaces from the input string. If these are not removed, 
it may cause problems later.

Line 4 is an if statement. An if statement performs the code within its body when the condition equals `True`.
Syntax: `if (condition):`. In this case, we want to check whether the file, provided by the user,
actually exists. To do this, we use the `os` module. Then, we use the `path` property of and then the
`exists` method. In this method's arguments, we pass the path the user provided. If this path
exists, the method will return `True`. If it doesn't exist, it returns `False`.
If the file exists, we want to stop our infinite loop. This is done with the `break` keyword.
If the file doesn't exist, we want to user to enter another file. The loop continues.
After the if-statement, a print statement is used to tell the user they may input another path.
After that print statement, the body of the while loop returns to the start; to the `input().strip()`.
This way the user may only continue when they have entered a file that exists.

---

```python
    parent = Path(src).parent.absolute()
```

The above code assigns the variable `parent` to the parent folder of the provided file path. 
The parent folder of the provided path is gathered using the `Path` class from `pathlib`.
`Path(src)` creates a new instance of the `Path` class. Then, we use the `parent` attribute of
the class to get the parent folder. The `absolute()` method returns the absolute file path
(from the source drive) to the parent of the provided file. 

---

```python
    print("Applying edge detection...")

    # convert to edged video
    to_edged.to_edged_video(src, parent)
```

Next, we let the user know what is happening with another print statement. Then, from the `to_edged.py`
file, the method `to_edged_video` is called. This takes the source file `src` and 
parent folder `parent` as arguments. This will be explained in detail in the `to_edged.py` chapter.

---

```python
    print()
    print("Converting frames...")
    
    # create folder with all frames as pngs
    # isn't done on the fly to ensure the console can play the video at preferred fps
    folder, video = to_frames.to_frames(src, parent)
```

Afterwards, we use a print statement with no arguments to print a new line. Then, again, we let
the user know what is happening with another print statement. Finally, we invoke the
`to_frames` method from `to_frames.py`, with the same arguments as `to_edged_video` from `to_edged.py`.
This method returns a 2-tuple, which we use to define several new variables on one line. Syntax:
`var1, var2 = 2-tuple`. A tuple is a way to send several pieces of information at the same time.
A method may, for instance, want to return `True` and `32`. To do this, you can save these values
in a tuple and return it. Syntax: `val1, val2`. 
In this case, `folder` is the folder in which all frames of the output video have been put. `video`
is the special opencv version of the output video. We store this and pass it on to the next method,
to avoid reading the output video twice. 

---

```python
    print()
    print("All good now. Enjoy the show!")

    to_terminal.play(folder, video)
```

Next, we print another new line using an empty print statement. We let the user know that the video
finished converting, and that they may enjoy the displaying. Then, the method `play` from `to_terminal.py`
is called. This prints the video to the standard output. This takes the `folder` and `video` arguments
we received when we invoked the `to_frames` method from `to_frames.py`. 

---

```python
    # remove folder with frames
    shutil.rmtree(folder, ignore_errors=True)
```

Finally, we use the `rmtree` method from the `shutil` module to remove the folder that contains 
all the frames as PNGs. We pass the `folder` variable to it, to indicate which folder to remove.
We also set the optional variable `ignore_errors` to `True`. This indicates that the method should
ignore any errors which may pop up. By default, this is set to `False`. 

---

```python
if __name__ == '__main__':
    main()
```

The above piece of code prevents users from accidentally running the entire file if they ever try to import it.
It consists of an if statement, where a special variable called `__name__` is checked to see if it is equal to
`"__main__"`. When a user executes this code, `__name__` is equal to `"__main__"`. When this file is imported by
another file, `__name__` will equal the file name, which in this case is `"main"`. `"main"` does not equal `"__main__"`, 
therefore preventing accidental execution.

### to_edged.py
rooham

### to_frames.py
rooham

### to_terminal.py
rooham

### to_ascii.py
rooham/wens? idk you pick