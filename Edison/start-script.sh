#!/bin/bash

# Change path to script if needed
/home/root/SmartHelmet/Edison/run-python.sh &
rfkill unblock bluetooth

# Determine which commands need to be re-entered
#bluetoothctl
#scan on
#pair 50:46:5D:77:25:1C
#discoverable on
#trust 50:46:5D:77:25:1C

#echo -e 'scan on' | bluetoothctl
echo -e 'pair 50:46:5D:77:25:1C' | bluetoothctl
sleep 1
echo -e 'discoverable on' | bluetoothctl
sleep 1
echo -e 'trust 50:46:5D:77:25:1C' | bluetoothctl
sleep 1
