#!/usr/bin/env python

import scapy.all as scapy
import time
from datetime import datetime

def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    clients_list = []
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        clients_list.append(client_dict)
    return clients_list

def print_result(results_list, new_devices):
    output = "IP\t\t\tMAC Address\n-----------------------------------------\n"
    for client in results_list:
        if client in new_devices:
            output += f"\033[91m{client['ip']}\t\t{client['mac']}\033[0m\n"  # Red color for new devices
        else:
            output += f"{client['ip']}\t\t{client['mac']}\n"
    return output

def check_string(ip_range):
    parts = ip_range.split("/")
    if len(parts) != 2:
        return False
    ip_address = parts[0]
    return ip_address.count(".") == 3 and parts[1].isdigit()

def save_to_file(output, filename):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(filename, 'a') as file:
        file.write(f"Scan Time: {timestamp}\n")
        file.write(output)
        file.write("\n")

ip_range = input("Input network range (eg: 192.168.1.0/24): ")

if not check_string(ip_range):
    print("Please enter the IP range in the correct format (see prompt)")
    exit()

previous_scan = []

while True:
    scan_result = scan(ip_range)

    new_devices = [client for client in scan_result if client not in previous_scan]

    output = print_result(scan_result, new_devices)
    print(output)

    save_to_file(output, "scan_results.txt")

    previous_scan = scan_result  # Update previous scan results
    time.sleep(1800)  # Sleep for 30 minutes (1800 seconds)