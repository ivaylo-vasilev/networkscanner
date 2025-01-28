#!/usr/bin/python3

import socket
import re
import time
import sys
from colorama import init, Fore

init(autoreset=True)
GRN = Fore.LIGHTGREEN_EX
RED = Fore.LIGHTRED_EX
YLW = Fore.LIGHTYELLOW_EX
RST = Fore.RESET


def main():
    print(banner())
    print("[*] Specify range of IP addresses [example: 192.168.1.1-255]")
    print("=" * 60)
    ip_range = input(">>> ")
    print("\n *  Scanning network ...\n")
    hosts = network_mapper(ip_range)
    network_devices = hosts_identifier(hosts)

    print("========== SCANNING RESULTS ==========\n")

    if len(network_devices) == 0:
        print(f"{YLW}[-] No devices detected{RST}")
        sys.exit(0)
    
    n = len(network_devices)

    print(f"{GRN}[+] {n} device(s) detected{RST}\n")
    
    for i, device in enumerate(network_devices):
        print(f"[{i + 1}] {device}")


def network_mapper(ip_range):
    network = base_network(ip_range)
    if network == False:
        print(f"{RED}[!] Could not set network{RST}")
        sys.exit(1)
    ip_addresses = ip_range.split(".")[-1]
    if "-" not in ip_addresses:
        print(f"{RED}[!] Specify a range of hosts{RST}")
        sys.exit(2)
    a, b = ip_addresses.split("-")
    hosts = []
    for ip in range(int(a), int(b) + 1):
        host = network + str(ip)
        hosts.append(host)
    
    return hosts


def base_network(ip_range):
    if matches := re.search(r"^(\d{1,3}\.\d{1,3}\.\d{1,3}\.)\d{1,3}(?:-\d{1,3})?$", ip_range):
        return matches.group(1)
    else:
        return False


def hosts_identifier(hosts):
    network_devices = []
    try:
        for host in hosts:
            print(f"IP: {host}", end="\r")
            try:
                hostname = socket.gethostbyaddr(host)
                network_devices.append(f"IP: {host} | Hostname: {hostname[0]}")
                print(f"{GRN}IP: {host}{RST}", end="\r")
                time.sleep(2)
            except socket.gaierror:
                continue
            except socket.herror:
                continue
    except KeyboardInterrupt:
        print(" " * 25, end="\r")
    finally:
        print(" " * 25, end="\r")
        return network_devices


def banner():
    return """
            **************************
            *                        *
            *     NetworkScanner     *
            *                        *
            * ---------------------- *
            * (c)2025 Ivaylo Vasilev *
            **************************
            **************************
        """


if __name__ == "__main__":
    main()
