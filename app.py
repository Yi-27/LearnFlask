from flask import Flask, escape, url_for, request, render_template, Markup, make_response, redirect, abort, jsonify
import settings
from werkzeug.utils import secure_filename
from bean.User import *

app = Flask(__name__)  # __name__  表示模块名
app.config.from_object(settings)

@app.route("/")  # 路由 URL
def hello_world():  # 视图函数  -> MTV中的view视图 函数
    print("hello world！")
    return "hello world!"



# test_request_context() 环境管理器
# 通过使用 with 语句，可以绑定一个测试请求
with app.test_request_context('/hello', method='POST'):
    # 这里面可以做一些
    assert request.path == "/hello", "路径不是hello"  # 断言不满足条件就会抛异常
    assert request.method == "POST", "不是POST请求"

    
@app.route("/login", methods=["POST", "GET"])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] == "Jiyou" and request.form['password'] == "123":
            return request.form['username']  # 这步其实应该跳转到主页的
        else:
            error = 'Invalid username/password'

    arg = request.args.get("key", default="hahah")
    print(arg)

    # 访问该页面是GET，直接返回login.html页面，和None
    # 如果用户名密码正确应该跳转到主页
    # 不正确就再次返回login.html页面，然后和Invalid username/password
    return render_template('login.html', error=error)



# @app.route("/upload", methods=["GET, POST"])  GET放前面会 405
@app.route("/upload", methods=["POST", "GET"])
def upload():
    status = "wait"
    if request.method == 'POST':
        f1 = request.files['file1']
        f2 = request.files['file2']
        print(request.files)
        print(type(f1))
        """
        ImmutableMultiDict([('file1', <FileStorage: 'gakki_waifu2x_art_noise2_scale_tta_1.png' ('image/png')>), ('file2', <FileStorage: 'gakki2_waifu2x_art_noise2_scale_tta_1.png' ('image/png')>)])
        <class 'werkzeug.datastructures.FileStorage'>
        """
        
        # save方法可以将上传的文件存储到服务器目录下
        f1.save('uploadFiles/gakki1.png')  # 这里注意不要 / 开头
        f2.save('uploadFiles/gakki2.png')  # 因为Flask默认有一个 /

        # 使用上传文件的名字存储  但是这样文件存储后损坏
        f1.save('uploadFiles/' + secure_filename(f1.filename)[:-4] + ".png")
        f2.save('uploadFiles/' + secure_filename(f2.filename)[:-4] + ".png")
        
        status = "upload OK"
    return render_template("upload.html", status=status)


@app.route("/cookie", methods=["POST", "GET"])
def cookie():
    # 获取cookie中的属性
    # 这里的cookies是一个字典
    # 用get(key)而不是直接cookies[key]
    username = request.cookies.get("username", default="默认值")  # 也可以设置找不到值时返回的默认值
    print(username)

    # 显式的转换响应对象
    resp = make_response(render_template("upload.html"))
    # 设置cookies
    resp.set_cookie('username', 'the username')  # 在这个响应中添加cookie
    return resp


@app.route("/redirect", methods=["POST", "GET"])
def redirect_to_login():
    # 看看cookie中有没有username，没有说明没登录，就重定向到登录页面
    if request.cookies.get("username"):
        abort(401)  # 提前中断 401 表示没有权限
        print("这句话没打印出来")
    else:
        # 这里就用到了url_for来构建URL 开头没有 /
        return redirect(url_for("login"))


# 定制出错页面
@app.errorhandler(404)
def page_not_found(error):
    # 返回自定义的友好的404页面，并指定状态码404,（默认是200
    
    resp = make_response(render_template('page404.html'), 404)
    print(type(resp))  # <class 'flask.wrappers.Response'>
    # 可以给响应对象添加响应头
    resp.headers['MyKey'] = "MyValue"  # 自定义的头信息
    
    # 可以添加cookies
    resp.set_cookie("cookieKey", "cookieValue")
    resp.set_cookie("cookieKey2", "cookieValue2")
    
    # 将最中的响应返回出去
    return resp


@app.route("/json", methods=["POST", "GET"])
def ret_json():
    return {
        "username": "Jiyou",
        "theme": "black",
        "age": 20
    }

@app.route("/users", methods=["POST", "GET"])
def users():
    users = [User("gakki", 32), User("shiyuan", 35), User()]
    user_list = [user.to_dict() for user in users]
    print(user_list)
    # [{'name': 'gakki', 'age': 32}, {'name': 'shiyuan', 'age': 35}, {'name': '纪莜', 'age': 22}]
    user_json = jsonify(user_list)
    print(user_json)  #     <Response 149 bytes [200 OK]>
    print(type(user_json))  # <class 'flask.wrappers.Response'>
    return jsonify(user_list)  # 会自动将字典和列表转换成JSON字符串

if __name__ == '__main__':
    app.run()