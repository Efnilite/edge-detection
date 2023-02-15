import time

import cv2

import to_ascii


def play(folder, video):
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

        if ns_to_wait < 0:
            dropped_frames.append(frame)
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
