#!/usr/bin/bash

sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install aircrack-ng -y
sudo apt-get install macchanger -y

pip3 install -r requirements.txt

sudo python3 main.py