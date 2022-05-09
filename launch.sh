#!/bin/bash

sudo modprobe -r port100
vendor=054c:06c3
devices=$(lsusb -d $vendor | sed -e 's|Bus \(...\) Device \(...\).*|usb:\1:\2|')
sed -i -e "/usb_bus_device/c usb_bus_device = $devices" config.ini

python3 main.py
