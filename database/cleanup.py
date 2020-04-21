import os
import time



def cleanup(wait_time):
    time.sleep(wait_time)
    os.remove(os.path.relpath('twitter.db'))
    os.remove(os.path.relpath('stream_output.log'))


if __name__ == "__main__":
    cleanup(86400)  # Every 24 hours

