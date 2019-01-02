from queue import Queue
from libs.Plugin_Base import PluginBase


class YuShiCamera(PluginBase):
    # 构造方法
    def __init__(self):
        self._to_port = 3702
        self._my_ip = self.get_local_ip()
        self.get_my_port()
        self.pkg = '<?xml version="1.0" encoding="UTF-8"?>\n<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://www.w3.org/2003/05/soap-envelope" xmlns:SOAP-ENC="http://www.w3.org/2003/05/soap-encoding" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xop="http://www.w3.org/2004/08/xop/include" xmlns:wsa="http://schemas.xmlsoap.org/ws/2004/08/addressing" xmlns:tns="http://schemas.xmlsoap.org/ws/2005/04/discovery" xmlns:dn="http://www.onvif.org/ver10/network/wsdl" xmlns:wsa5="http://www.w3.org/2005/08/addressing"><SOAP-ENV:Header><wsa:MessageID>urn:uuid:E118C7D8-B8FE-4792-B0A1-6949F68DD7FF</wsa:MessageID><wsa:To SOAP-ENV:mustUnderstand="true">urn:schemas-xmlsoap-org:ws:2005:04:discovery</wsa:To><wsa:Action SOAP-ENV:mustUnderstand="true">http://schemas.xmlsoap.org/ws/2005/04/discovery/Probe</wsa:Action></SOAP-ENV:Header><SOAP-ENV:Body><tns:Probe><tns:Types>dn:NetworkVideoTransmitter</tns:Types></tns:Probe></SOAP-ENV:Body></SOAP-ENV:Envelope>'

    # 获取数据
    def start(self, q, ip):
        self._to_ip = ip
        result = self.send_one(self.pkg)
        if result[1]:
            dic = {}
            dic['ip'] = result[1][0]
            dic['info'] = result[0]
            q.put(dic)


# 插件信息函数
def get_plugin_info():
    plugin_info = {
        "name": "Yushi_Camera.py",
		"model_name":"Yushi_Camera",
        "info": "用于扫描宇视品牌摄像头的插件",
        "type": "camera",
        "brand": "宇视",
    }
    return plugin_info


# 启动扫描类
class Check():
    def __init__(self):
        self.yushi = YuShiCamera()

    @staticmethod
    def check(q, ip):
        Check().yushi.start(q, ip)


if __name__ == '__main__':
    ip = '192.168.0.235'
    q = Queue()
    Check().check(q, ip)
