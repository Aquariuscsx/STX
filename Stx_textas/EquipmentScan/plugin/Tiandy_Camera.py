from libs.Plugin_Base import PluginBase


class Tiandy_Camera(PluginBase):
    # 构造方法
    def __init__(self):
        self._my_ip = self.get_local_ip()
        self.get_my_port()
        self.pkg = b"\xbe\xbe\xe5\xe5\x00\x00\x00\x00\x1e\x00\x49\x50\x09\x49\x50\x09" \
                   b"\x4e\x45\x57\x4d\x34\x56\x30\x30\x09\x43\x4d\x44\x09\x53\x45\x45" \
                   b"\x4b\x4e\x56\x53\x53\x0a\x0a\x0a"

    # 获取数据
    def start(self, q, target):
        try:
            self._to_ip = target[0]
            self._to_port = 3000
            result = self.send_one(self.pkg)
            if result:
                dic = self.parse(result)
                q.put(dic)
        except:
            pass

    def stop(self):
        self._sock.close()

    def parse(self, res):
            dic = {}
            result = res[0][10:][:-2]
            result = result.decode(encoding='utf-8')
            result = result.split('\t')
            dic['device_brand'] = '天地伟业'
            dic['device_type'] = '摄像头'
            dic['ipv4_address'] = target[0]
            dic['mac'] = target[1]
            try:
                dic['http_address'] = 'http://' + target[0] + ':' + result[13]
                dic['device_description'] = result[2]
                dic['device_sn'] = result[15]
                dic['command_port'] = result[10]
                dic['other'] = res[0]
            except:
                dic['other'] = res[0]
            print(dic)
            return dic







def get_plugin_info():
    plugin_info = {
        "name": "Tiandy_Camera.py",
        "model_name": "Tiandy_Camera",
        "info": "用于扫描天地伟业品牌摄像头的插件",
        "type": "camera",
        "brand": "天地伟业",
    }
    return plugin_info


# 启动扫描类
class Check(object):
    def __init__(self):
        self.scan = Tiandy_Camera()

    def check(self, q, target):
        self.scan.start(q, target)
        return self

    def stop(self):
        self.scan.stop()


if __name__ == '__main__':
    import queue

    target = ['192.168.0.237', 'af:ae:73:c2:50:00']
    q = queue.Queue()
    Check().check(q, target)
