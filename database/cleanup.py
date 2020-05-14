import os
import time


# script to delete the database from our hsted solution every 24 hours, helps with keeping db calls quick
def cleanup(wait_time):
    time.sleep(wait_time)
    os.remove(os.path.relpath('twitter.db'))
    os.remove(os.path.relpath('stream_output.log'))


if __name__ == "__main__":
    cleanup(86400)  # Every 24 hours

