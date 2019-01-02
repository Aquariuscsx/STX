# import socket
#
# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# # sock.bind(('192.168.0.63',5252))
#
# sock.settimeout(1)
#
# sock.sendto(
#     'M-SEARCH * HTTP/1.1\r\n'
#     'HOST: 239.255.255.250:1900\r\n'
#     'MAN: "ssdp:discover"\r\n'
#     'MX: 3\r\n'
#     'ST: urn:schemas-upnp-org:device:InternetGatewayDevice:1\r\n'
#     'USER-AGENT: Google Chrome/71.0.3578.98 Windows\r\n'.encode(
#         'utf-8'),('239.255.255.250',1900))
# print('11111')
# a = True
# while a:
#     try:
#         result = sock.recv(4096)
#         print(result)
#     except socket.timeout as e:
#
#         print(e)
#         a = False


#coding=utf8


import time
import struct
from socket import *

SENDERIP = '192.168.0.63'  # 本地ip
SENDERPORT = 37022  # 本地接口
MYPORT = 1900  # 发送数据到该端口
MYGROUP = '239.255.255.250'  # 组播组
MYTTL = 20  # 发送数据的TTL值

s = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
# s.bind((SENDERIP, SENDERPORT))
def sender():


    # Set Time-to-live (optional)
    ttl_bin = struct.pack('@i', MYTTL)
    s.setsockopt(IPPROTO_IP, IP_MULTICAST_TTL, ttl_bin)
    status = s.setsockopt(IPPROTO_IP,
                          IP_ADD_MEMBERSHIP,
                          inet_aton(MYGROUP) + inet_aton(SENDERIP))  # 加入到组播组
    while True:
        data = 'M-SEARCH * HTTP/1.1\r\n''HOST: 239.255.255.250:1900\r\n''MAN: "ssdp:discover"\r\n''MX: 3\r\n''ST: urn:schemas-upnp-org:device:InternetGatewayDevice:1\r\n''USER-AGENT: Google Chrome/71.0.3578.98 Windows\r\n'

        s.sendto(data.encode('utf8'), (MYGROUP, MYPORT))
        # result = s.recv(4096)
        # print(result)
        print("send data ok !")

        time.sleep(10)

#coding=utf8




def receiver():
    import time
    import socket

    while 1:
        result = s.recvfrom(4096)
        print(result)



if __name__ == "__main__":
    sender()
    # receiver()






