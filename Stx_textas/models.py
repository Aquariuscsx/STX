from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from exts import db
from sqlalchemy.orm import foreign, remote

db.Model.__table_args__ = {'mysql_engine':'InnoDB' , 'mysql_charset':'utf8'}
#
# #摄像头信息
# class Camera(db.Model):
#     __tablename__ = 'camera'
#     id = db.Column(db.Integer , primary_key=True , autoincrement=True)
#     uuid = db.Column(db.String(80) , nullable=False) #uuid
#     types = db.Column(db.Text , nullable=False) #设备类型
#     device_type = db.Column(db.Integer) #
#     device_description = db.Column(db.Integer , nullable=False) #设备型号
#     device_sn = db.Column(db.String(80) , nullable=False) #设备序列号
#     command_port = db.Column(db.Integer) #命令端口
#     http_port = db.Column(db.Boolean) #http端口
#     mac = db.Column(db.Boolean) #mac地址
#     ipv4_address = db.Column(db.Boolean) #ipv4地址
#     ipv4_subnet_mask = db.Column(db.Boolean) #子网掩码
#     ipv4_gateway = db.Column(db.Boolean) #网关地址
#     dhcp = db.Column(db.Boolean) #dhcp协议是否开放
#     analog_channel_num = db.Column(db.Boolean) #模拟通道数
#     digital_channel_num = db.Column(db.Boolean) #数字通道数
#     software_version = db.Column(db.Boolean) #软件版本
#     dsp_version = db.Column(db.Boolean) #dsp版本
#     boot_time = db.Column(db.DateTime,nullable=True) #最后一次启用时间
#     oem_info = db.Column(db.Boolean) #原始设备制造商信息
#     ezviz_code = db.Column(db.Boolean) #萤石代码
#     activated = db.Column(db.Boolean) #是否活动
#     password_reset_ability = db.Column(db.Boolean) #是否允许密码重置
#
#     brand = db.Column(db.String(80) , nullable=False) #品牌
#
#
#
#
#
# #存活IP信息
# class IpInfo(db.Model):
#     __tablename__ = 'ip_info'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     ip = db.Column(db.String(255),nullable=True) #ip地址
#     status = db.Column(db.String(255),nullable=True) #状态
#     type = db.Column(db.String(255),nullable=True) #设备类型（PC，摄像头，路由器，其他）
#
#
# #端口信息
# class PortInfo(db.Model):
#     __tablename__ = 'port_info'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     port = db.Column(db.Integer, nullable=True)  # 端口地址


#平台配置信息
class Config(db.Model):
    __tablename__ = 'config'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    key = db.Column(db.String(255), nullable=True)  # ip地址
    value = db.Column(db.String(255), nullable=True)  # ip地址

#port_list 扫描端口
#thrad_num 线程数



#插件信息
class Plugin(db.Model):
    __tablename__ = 'plugin'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=True)  # 插件名称
    model_name = db.Column(db.String(255), nullable=True)  # 导入插件名称
    type = db.Column(db.String(255), nullable=True)  # 插件类型
    info = db.Column(db.String(255), nullable=True)  # 插件介绍
    brand = db.Column(db.String(255), nullable=True)  # 插件品牌


#扫描批次
class Batch(db.Model):
    __tablename__ = 'batch'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    target = db.Column(db.String(255), nullable=True) #目标
    start_time = db.Column(db.DateTime) #开始时间
    end_time = db.Column(db.DateTime) #结束时间
    total = db.Column(db.Integer,nullable=True) #结果总数
    plugin_parameter = db.Column(db.String(255), nullable=True) #插件参数
    plugins = db.Column(db.String(255), nullable=True) #插件
    progress = db.Column(db.String(255), nullable=True) #进度


#扫描信息
class Info(db.Model):
    __tablename__ = 'info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ip = db.Column(db.String(255), nullable=True)  # ip地址
    info = db.Column(db.UnicodeText, nullable=True)  # 设备返回的信息

    batch_id = db.Column(db.Integer, index=True)
    batch = db.relationship('Batch',
                            primaryjoin=foreign(batch_id) == remote(Batch.id),
                            backref='information', lazy='joined')










