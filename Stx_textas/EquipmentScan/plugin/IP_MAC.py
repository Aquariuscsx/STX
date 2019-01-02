from scapy.all import *
from queue import Queue


LISTEN = None

#扫描模块
class IP_MAC(object):

    def start(self,q,ip):
        self.q = q
        self.dstIP = ip
        d = {'ip':self.dstIP,'info':self.ip_mac(self.dstIP)}
        self.q.put(d)

    def ip_mac(self, cip):
        try:
            ans, unans = srp(Ether(dst="FF:FF:FF:FF:FF:FF") / ARP(pdst=cip), timeout=1, verbose=False)
        except Exception as e:
            print(str(e))
        else:
            return ans[0][1].sprintf("%Ether.src%")




#插件信息函数
def get_plugin_info():
    plugin_info = {
        "name": "IP_MAC.py",
        "model_name": "IP_MAC",
        "info": "用于存活ip及mac地址",
        "type": "IP",
        "brand": "IP",
    }
    return plugin_info


#启动扫描类
class Check():
    def __init__(self):
        self._ip = IP_MAC()

    @staticmethod
    def check(q,ip):
        Check()._ip.start(q,ip)



if __name__ == '__main__':
    ip = '192.168.0.110'
    q = Queue()
    Check().check(q,ip)
