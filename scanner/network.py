import psutil
import struct
import socket

class Interface:

    def __init__(self, interface_name: str) -> None:
        self.name = interface_name
        self.MAC, ip = self._get_addrs()
        self.ip_address = ip[0]
        self.ip_mask = ip[1]


    def _get_addrs(self):
        addrs = psutil.net_if_addrs()[self.name]
        # Looping through nethwork addresses
        for addr in addrs:
            # -1 is the code for AF_LINK family
            if addr.family == -1:
                mac_address = addr.address
            # 2 is the code for AF_INET family
            if addr.family == 2:
                ip_address = addr.address
                mask = addr.netmask
        return mac_address, (ip_address, mask)


class Packet:
    
    def __init__(self, interface: Interface, target_ip: str) -> None:
        eth_header = struct.pack(
            '!6s6sH',
            bytes.fromhex('000000000000'), # Target MAC
            bytes.fromhex(interface.MAC.replace('-', '')), # Source MAC
            0x0806 # EtherType
        )

        arp_payload = struct.pack(
            '!HHBBH6s4s6s4s',
            0x0001, # Hardware Type
            0x0800, # IPv4
            6, # Hardware Address Length
            4, # Protocol Address Length
            0x0001, # Operation code
            bytes.fromhex(interface.MAC.replace('-', '')), # Source MAC
            socket.inet_aton(interface.ip_address), # Source IP
            bytes.fromhex('000000000000'), # Target MAC
            socket.inet_aton(target_ip) # Target IP
        )

        self.packet = eth_header + arp_payload


if __name__ == "__main__":
    inter = Interface('Wi-Fi')
    pack = Packet(inter, '192.168.0.1')
    print(pack.packet)

