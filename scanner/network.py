import psutil

class Interface:

    def __init__(self, interface_name: str) -> None:
        self.name = interface_name
        self.MAC, self.ip = self._get_addrs()


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
        return mac_address, ip_address



if __name__ == "__main__":
    pass

