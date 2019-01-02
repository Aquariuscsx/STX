from libs.Plugin_Base import PluginBase
from queue import Queue


class KeDaCamera(PluginBase):

    # 构造方法
    def __init__(self):
        self._to_port = 5513
        self._my_ip = self.get_local_ip()
        self.get_my_port()
        self.pkg = b"\x4e\x44\x54\x31\x08\x00\x27\xce\x13\x0b\x00\x00\x00\x00\x00\x00\x00\x01\x31\x2e" \
                   b"\x33\x2e\x30\x2e\x30\x00\x32\x32\x34\x2e\x31\x36\x2e\x33"

    # 获取数据
    def start(self, q, t_ip):
        self.q = q
        self._to_ip = t_ip
        result = self.send_one(self.pkg)
        if result[1]:
            dic = {}
            dic['ip'] = result[1][0]
            dic['info'] = result[0]
            q.put(dic)


# 插件信息函数
def get_plugin_info():
    plugin_info = {
        "name": "Keda_Camera.py",
        "model_name": "Keda_Camera",
        "info": "用于扫描科达品牌摄像头的插件",
        "type": "camera",
        "brand": "科达",
    }
    return plugin_info


#启动扫描类
class Check():
    def __init__(self):
        self.hika = KeDaCamera()

    @staticmethod
    def check(q, t_ip):
        Check().hika.start(q, t_ip)

if __name__ == '__main__':
    t_ip = '192.168.0.152'
    q = Queue()
    Check().check(q, t_ip)