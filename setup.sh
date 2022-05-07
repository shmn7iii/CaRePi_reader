#!/bin/bash

sudo apt-get install -y python3-pip
sudo pip3 install -r requirements.txt
sudo modprobe -r port100

vendor=054c:06c3
devices=$(lsusb -d $vendor | sed -e 's|Bus \(...\) Device \(...\).*|usb:\1:\2|')

sed -i -e "s/xxx\:xxx\:xxx/$devices/" config.ini
