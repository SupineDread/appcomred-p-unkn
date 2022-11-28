import socket
from time import sleep
import ipaddress

def main():
    interfaces = socket.getaddrinfo(host=socket.gethostname(), port=None, family=socket.AF_INET)
    # allips = [ip[-1][0] for ip in interfaces]
    allips = []

    for interface in interfaces:
        ip = ipaddress.IPv4Interface(interface[-1][0])
        print(ip.netmask)
        allips.append(str(ip.netmask))

    message = b'Hello world'
    while True:
        for ip in allips:
            print(f'sending on {ip}')
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.bind((ip, 0))
            sock.sendto(message, ('255.255.255.255', 37020))
            sock.close()

        sleep(2)

main()
