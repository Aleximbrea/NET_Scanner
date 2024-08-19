# Network Scanner

## Explanation

In this script i wanted to manually create the packets for the ARP request.

The packet operates at levels 2 and 3 of the osi model: **Data Link Layer** and **Network Layer**.

For the ethernet frame we only need to provide the following fields, the rest of it is managed at lower levels.
|      **Fields**     | MAC Destination | Mac Source | EtherType | Payload |
|:-------------------:|:---------------:|:----------:|:---------:|:-------:|
| **Length** (octets) |        6        |      6     |     2     | 42-1500 |

- **MAC Destination** is FF:FF:FF:FF:FF:FF for broadcast
- **Ethertype** is 0x0806 for ARP

The **Payload** field contains the ARP request itself
|      **Fields**     | Hardware Type | Protocol Type | Hardware Addrs Length | Protocol Addrs Length | Operation | Sender Hardware Addrs | Sender Protocol Addrs | Target Hardware Addrs | Target Protocol Addrs |
|:-------------------:|:-------------:|:-------------:|:---------------------:|:---------------------:|:---------:|:---------------------:|:---------------------:|:---------------------:|:---------------------:|
| **Length** (octets) |       2       |       2       |           1           |           1           |     2     |           6           |           4           |           6           |           4           |

- **Hardware Type** is 1 for Ethernet
- **Protocol Type** is 0x0800 for IPv4
- **Operation** is 1 for ARP request, 2 for response

## Requirements
- Python 3
- Windows 10 / 11

## Get started

1. Check Python installation `python --version`
2. Clone this repository
3. Navigate to the directory with a terminal. **The terminal must have administrator privileges**
4. Install packages ``pip install -r requirements.txt``
5. Execute the script `python main.py`
   
      To check for active connections i use the `netsh interface show interface` command which returns an output based on the system language
      To filter the resaults i use the following statement:
      ```python
        if status == 'Connessione' or status == 'Connected':
      ```
      So if you are using another language it wont find active interfaces

## Notes
- The script only works with Class C networks with 254 hosts max