import ctypes
import sys
import psutil
from scanner.network import Interface

def is_admin() -> bool:
    if ctypes.windll.shell32.IsUserAnAdmin():
        return True
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
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