# Network Scanner

## Requirements
- Python 3
- Linux

## Get started

1. Check Python installation `python --version`
2. Clone this repository
3. Navigate to the directory with a terminal. **The terminal must have administrator privileges**
4. Install packages ``pip install -r requirements.txt``
5. Execute the script `python main.py`

## Description

In this script i wanted to manually create the packets for the ARP request. And send them using the __socket__ module.

Unfortunately i've found out that:

> [!IMPORTANT]
> Raw sockets are not supported on Windows

So i resigned myself to using __scapy__.

I will still keep the cool representation of the ethernet and arp frame.

## How it works


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

> [!NOTE]
> Since i'm using ***scapy*** all of this is managed by the module




## Notes
- The script only works with Class C networks (254 hosts max)