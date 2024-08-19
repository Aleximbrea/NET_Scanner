from scanner.utils import ip_to_bin, bin_to_ip

def get_all_network_addrs(ip , mask) -> list:

    # Converting ip's to binary
    ip_bin = ip_to_bin(ip)
    mask_bin = ip_to_bin(mask)

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

if __name__ == '__main__':
    get_all_network_addrs('192.168.67.231', '255.255.255.0')
