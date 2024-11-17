#!/usr/bin/env python

import nmap
import time
from datetime import datetime

def scan(ip_range):
    nm = nmap.PortScanner()
    nm.scan(hosts=ip_range, arguments='-sn')  # Use -sn for a ping scan (no port scan)
    
    clients_list = []
    for host in nm.all_hosts():
        if 'mac' in nm[host]['addresses']:
            client_dict = {
                "ip": host,
                "mac": nm[host]['addresses']['mac']
            }
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

# Main execution
ip_range = input("Input network range (eg: 192.168.1.0/24): ")

if not check_string(ip_range):
    print("Please enter the IP range in the correct format (see prompt)")
    exit()

previous_scan = []

while True:
    scan_results = []
    for _ in range(3):  # Perform 3 scans
        scan_results.extend(scan(ip_range))
        time.sleep(1)  # Wait a bit before the next scan

    # Deduplicate results
    unique_devices = { (client['ip'], client['mac']) for client in scan_results }
    unique_clients_list = [{"ip": ip, "mac": mac} for ip, mac in unique_devices]

    new_devices = [client for client in unique_clients_list if client not in previous_scan]

    output = print_result(unique_clients_list, new_devices)
    print(output)

    save_to_file(output, "scan_results.txt")

    previous_scan = unique_clients_list  # Update previous scan results
    time.sleep(1800)  # Sleep for 1800 seconds (30min)