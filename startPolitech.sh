#!/bin/bash

DIR="${0%/*}"
cd $DIR/database
sudo nohup python3 entry_v2.py > stream_output.log &
cd ..
sudo nohup python3 main.py > main_output.log &