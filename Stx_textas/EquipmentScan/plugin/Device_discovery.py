import struct

from libs.Plugin_Base import PluginBase

import socket

MYGROUP = '239.255.255.250'
GROUP_PORT = 1900
SENDERIP = '192.168.0.63'
SENDERIP_PORT = 19202
MYTTL = 64

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    # allow multiple sockets to use the same PORT number
sock.bind((SENDERIP,SENDERIP_PORT))
ttl_bin = struct.pack('@i',MYTTL)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.setsockopt(socket.IPPROTO_IP,
                             socket.IP_ADD_MEMBERSHIP,
                             socket.inet_aton(MYGROUP) + socket.inet_aton(SENDERIP))
# sock.bind(('192.168.0.63',19990))
class DeviceDiscovery(PluginBase):
    # 构造方法
    def __init__(self):
        self._to_group = '239.255.255.250'
        self._to_port = 1900
        self.pkg = 'M-SEARCH * HTTP/1.1\r\n''HOST: 239.255.255.250:1900\r\n''MAN: "ssdp:alive"\r\n''MX: 3\r\n''ST: ssdp:all\r\n''USER-AGENT: Google Chrome/71.0.3578.98 Windows\r\n'

    # 获取数据
    def start(self):
        try:

            while 1:
                lock.acquire()
                sock.sendto(self.pkg.encode('utf-8'),(MYGROUP,GROUP_PORT))
                print('send to ok.')
                lock.release()
                time.sleep(10)

        except:
            pass

    def stop(self):

        while 1:
            print('111111111111111111')
            result = sock.recv(4096)
            print(result)




def get_plugin_info():
    plugin_info = {
        "name": "Tiandy_Camera.py",
        "model_name": "Tiandy_Camera",
        "info": "用于扫描发现设备的插件",
        "type": "camera",
        "brand": "天地伟业",
    }
    return plugin_info


# 启动扫描类
class Check(object):
    def __init__(self):
        self.scan = DeviceDiscovery()

    def check(self):
        self.scan.start()
        return self

    def stop(self):
        self.scan.stop()


if __name__ == '__main__':
    import queue
    import  time
    import threading
    lock = threading.Lock()
    q = queue.Queue()
    s = threading.Thread(target=Check().check,name='SendTo')
    s.start()
    r = threading.Thread(target=Check().stop,name='SendTo')
    r.start()


