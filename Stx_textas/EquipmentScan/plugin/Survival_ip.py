import re
import struct
from socket import *
import socket

import time

from libs.Plugin_Base import PluginBase

a = '<Envelope xmlns:dn="http://www.onvif.org/ver10/network/wsdl" xmlns="http://www.w3.org/2003/05/soap-envelope">'


class Survival_ip(PluginBase):

    def __init__(self):
        super(PluginBase, self).__init__()
        self._my_ip = self.get_local_ip()
        # 不要 Header 就只能访问天地伟业,有详细数据,不加body数据获取不到
        self.pkg1 = '<?xml version="1.0" encoding="utf-8"?><Envelope xmlns:dn="http://www.onvif.org/ver10/network/wsdl" xmlns="http://www.w3.org/2003/05/soap-envelope"><Header><wsa:MessageID xmlns:wsa="http://schemas.xmlsoap.org/ws/2004/08/addressing">uuid:c662530d-1445-464a-95a8-73808841ebeb</wsa:MessageID><wsa:To xmlns:wsa="http://schemas.xmlsoap.org/ws/2004/08/addressing">urn:schemas-xmlsoap-org:ws:2005:04:discovery</wsa:To><wsa:Action xmlns:wsa="http://schemas.xmlsoap.org/ws/2004/08/addressing">http://schemas.xmlsoap.org/ws/2005/04/discovery/Probe</wsa:Action></Header><Body><Probe xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns="http://schemas.xmlsoap.org/ws/2005/04/discovery"><Scopes /></Probe></Body></Envelope>'
        self.pkg = '<?xml version="1.0" encoding="utf-8"?><Probe><Types>inquiry</Types></Probe>'

    def start(self, q, target):
        try:
            self._to_ip = target[0]
            self._to_port = 3702
            self._my_port = 65033
            result1 = self.send_group(self.pkg1)
            self._to_port = 37020
            self._my_port = 62205
            result2 = self.send_group(self.pkg)
            result = result1 + result2

            for i in result:
                if self._to_ip == i[1][0]:
                    info_list = i[0]
                    info_list = info_list.decode('utf-8')
                    print(info_list)
                    from bs4 import BeautifulSoup
                    XML = BeautifulSoup(info_list, 'lxml')
                    try:
                        onvif_list = []
                        # 取出onvif 部分的值
                        for i in XML.find(re.compile('scopes')).get_text().split(' '):
                            if i != "": onvif_list.append(i)
                        onvif_list = [i.split('org/')[1] for i in onvif_list]
                        items = [items.split('/', 1) for items in onvif_list]
                        types = []
                        for i in items:
                            if i[0] == 'type': types.append(i[1])
                        for item in items:
                            if len(item) < 2: item.append('None')
                        # 设备的管理地址
                        service_addr = XML.find(re.compile('xaddr')).get_text().split('/onvif')[0]
                        # 设备的uuid
                        uuid = XML.find(re.compile('address')).get_text().split('uuid:')[1]
                        dic = {'ip': target[0], 'type': '摄像头', 'Uuid': uuid, 'ServiceAddr': service_addr,
                               'types': types}
                        for a in range(len(items)):
                            if items[a][0] != 'type': dic[items[a][0]] = items[a][1]
                        q.put(dic)
                        print(dic)
                    except:
                        try:
                            print(XML)
                            # 海康威视解析
                            type = XML.find('types').get_text()  # 设备类型
                            Uuid = XML.find('uuid').get_text()  # 设备描述
                            DeviceType = XML.find('devicetype').get_text()  # 设备描述
                            DeviceDescription = XML.find('devicedescription').get_text()  # 设备描述
                            DeviceSN = XML.find('devicesn').get_text()  # 设备序列号
                            CommandPort = XML.find('commandport').get_text()  # 远程端口
                            HttpPort = XML.find('httpport').get_text()  # 端口
                            MAC = XML.find('mac').get_text()  # MAC地址
                            IPv4Address = XML.find('ipv4address').get_text()  # ipv4地址
                            SubnetMask = XML.find('ipv4subnetmask').get_text()  # 子网掩码
                            Gateway = XML.find('ipv4gateway').get_text()  # 网关
                            SoftwareVersion = XML.find('softwareversion').get_text()
                            DHCP = XML.find('dhcp').get_text()
                            AnalogChannelNum = XML.find('analogchannelnum').get_text()
                            DSPVersion = XML.find('digitalchannelnum').get_text()
                            BootTime = XML.find('boottime').get_text()
                            OEMInfo = XML.find('oeminfo').get_text()
                            EZVIZCode = XML.find('ezvizcode').get_text()
                            Activated = XML.find('activated').get_text()
                            PasswordResetAbility = XML.find('passwordresetability').get_text()
                            dic = {'ip': i[1][0], 'type': '摄像头'}
                            info = {'Uuid': Uuid, 'types': type, 'DeviceType': DeviceType,
                                    'DeviceDescription': DeviceDescription, 'DeviceSN': DeviceSN,
                                    'CommandPort': CommandPort,
                                    'HttpPort': HttpPort, 'MAC': MAC, 'IPv4Address': IPv4Address,
                                    'IPv4SubnetMask': SubnetMask,
                                    'IPv4Gateway': Gateway, 'SoftwareVersion': SoftwareVersion,
                                    'DHCP': DHCP, 'AnalogChannelNum': AnalogChannelNum, 'DSPVersion': DSPVersion,
                                    'BootTime': BootTime, 'OEMInfo': OEMInfo, 'EZVIZCode': EZVIZCode,
                                    'Activated': Activated, 'PasswordResetAbility': PasswordResetAbility}
                            dic['info'] = info
                            q.put(dic)
                            print(dic)
                        except:
                            dic = {'ip': target[0], 'type': '摄像头', 'info': info_list}
                            q.put(dic)
                            print(dic)
        except BaseException as e:
            print(e)

    def stop(self):
        pass


def get_plugin_info():
    plugin_info = {
        "name": "Survival_ip.py",
        "model_name": "Survival_ip",
        "info": "用于判断是否是摄像头的插件",
        "type": "camera",
        "brand": "摄像头发现",
    }
    return plugin_info


# 启动扫描类
class Check(object):
    def __init__(self):
        self.scan = Survival_ip()

    def check(self, q, target):
        self.scan.start(q, target)

    def stop(self):
        self.scan.stop()


if __name__ == '__main__':
    import queue

    q = queue.Queue()
    # target = ['192.168.0.237', '']
    # Check().check(q, target)
    ip_list = [['192.168.0.249', ''], ['192.168.0.110', ''], ['192.168.0.237', ''], ['192.168.0.235', ''],
               ['192.168.0.129', ''], ['192.168.0.88', ''], ]
    for ip in ip_list:
        # ip = ['192.168.0.237', '']
        Check().check(q, ip)
