#!/bin/bash

DIR="${0%/*}"
cd $DIR/database
sudo nohup python3 entry_v2.py > stream_output.log &
sudo nohup python3 cleanup.py > /dev/null &
cd ..
sudo nohup python3 main.py > /dev/null &