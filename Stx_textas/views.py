import sys
import json
import _thread
import importlib
import threading
from flask import Flask,render_template,request,redirect,url_for
from libs import ip_scan
from libs.management import ConfigManage
from exts import db
from config import devel,prod
from models import Info,Plugin,Batch,Config
from EquipmentScan.Scan import EquipmentScan


app = Flask(__name__)

SURVIVE_IP = 0

app.config.from_object(prod)
if len(sys.argv) > 1:
    extra_config = importlib.import_module('config.%s' % sys.argv[1])
    app.config.from_object(extra_config)

db.init_app(app)

try:
    db.create_all(app=app)
except Exception as e:
    print(e)


@app.route('/')
def _index():
    return redirect(url_for('_scan'))

#扫描页面
@app.route('/scan/',methods=['GET','POST'])
def _scan():
    if request.method == 'GET':
        plugin = Plugin.query.filter().all()
        context = {
            'plugin': plugin,
        }
        return render_template('video-start.html',**context)
    elif request.method == 'POST':
        target = request.form.get('target','')
        plugin_list = request.form.getlist('plugin_list[]')

        def ttt(target, plugin_list):
            survive_ip = ip_scan.ArpScan.survive_scan(target)
            t = threading.Thread(target=EquipmentScan(target, survive_ip, plugin_list).run())
            t.start()

        _thread.start_new_thread(ttt,(target, plugin_list))
        return 'success'

@app.route('/progress_bar/',methods=['GET','POST'])
def _progress_bar():
    if request.method == 'POST':
        batch = Batch.query.filter().order_by(Batch.id.desc()).first()
        info  = []
        if batch:
            for i in batch.information:
                dic = {}
                for key in ['id', 'ip', 'info']:
                    dic[key] = getattr(i, key)
                info.append(dic)
            if not batch.total:
                batch.total = 0
            if not batch.progress:
                batch.progress = 0

            context = {
                'progress': int(batch.progress),
                'info':info,
                'total':int(batch.total),
            }
            return json.dumps(context)
        else:
            context = {
                'progress': 0,
                'info': [],
                'total': 0,
            }
            return json.dumps(context)
    elif request.method == 'GET':
        context = {
            'progress':0,
            'info':[],
            'total':0,
        }
        return render_template('video-being.html', **context)


#配置页面
@app.route('/config/',methods=['GET','POST'])
def _config():
    if request.method == 'GET':
        for i in ['hikvision_camera_slice','hikvision_camera_port','keda_camera_port',
                  'dahua_camera_port','thread_num','port_list''recv_num']:
            i = Config.query.filter(Config.key == i).first()

        hikvision_camera_slice = Config.query.filter(Config.key == 'hikvision_camera_slice').first()
        hikvision_camera_port = Config.query.filter(Config.key == 'hikvision_camera_port').first()
        keda_camera_port = Config.query.filter(Config.key == 'keda_camera_port').first()
        dahua_camera_port = Config.query.filter(Config.key == 'dahua_camera_port').first()

        thread_num = Config.query.filter(Config.key == 'thread_num').first()
        port_list = Config.query.filter(Config.key == 'port_list').first()
        recv_num = Config.query.filter(Config.key == 'recv_num').first()
        context = {
            'hikvision_camera_slice':hikvision_camera_slice,
            'hikvision_camera_port':hikvision_camera_port,
            'keda_camera_port':keda_camera_port,
            'dahua_camera_port':dahua_camera_port,
            'port_list': port_list,
            'thread_num': thread_num,
            'recv_num': recv_num,
        }
        return render_template('config.html',**context)
    elif request.method == 'POST':
        #海康插件变量
        hikvision_camera_port = request.form.get('hikvision_camera_port','')
        hikvision_camera_slice = request.form.get('hikvision_camera_slice','')
        #科达插件变量
        keda_camera_port = request.form.get('keda_camera_port', '')
        #大华插件变量
        dahua_camera_port = request.form.get('dahua_camera_port', '')

        #平台变量
        thread_num = request.form.get('thread_num','')
        port_list = request.form.get('port_list','')
        recv_num = request.form.get('recv_num','')
        dic = {'thread_num':thread_num,'port_list':port_list,'hikvision_camera_port':hikvision_camera_port,
               'hikvision_camera_slice':hikvision_camera_slice,'keda_camera_port':keda_camera_port,
               'dahua_camera_port':dahua_camera_port,'recv_num':recv_num}
        for key,value in dic.items():
            ConfigManage.update(key,value)
        return 'success'

#搜索页面
@app.route('/search/',methods=['GET','POST'])
def _search():
    if request.method == 'GET':
        return render_template('search.html')
    elif request.method == 'POST':
        q = request.form.get('q','')
        if (':' in q) and (q.split(':')[0] == 'pi'):
            info = Batch.query.filter(Batch.id == q.split(':')[1]).first()
            if info:
                info = info.information
            else:info = ''
        else:
            info = Info.query.filter(Info.ip == q).all()
        context = {
            'info': info,
        }
        return render_template('detail.html',**context)

