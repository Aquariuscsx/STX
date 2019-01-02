import queue
from libs.Plugin_Base import PluginBase

# 测试举例
class DahuaUDPScanner(PluginBase):
    # 构造方法
    def __init__(self):
        self._my_ip = self.get_local_ip()
        self.get_my_port()

    def parser(self):
        return

    # 获取数据
    def start(self,q,ip):
        self._to_port = 37810
        self._to_ip = ip
        self.pkg = b"\0\0\0\0DHIP\0\0\0\0\0\0\0\0I\0\0\0\0\0\0\0I\0\0\0\0\0\0\0{ \"method\" : \"DHDiscover.search\", \"params\" : { \"mac\" : \"\", \"uni\" : 1 } }\n"
        result = self.send_one(self.pkg)
        print(result[0][32:][:-2])
        if result[1]:
            result = str(result[0][32:][:-2],'utf-8')
            print(result)
            dic = {}
            dic['ip'] = result[1][0]
            dic['info'] = result[0]
            q.put(dic)


#插件信息函数
def get_plugin_info():
    plugin_info = {
        "name": "Dahua_Camera.py",
        "model_name": "Dahua_Camera",
        "info": "用于扫描大华品牌摄像头的插件",
        "type": "camera",
        "brand": "大华",
    }
    return plugin_info


#启动扫描类
class Check():
    def __init__(self):
        self.dahua = DahuaUDPScanner()

    @staticmethod
    def check(q,ip):
        Check().dahua.start(q,ip)


if __name__ == '__main__':
    q = queue.Queue()
    ip  = '192.168.0.129'
    Check().check(q,ip)