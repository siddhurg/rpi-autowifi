#!/bin/bash
# Check if connected to Wi-Fi
iwgetid -r
if [ $? -eq 0 ]; then
    echo "Connected to Wi-Fi."
else
    echo "No Wi-Fi. Starting Access Point and UI..."
    sudo systemctl start hostapd
    sudo systemctl start dnsmasq
    python3 /home/pi/wifi_config.py
fi
