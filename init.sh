#!/usr/bin/bash

sudo apt update && sudo apt upgrade -y
sudo apt install aircrack-ng -y
sudo apt install macchanger -y

pip3 install -r requirements.txt

sudo python3 main.py