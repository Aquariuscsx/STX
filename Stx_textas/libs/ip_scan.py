import queue
import netaddr
from scapy.all import *
from scapy.layers.l2 import Ether, ARP
from libs.CIDR import cidr



class ArpScan(object):

    def __init__(self):
        self.survive_ip = queue.Queue()

    #识别是否是IP
    def identify(self,ip):
        compile_ip = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
        if compile_ip.match(ip):
            return True
        else:
            return False

    # arp扫描存活ip
    def arp_scan(self, target):
        try:
            ans, unans = srp(Ether(dst="FF:FF:FF:FF:FF:FF") / ARP(pdst=target),timeout=2)
            print("len:" + str(len(ans)))
        except Exception as e:
            print(e)
        else:
            for send, rcv in ans:
                ip = rcv.sprintf("%ARP.psrc%")
                self.survive_ip.put(ip)
                print(ip)

    def get_target(self,target):
        #输入C段ip时
        if '/' in target:
            if int(target.split('/')[1]) >= 25:
                self.arp_scan(target)
            elif 16 <= int(target.split('/')[1]) <= 24:
                ip = target.split('/')[0]
                if self.identify(ip):
                    target = cidr(target)
                    ip = target.split('-')[0]
                    period = target.split('-')[1].split('.')[2]
                    target = []
                    ip_ = ip.split('.')
                    for per in range(int(ip.split('.')[2]),int(period) + 1):
                        ip_[2] = str(per)
                        ip_[3] = '0'
                        result = '.'.join(ip_) + '/24'
                        target.append(result)
                    for ip in target:
                        self.arp_scan(ip)
        #输入ip段时
        elif '-' in target:
            start_ip = target.split('-')[0]
            end_ip = target.split('-')[1]
            if self.identify(start_ip) and self.identify(end_ip):
                cidrs = netaddr.iprange_to_cidrs(start_ip, end_ip)
                for k, v in enumerate(cidrs):
                    self.arp_scan(str(v))
        #输入单个ip时
        else:
            if self.identify(target):
                self.arp_scan(target)
        return self

    # 获取配置网段存活IP总
    @staticmethod
    def survive_scan(target):
        s = ArpScan().get_target(target)
        return s.survive_ip

    # 获取配置网段存活IP总数量
    @staticmethod
    def survive_ip_count(target):
        return ArpScan().get_target(target).survive_ip.qsize()


if __name__ == '__main__':
    # survive_ip = ArpScan.survive_scan('192.168.0.1/20')
    # print(survive_ip)
    t = ArpScan.survive_ip_count('192.168.0.0/22')
    print(t)



