import queue
import uuid
from libs.Plugin_Base import PluginBase
from xml.dom import minidom


# 测试举例
class HikvisionUDPScanner(PluginBase):
    # 构造方法
    def __init__(self):
        self._my_ip = self.get_local_ip()
        self.get_my_port()

    @staticmethod
    def get_discover_xml():
        # 标准XML声明
        standard = '<?xml version="1.0" encoding="utf-8"?>'
        # 创建XML根节点Probe
        dom_impl = minidom.getDOMImplementation()
        send_document = dom_impl.createDocument(None, 'Probe', None)
        send_root = send_document.documentElement
        # 创建子结点Uuid
        uuid_e = send_document.createElement('Uuid')
        uuid_t = send_document.createTextNode(str(uuid.uuid1()).upper())
        uuid_e.appendChild(uuid_t)
        send_root.appendChild(uuid_e)
        # 创建子结点Types
        types_e = send_document.createElement('Types')
        types_t = send_document.createTextNode('inquiry')
        types_e.appendChild(types_t)
        send_root.appendChild(types_e)
        # 合成标准XML字符串
        result = standard + send_root.toxml()
        return result

    @staticmethod
    def parser(data) -> dict:
        assert isinstance(data, str)
        # 去除前面的XML描述符
        data = data[39:]  # 39
        # 接收到的XML对象
        # try:
        recv_xml = minidom.parseString(data)
        # 获取XML对象的根结点
        recv_root = recv_xml.documentElement
        # 设备信息字典类型
        dev_dict = {}
        # 判断根结点名称是否为ProbeMatch
        if recv_root.nodeName == 'ProbeMatch':
            # 获得根结点的所有子结点
            recv_childnodes = recv_root.childNodes
            for childnode in recv_childnodes:
                # 过滤掉内容仅为\n的结点
                if isinstance(childnode.childNodes, list) is True:
                    # 设置字典，Key为字段名称，Value为字段的值
                    dev_dict[childnode.nodeName] = childnode.childNodes[0].data

            return dev_dict
        # except Exception as e:
        #     print(e)
        #     return {}
        # else:
        #     raise TypeError('不是探测包的返回包，返回包的根结点名称必须是ProbeMatch')

    # 获取数据
    def start(self,q,ip):
        self._to_port = 37020
        self._to_ip = ip
        self.pkg = self.get_discover_xml()
        result = self.send_one(self.pkg)
        if result[1]:
            result = str(result[0],'utf-8')
            result = self.parser(result)
            dic = {}
            dic['ip'] = result['IPv4Address']
            dic['info'] = result
            q.put(dic)


#插件信息函数
def get_plugin_info():
    plugin_info = {
        "name": "Hikvision_Camera.py",
        "model_name": "Hikvision_Camera",
        "info": "用于扫描海康威视品牌摄像头的插件",
        "type": "camera",
        "brand": "海康威视",
    }
    return plugin_info


#启动扫描类
class Check():
    def __init__(self):
        self.hika = HikvisionUDPScanner()

    @staticmethod
    def check(q,ip):
        Check().hika.start(q,ip)


if __name__ == '__main__':
    q = queue.Queue()
    ip  = '192.168.0.249'
    Check().check(q,ip)