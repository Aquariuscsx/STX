from _socket import *
import struct
import random


class PluginBase(object):
    _my_ip = '0.0.0.0'
    _my_port = 12345
    _to_ip = '0.0.0.0'
    _to_port = 3702
    _ttl = 20
    _to_group = '239.255.255.250'  # 组播组
    _sock = None

    def get_my_port(self):
        self._my_port = random.randint(10000, 60000)

    # 获取本地ip
    def get_local_ip(self):
        '''
        获取当前的本地ip
        :return: ip字符串
        '''
        s = socket(AF_INET, SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]  # 获取本机ip
        s.close()
        return ip

    # 发送数据到一个ip
    def send_one(self, data, timeout=2):
        '''
        发送数据到某个ip，ip值在对象属性中设置
        :param data: str | byte字符串 (数据内容)
        :return: 发送数据后的结果，单播为()
        '''
        dest_addr = (self._to_ip, self._to_port)
        self._sock = self.set_socket()
        self._sock.settimeout(timeout)
        # 尝试编码
        data = self._en_data(data)
        # 发送数据
        try:
            self._sock.sendto(data, dest_addr)
        except Exception as e:
            print(e)
        # d, addr = (None,None)
        import socket
        try:
            d, addr = self._sock.recvfrom(4096)
        except socket.timeout as e:
            return (None, None)
        except Exception as e:
            return e
        return (d, addr)

    # 发送消息到组播中
    def send_group(self, data, timeout=2):
        '''
        发送消息到组
        :param data: str | byte字符串 (数据内容)
        :param timeout: 接收数据超时时间
        :return: [(),()] ,
        '''
        self._sock = self.set_socket('group')
        self._sock.settimeout(timeout)
        dest_addr = (self._to_group, self._to_port)
        data = self._en_data(data)
        try:
            self._sock.sendto(data, dest_addr)
        except Exception as e:
            print(e)
        result = []
        import socket
        while True:
            try:
                d, addr = self._sock.recvfrom(4096)
                result.append((d, addr))
            except socket.timeout as e:
                return result
            except Exception as e:
                return e

    # 根据类型不同设置不同的socket包头
    def set_socket(self, type='one', option={}):
        '''
        设置单播或组播，
        :param type: "one"|"group"
        :param option: 其他参数
        :return: type->socket 一个设置好的socket包头
        '''
        my_addr = (self._my_ip, self._my_port)

        if type == 'group':
            group = self._to_group
            sock = self.make_group_socket(my_addr, group)
        else:
            sock = self.make_default_socket(my_addr)
        return sock

    # 创建一个组播socket包
    def make_group_socket(self, my_addr, group):
        '''
        工具方法，创建组播包头
        :param my_addr: (ip,port) 一个自己地址的元组
        :param group:  发送组的字符串
        :return: type->socket 一个设置好的socket包头
        '''
        sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
        sock.bind(my_addr)
        # Set Time-to-live (optional)
        ttl_bin = struct.pack('@i', self._ttl)
        sock.setsockopt(IPPROTO_IP, IP_MULTICAST_TTL, ttl_bin)
        sock.setsockopt(IPPROTO_IP, IP_ADD_MEMBERSHIP, inet_aton(group) + inet_aton(my_addr[0]))  # 加入到组播组
        return sock

    def make_default_socket(self, my_addr):
        '''
        工具方法，创建组播包头
        :param my_addr: (ip,port) 一个自己地址的元组
        :return: type->socket 一个设置好的单播socket包头
        '''
        sock = socket(AF_INET, SOCK_DGRAM)
        sock.bind(my_addr)
        return sock

    def _en_data(self, data):
        '''
        尝试格式化发送的包
        :param data: str|byte 要发送的包
        :return: str 一个可以发送的包
        '''
        try:
            dat = data.encode('utf8')
        except Exception as e:
            dat = data
        return dat

    # 对赋值做安全限制
    def __setattr__(self, name, value):
        '''
        对赋值做安全限制
        :param name: 要设置的属性
        :param value: 属性的值
        :return: None
        '''
        self.__dict__[name] = value
        # print(name, value)

    # 删除对象时候的方法
    def __del__(self):
        '''
        销毁socket链接
        :return:
        '''
        if (self._sock is not None) and isinstance(self, socket):
            self._sock.close()


# 测试举例
class HaiKan(PluginBase):
    # 构造方法
    def __init__(self):

        self._to_port = 3702
        self._to_ip = '192.168.0.235'
        self._my_ip = self.get_local_ip()
        self.pkg = '<?xml version="1.0" encoding="utf-8"?><Probe><Types>inquiry</Types></Probe>'
        # self.pkg = b"\xbe\xbe\xe5\xe5\x00\x00\x00\x00\x1e\x00\x49\x50\x09\x49\x50\x09" \
        #            b"\x4e\x45\x57\x4d\x34\x56\x30\x30\x09\x43\x4d\x44\x09\x53\x45\x45" \
        #            b"\x4b\x4e\x56\x53\x53\x0a\x0a\x0a"
        # self.pkg = '<?xml version="1.0" encoding="UTF-8"?>\n<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://www.w3.org/2003/05/soap-envelope" xmlns:SOAP-ENC="http://www.w3.org/2003/05/soap-encoding" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xop="http://www.w3.org/2004/08/xop/include" xmlns:wsa="http://schemas.xmlsoap.org/ws/2004/08/addressing" xmlns:tns="http://schemas.xmlsoap.org/ws/2005/04/discovery" xmlns:dn="http://www.onvif.org/ver10/network/wsdl" xmlns:wsa5="http://www.w3.org/2005/08/addressing"><SOAP-ENV:Header><wsa:MessageID>urn:uuid:E118C7D8-B8FE-4792-B0A1-6949F68DD7FF</wsa:MessageID><wsa:To SOAP-ENV:mustUnderstand="true">urn:schemas-xmlsoap-org:ws:2005:04:discovery</wsa:To><wsa:Action SOAP-ENV:mustUnderstand="true">http://schemas.xmlsoap.org/ws/2005/04/discovery/Probe</wsa:Action></SOAP-ENV:Header><SOAP-ENV:Body><tns:Probe><tns:Types>dn:NetworkVideoTransmitter</tns:Types></tns:Probe></SOAP-ENV:Body></SOAP-ENV:Envelope>'
        self.pkg2 = '<?xml version="1.0" encoding="utf-8"?><Envelope xmlns:tds="http://www.onvif.org/ver10/device/wsdl" xmlns="http://www.w3.org/2003/05/soap-envelope"><Header><wsa:MessageID xmlns:wsa="http://schemas.xmlsoap.org/ws/2004/08/addressing">uuid:4b11ceee-cd13-4853-a285-212a44c68011</wsa:MessageID><wsa:To xmlns:wsa="http://schemas.xmlsoap.org/ws/2004/08/addressing">urn:schemas-xmlsoap-org:ws:2005:04:discovery</wsa:To><wsa:Action xmlns:wsa="http://schemas.xmlsoap.org/ws/2004/08/addressing">http://schemas.xmlsoap.org/ws/2005/04/discovery/Probe</wsa:Action></Header><Body><Probe xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns="http://schemas.xmlsoap.org/ws/2005/04/discovery"><Types>tds:Device</Types><Scopes /></Probe></Body></Envelope>'
        #

    # 获取数据
    def get_data(self):

        self._to_port = 37020
        result1 = self.send_group(self.pkg)
        self._to_port = 3702
        self._my_port = 9992
        result = self.send_group(self.pkg2)
        print(len(result1+result))

        return result


if __name__ == "__main__":
    hk = HaiKan()
    print(hk.get_data())

    # pkg = '<?xml version="1.0" encoding="utf-8"?><Probe><Types>inquiry</Types></Probe>'
    # pkg = '<?xml version="1.0" encoding="utf-8"?><Envelope xmlns:tds="http://www.onvif.org/ver10/device/wsdl" xmlns="http://www.w3.org/2003/05/soap-envelope"><Header><wsa:MessageID xmlns:wsa="http://schemas.xmlsoap.org/ws/2004/08/addressing">uuid:4b11ceee-cd13-4853-a285-212a44c68011</wsa:MessageID><wsa:To xmlns:wsa="http://schemas.xmlsoap.org/ws/2004/08/addressing">urn:schemas-xmlsoap-org:ws:2005:04:discovery</wsa:To><wsa:Action xmlns:wsa="http://schemas.xmlsoap.org/ws/2004/08/addressing">http://schemas.xmlsoap.org/ws/2005/04/discovery/Probe</wsa:Action></Header><Body><Probe xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns="http://schemas.xmlsoap.org/ws/2005/04/discovery"><Types>tds:Device</Types><Scopes /></Probe></Body></Envelope>'
    # pkg = b"\x4e\x44\x54\x31\x08\x00\x27\xce\x13\x0b\x00\x00\x00\x00\x00\x00\x00\x01\x31\x2e\x33\x2e\x30\x2e\x30\x00\x32\x32\x34\x2e\x31\x36\x2e\x33"
    # pkg = '<?xml version="1.0" encoding="utf-8"?><Envelope xmlns:dn="http://www.onvif.org/ver10/network/wsdl" xmlns="http://www.w3.org/2003/05/soap-envelope"><Header><wsa:MessageID xmlns:wsa="http://schemas.xmlsoap.org/ws/2004/08/addressing">uuid:c662530d-1445-464a-95a8-73808841ebeb</wsa:MessageID><wsa:To xmlns:wsa="http://schemas.xmlsoap.org/ws/2004/08/addressing">urn:schemas-xmlsoap-org:ws:2005:04:discovery</wsa:To><wsa:Action xmlns:wsa="http://schemas.xmlsoap.org/ws/2004/08/addressing">http://schemas.xmlsoap.org/ws/2005/04/discovery/Probe</wsa:Action></Header><Body><Probe xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns="http://schemas.xmlsoap.org/ws/2005/04/discovery"><Types>dn:NetworkVideoTransmitter</Types><Scopes /></Probe></Body></Envelope>'

    # base = PluginBase()
    # base._data = pkg
    # base._my_ip = base.get_local_ip()
    #
    # base._to_ip = '192.168.0.237'
    # base._to_port = 3000
    # # base.send_one(pkg)
    # base.send_one(pkg)
