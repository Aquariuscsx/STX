from views import app

app.DEBUG = True

if __name__ == '__main__':
    app.run(threaded=True , port=80, host="127.0.0.1")