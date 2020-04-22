#!/bin/bash

DIR="${0%/*}"
cd $DIR/database
sudo nohup python3 entry_v2.py > /dev/null &
cd ..
sudo nohup python3 main.py > /dev/null &
