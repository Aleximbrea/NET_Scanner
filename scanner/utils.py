import os
import sys
import psutil
from scanner.network import Interface
import struct
import binascii
import socket

def is_admin() -> bool:
    if os.geteuid() == 0:
        return True
    else:
        # Se non si è root, lancia il comando con sudo
        print("You are not root!")
        os.execvp("sudo", ["sudo", sys.executable] + sys.argv)
        return False
    
def get_interfaces() -> list:
    active_interfaces = []
    
    interfaces = psutil.net_if_stats()
    for interface, stats in interfaces.items():
        # Checking for up interfaces and excluding loopback
        if stats.isup == True and 'Loopback' not in interface:
            active_interfaces.append(interface)
    if not active_interfaces:
        raise Exception('No active interfaces or system language not supported')
    return active_interfaces

def get_all_network_addrs(interface: Interface) -> list:

    # Converting ip's to binary
    ip_bin = ip_to_bin(interface.ip_address)
    mask_bin = ip_to_bin(interface.ip_mask)

    # Getting maximum numero of hosts on a network
    net_size = ((2 ** mask_bin.count('0')) - 2)
    if net_size > 254:
        raise Exception('Network too big.')


    # Getting net address and broadcast
    bin_net_address = ''.join(ip_bin[i] if mask_bin[i] == '1' else '0' for i in range(32))
    bin_broadcast = ''.join(ip_bin[i] if mask_bin[i] == '1' else '1' for i in range(32))

    int_bin_net_addrs = int(bin_net_address, 2)
    int_bin_broadcast = int(bin_broadcast, 2)

    # Getting an array with all host ip addresses
    ip_list = []
    for ip_int in range(int_bin_net_addrs + 1, int_bin_broadcast):
        ip_list.append(bin_to_ip(f'{ip_int:032b}'))
    return ip_list

def bin_to_ip(bin: str) -> str:
    return '.'.join(str(int(bin[i:i+8], 2)) for i in range(0, 32, 8))

def ip_to_bin(ip: str) -> str:
    return ''.join(f'{int(octet):08b}' for octet in ip.split('.'))

def get_addresses(response):
    sender_ip = None
    sender_mac = None
    ethernet_header = response[0:14]
    ethertype = struct.unpack('!H', ethernet_header[12:14])[0]

    if ethertype == 0x0806:
        arp_header = response[14:42]
        arp_data = struct.unpack('!HHBBH6s4s6s4s', arp_header)

        if arp_data[4] == 2:
            sender_mac = binascii.hexlify(arp_data[5]).decode()
            sender_ip = socket.inet_ntoa(arp_data[6])
    return sender_ip, sender_mac