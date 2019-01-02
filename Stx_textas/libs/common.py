from exts import db
import datetime

def get_ip_list(ip):
    ip_list_tmp = []
    iptonum = lambda x: sum([256 ** j * int(i) for j, i in enumerate(x.split('.')[::-1])])
    numtoip = lambda x: '.'.join([str(x // (256 ** i) % 256) for i in range(3, -1, -1)])
    if '-' in ip:
        ip_range = ip.split('-')
        ip_start = int(iptonum(ip_range[0]))
        ip_end = int(iptonum(ip_range[1]))
        ip_count = ip_end - ip_start
        if ip_count >= 0 and ip_count <= 655360:
            for ip_num in range(ip_start, ip_end + 1):
                ip_list_tmp.append(numtoip(ip_num))
        else:
            print('IP格式错误')
    else:
        ip_split = ip.split('.')
        net = len(ip_split)
        if net == 2:
            for b in range(1,255):
                for c in range(1,255):
                    ip = '%s.%s.%d.%d'%(ip_split[0],ip_split[1],b,c)
                    ip_list_tmp.append(ip)
        elif net == 3:
            for c in range(1,255):
                ip = '%s.%s.%s.%d'%(ip_split[0],ip_split[1],ip_split[2],c)
                ip_list_tmp.append(ip)
        elif net == 4:
            ip_list_tmp.append(ip)
        else:
            print('IP格式错误')
    return ip_list_tmp


#判断ip设备是否更改，有更改则报警
def test_warning(dic,model,warning_model):
    instance = model.query.filter(dic['ip']).first()
    for key,value in dic:
        if value != getattr(instance,key):
            warning_instance_ = warning_model.query.filter(dic['ip']).first()
            if warning_instance_:
               warning_instance = warning_instance_
            else:
                warning_instance = warning_model()
            for key,value in dic:
                setattr(warning_instance,key,value)
            if not warning_instance_:
                db.session.add(warning_instance)
            db.session.commit()


#获取当前时间
def get_now():
    now = datetime.datetime.now()
    return now




