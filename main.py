import scanner.utils as utils
from scanner.network import Interface

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
    
    