# socket1.py
import psutil
import socket

def get_wifi_ipv4_address():
    wifi_interface_name = None
    for interface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == socket.AF_INET and ('wlan' in interface or 'Wi-Fi' in interface):
                wifi_interface_name = interface
                return addr.address
    return None

wifi_ipv4_address = get_wifi_ipv4_address()
print(wifi_ipv4_address)