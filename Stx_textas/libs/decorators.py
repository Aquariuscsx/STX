from flask import session,redirect,url_for
from functools import wraps

#登录验证
def login_chick(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if session.get('user')==None:
            return redirect(url_for('_login'))
        else:
            return func(*args,**kwargs)
    return wrapper


#管理员验证
def admin_chick(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if session.get('usertype') == '平台管理员':
            return func(*args,**kwargs)
        else:
            return redirect(url_for('_notFound'))
    return wrapper
