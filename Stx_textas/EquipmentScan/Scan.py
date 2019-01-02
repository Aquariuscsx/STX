import os
import sys
import threading
import queue
from importlib import import_module
from models import Info,Plugin,Batch,Config
from libs.management import ConfigManage
from exts import db,create_app
from libs.common import get_now
from config import devel,prod
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import time
import _thread

if len(sys.argv) > 1:
    engine = create_engine(devel.DB_URI)
else:
    engine = create_engine(prod.DB_URI)
DB_Session = sessionmaker(bind=engine)


sys.path.append(sys.path[0] + '/EquipmentScan/plugin/')


#初始化本地插件
class InitPlugin(object):

    def __init__(self):
        self.script_plugin = []

    def init(self):
        file_list = os.listdir(sys.path[0] + '/plugin')
        for filename in file_list:
            try:
                if filename.split('.')[1] == 'py':
                    res_tmp = import_module(filename.split('.')[0])
                    plugin_info = res_tmp.get_plugin_info()
                    self.save_plugin(plugin_info)
            except Exception as e:
                print(e)

    def save_plugin(self,plugin_info):
        plugin_ = Plugin.query.filter(Plugin.name == plugin_info['name']).first()
        if plugin_:
            plugin = plugin_
        else:
            plugin = Plugin()
        for key, value in plugin_info.items():
            setattr(plugin,key,value)
        if not plugin_:
            db.session.add(plugin)
        db.session.commit()


#设备扫描模块
class EquipmentScan(object):

    def __init__(self,target,survive_ip,plugin_list=None):
        self.survive_total = survive_ip.qsize()
        self.total = 0 #结果总数
        self.start_time = get_now() #扫描开始时间
        self.target = target #目标
        self.survive_ip = survive_ip #存活IP
        self.camera = queue.Queue() #摄像头结果队列
        # self.pc = queue.Queue() #PC结果队列
        # self.router = queue.Queue() #路由器结果队列
        # self.other = queue.Queue() #其他设备

        if plugin_list:
            self.plugin_list = plugin_list
        else:
            self.plugin_list = []
            all = db.session.query(Plugin.model_name).filter().all()
            for i in all:
                self.plugin_list.append(i[0])


    #添加批次信息
    def set_batch(self):
        app = create_app(__name__)
        with app.app_context():
            plugin_parameter = {}
            for i in self.plugin_list:
                config = Config.query.filter(Config.key.like(i + '%')).all()
                for c in config:
                    plugin_parameter[c.key] = c.value
            for i in ['thread_num','port_list','recv_num']:
                config = Config.query.filter(Config.key.like(i + '%')).all()
                for c in config:
                    plugin_parameter[c.key] = c.value

            dic = {'target':str(self.target), 'start_time': self.start_time,
                   'plugin_parameter':str(plugin_parameter),'plugins':str(self.plugin_list)}
            batch = Batch()
            for key,value in dic.items():
                setattr(batch,key,value)
            db.session.add(batch)
            db.session.commit()
            self.batch = batch
            self.batch_id = batch.id


    def scan(self):
        while True:
            ip = self.survive_ip.get()
            print(ip,type(ip))
            for plugin in self.plugin_list:
                res_tmp = import_module(plugin)
                # plugin_type = res_tmp.get_plugin_info()['type']
                # if plugin_type == 'camera':
                #     q = self.camera
                # elif plugin_type == 'pc':
                #     q = self.pc
                # elif plugin_type == 'router':
                #     q = self.router
                # else:
                #     q = self.other
                res_tmp.Check.check(self.camera,ip)
            self.survive_ip.task_done()

    #取得扫描结果
    def get_result(self):
        app = create_app(__name__)
        with app.app_context():
            while True:
                ip = ''
                result = self.camera.get()
                self.total += 1
                if 'ip' in result:
                    ip = result['ip']
                elif 'IPv4Address' in result:
                    ip = result['IPv4Address']
                if ip:
                    info = Info.query.filter(Info.ip==ip,Info.batch_id==self.batch_id).first()
                    if info:
                        info.info = str(result)
                        info.batch_id = self.batch_id
                    else:
                        info = Info(ip=ip,info=str(result))
                        info.batch_id = self.batch_id
                        db.session.add(info)
                    db.session.commit()
                    self.camera.task_done()
                else:pass

    def run(self):
        self.set_batch()
        r = threading.Thread(target=self.get_result, args=())
        r.daemon = True
        r.start()
        app = create_app(__name__)
        with app.app_context():
            thread_num = ConfigManage.search('thread_num')
        for i in range(int(thread_num)):
            t = threading.Thread(target=self.scan,args=())
            t.daemon = True
            t.start()

        _thread.start_new_thread(self.progress, ())
        while True:
            self.survive_ip.join()
            self.camera.join()
            #扫描批次结束时间
            app = create_app(__name__)
            with app.app_context():
                end_time = get_now()
                self.batch.end_time = end_time
                self.batch.total = self.total
                db.session.add(self.batch)
                db.session.commit()
                print('结束')
            break

    def progress(self,progress=None)    :
        while True:
            time.sleep(1)
            progress = (str((self.survive_total - self.survive_ip.qsize()) / self.survive_total * 100).split('.')[0])
            app = create_app(__name__)
            with app.app_context():
                self.batch.progress = progress
                db.session.add(self.batch)
                db.session.commit()
            if progress == 100 or progress == '100':
                break



if __name__ == '__main__':
    app = create_app(__name__)
    with app.app_context():
        # plugin_list = []
        # all = db.session.query(Plugin.model_name).filter().all()
        # for i in all:
        #     plugin_list.append(i[0])
        # print(plugin_list)

        # survive_ip = ip_scan.ThreadIPScan.survive_ip('192.168.0.1-192.168.0.250')
        # e = EquipmentScan(survive_ip)
        # e.run()

        i = InitPlugin()
        i.init()




