import scanner.utils as utils
from scanner.network import Interface, Packet
import socket
import struct
import binascii


if __name__ == "__main__":
    
    # Checking if user has administrator privileges
    if not utils.is_admin():
        raise Exception('Administrator privileges missing!')
    
    # Interface checking
    interfaces = utils.get_interfaces()
    # If there are multiple active interfaces i'll ask the user to choose the right one
    if len(interfaces) > 1:
        print(f'---- ACTIVE INTERFACES ----')
        for i in interfaces: print(i)
        interface = input("Choose interface: ")
        # Checking if input interface is correct
        if interface not in interfaces:
            raise Exception('Invalid interface name.')
    elif interfaces:
        interface = interfaces[0]
        print(f"Active interface: {interface}")
    else:
        raise Exception('No active interfaces.')
    
    # Creating interface object
    interface = Interface(interface)

    # Getting the list of all the possible network addresses
    targets = utils.get_all_network_addrs(interface)

    # For each target ip we send an ARP request
    net_hosts = []
    print('Scanning ...')
    for target in targets:
        sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))
        sock.bind((interface.name, 0))
        packet = Packet(interface, target).packet
        sock.send(packet)
        sock.settimeout(0.1) # 0.1 seconds  seconds
        try:
            while True:
                response = sock.recv(65535)
                response_ip , response_mac = utils.get_addresses(response)
                if response_ip is not None and not any(response_ip == host[0] for host in net_hosts):
                    net_hosts.append((response_ip, response_mac))

        except socket.timeout:
            pass

    # Printing all hosts found
    print('Scan complete.')
    for host in net_hosts:
        print(f'IP {host[0]} MAC {host[1]}')

    