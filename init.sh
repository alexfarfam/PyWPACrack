#!/usr/bin/bash

sudo apt-get update && sudo apt-get upgrade
sudo apt-get install aircrack-ng
sudo apt-get install macchanger

pip3 install -r requirements.txt

sudo python3 main.py