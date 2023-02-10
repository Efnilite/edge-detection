import time

import image_processor

# options
fps = 30
sec_time = 218.933333

ns_between_frames = 1 / 30 * 10 ** 9
ns_init_sleep = 1_000_000  # time to initiate sleep

if __name__ == '__main__':

    result = 0
    frame = 0
    dropped_frames = []
    begin = time.time_ns()

    while result is not None:
        before = time.time_ns()

        result = image_processor.print_frame(f"resources/bad_apple/{frame}.png")

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

    deltasecs = (end - begin) / 10 ** 9

    print(f"Took: {deltasecs} | "
          f"Accuracy: {(deltasecs - sec_time) / sec_time * 100}% | "
          f"Dropped frames: {dropped_frames}")
