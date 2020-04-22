import os
import time


def cleanup(wait_time):
    while True:
        time.sleep(wait_time)
        os.remove(os.path.relpath('stream_output.log'))


if __name__ == "__main__":
    cleanup(172_800)  # Every 48 hours

