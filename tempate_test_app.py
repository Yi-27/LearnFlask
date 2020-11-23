# 导入能用到的flask的包
from flask import Flask, escape, url_for, request, render_template, Markup, make_response, redirect, abort, jsonify
import settings

app = Flask(__name__)
app.config.from_object(settings)  # 设置当前Flask项目的配置文件
app.secret_key = "321miyao123"  # 可以通过os.urandom(16)生成随机密钥


@app.route("/")  # 默认URL
@app.route("/index")
def index():
    return "hello world!"





if __name__ == "__main__":
    app.run()
    # app.run(ip="127.0.0.1", port=5000, debug=False)  # 自定义IP/端口和debug状态