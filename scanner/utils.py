import ctypes
import sys
import psutil

def is_admin():
    if ctypes.windll.shell32.IsUserAnAdmin():
        return True
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        return False
    
def get_interfaces():
    active_interfaces = []
    
    interfaces = psutil.net_if_stats()
    for interface, stats in interfaces.items():
        # Checking for up interfaces and excluding loopback
        if stats.isup == True and 'Loopback' not in interface:
            active_interfaces.append(interface)
    if not active_interfaces:
        raise Exception('No active interfaces or system language not supported')
    return active_interfaces

if __name__ == "__main__":
    get_interfaces()
