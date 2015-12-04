#!/bin/bash

# Change path to script if needed
/home/root/SmartHelmet/Edison/run-python.sh &
rfkill unblock bluetooth

# This method is very touchy!
# Pair to Nexus 7 (ID 50:46:5D:77:25:1C)
#echo -e "power on\n" | bluetoothctl
#sleep 2
#echo -e "scan on\n" | bluetoothctl
#sleep 2
#echo -e "pair 50:46:5D:77:25:1C\n" | bluetoothctl
#sleep 2
#echo -e "discoverable on\n" | bluetoothctl
#sleep 1
#echo -e "trust 50:46:5D:77:25:1C\n" | bluetoothctl
#sleep 2

# Alternative pairing
bluetoothctl < /home/root/SmartHelmet/Edison/file.txt
