from exts import db
from models import Config


#通用增删改模块
class Manage(object):

    def __init__(self,instance):
        self.instance = instance

    def delete(self):
        db.session.delete(self.instance)
        result = self.commit()
        return result

    def update(self,data,instance=False):
        try:
            for key,value in data.items():
                setattr(self.instance,key,value)
                self.commit()
            if instance:
                return self.instance
            else:
                return 'success'
        except:
            return 'fail'

    def commit(self):
        try:
            db.session.commit()
            return 'success'
        except Exception as e:
            print(e)
            db.session.close()
            return 'fail'



# 通用配置模块
class ConfigManage(object):

    @classmethod
    def update(slc, key, value):
        result = Config.query.filter(Config.key == key).first()
        if not result:
            config = Config()
        else:
            config = result
        config.key = key
        config.value = value
        if not result:
            db.session.add(config)
        try:
            db.session.commit()
        except Exception as e:
            print(e)

    @classmethod
    def search(cls, key):
        config = Config.query.filter(Config.key == key).first()
        if config:
            return config.value
        else:
            return ''



