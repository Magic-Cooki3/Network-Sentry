# Network Sentry

This Python script scans a specified network range for connected devices and outputs their IP and MAC addresses. It saves the scan results to a text file along with timestamps, allowing you to keep track of devices on your network over time.

Must be run as root/sudo on Linux or Admin on Windows.

## Features

- Scans a specified network range (e.g., `192.168.1.0/24`) for connected devices.
- Displays the detected devices with their IP and MAC addresses in the console.
- Saves scan results to a text file with timestamps for each scan.
- Highlights new devices in red in the console output.

## Requirements

- Python 3.x
- Scapy library
