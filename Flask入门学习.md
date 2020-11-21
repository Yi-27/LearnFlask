Flask是一个轻量级的PythonWeb框架，灵活需要自定制。

Tornado能解决c10k的问题。即解决并发问题。

Django是重量级的，



# 虚拟环境

+ pip install virtualenv 
+ 创建虚拟环境
    + 命令：virtualenv + 环境名
    + 当拥有多个Python版本时，可以通过-p参数指定使用Python版本
        + 不指定即为默认版本

+ 进入环境下的Scripts目录下
    + 输入命令执行脚本：activate
+ 接着可以在此虚拟环境下pip安装只属于该虚拟环境的库了

+ 退出虚拟环境
    + 命令：deactivate



可以通过virtualenvwrapper工具来管理虚拟环境

+ pip install virtualenvwrapper-win

+ 创建虚拟环境
    + 输入命令:mkvirtualenv 环境名
    + 与直接用virtualenv创建不同的是，前面那个是在当前文件夹下创建虚拟环境，而这个是统一在当前用户的envs文件夹下创建，并且会自动进入到该虚拟环境下
    + 如果不想在默认地方创建(c:/user/envs)，可以新建个环境变量:WORKON_HOME，然后里面设置默认路径
    + 如果要指定python版本，则输入: mkvirtualenv --python=python路径（到exe文件)环境名
+ 进入虚拟环境
    + 输入命令：workon + 环境名
+ 退出虚拟环境
    + 输入命令：deactivate
+ 删除虚拟环境
    + 输入命令：rmvirtualenv + 环境名
+ 列出虚拟环境
    + 输入命令：svirtualenv
+ 进入到虚拟环境目录
    + 输入命令：cdvirtualenv + 环境名





# Flask入门

## Flask项目结构

+ 项目名
    + static（静态文件文件夹）
    + templates（模板文件文件夹）
    + app.py（启动文件）

web项目

+ MVC模型
    + model：模型
    + view：视图
    + controller：控制器

PythonWeb项目

+ MTV模型
    + model：模型
    + template：模板（HTML）
    + view：视图（起控制作用类似于controller，写Python代码）



**Flask项目默认端口为5000。**



## WSGI

WSGI（Python Web Server Gateway Interface）Python的web服务器网关接口。

是为Python语言定义的**Web服务器**和**Web应用程序**或**框架**之间的一种简单的通用的接口。



Flask实现了这个接口，并且**内置了一个服务器**。也可以自定义服务器。



### app.py

```python
from flask import Flask

app = Flask(__name__)  # __name__  表示模块名
print(app.config)  # 项目的默认配置 字典格式

@app.route("/")  # 路由 URL
def hello_world():  # 视图函数  -> MTV中的view视图 函数
    return "hello world!"

if __name__ == '__main__':
    app.run()
    # app.run(host="ip", port="端口号", debug=false)  
    # debug True表示一改动代码就重新部署，一般用于development环境
    # debug False 为默认，一般用于production环境
```

`Flask(__name__)`第一个参数是应用模块或者包的名称。如果使用一个单一模块（就像本例），那么应当使用 `__name__` ，因为名称会根据这个模块是按应用方式使用还是作为一个模块导入而发生变化（可能是 `__main__`， 也可能是实际导入的名称）。这个参数是必需的，这样 Flask 才能知道在哪里可以找到模板和静态文件等东西。

> `__name__`在当前模块下会返回`__main__`。导入别的模块，如果别的模块有输出`__name__`的话，当前模块看见的输出就是别的模块的模块名（.py文件名）

#### Flask项目配置

**app.config**

```
<Config {'ENV': 'production', 'DEBUG': False, 'TESTING': False, 'PROPAGATE_EXCEPTIONS': None, 'PRESERVE_CONTEXT_ON_EXCEPTION': None, 'SECRET_KEY': None, 'PERMANENT_SESSION_LIFETIME': datetime.timedelta(31), 'USE_X_SENDFILE': False, 'SERVER_NAME': None, 'APPLICATION_ROOT': '/', 'SESSION_COOKIE_NAME': 'session', 'SESSION_COOKIE_DOMAIN': None, 'SESSION_COOKIE_PATH': None, 'SESSION_COOKIE_HTTPONLY': True, 'SESSION_COOKIE_SECURE': False, 'SESSION_COOKIE_SAMESITE': None, 'SESSION_REFRESH_EACH_REQUEST': True, 'MAX_CONTENT_LENGTH': None, 'SEND_FILE_MAX_AGE_DEFAULT': datetime.timedelta(0, 43200), 'TRAP_BAD_REQUEST_ERRORS': None, 'TRAP_HTTP_EXCEPTIONS': False, 'EXPLAIN_TEMPLATE_LOADING': False, 'PREFERRED_URL_SCHEME': 'http', 'JSON_AS_ASCII': True, 'JSON_SORT_KEYS': True, 'JSONIFY_PRETTYPRINT_REGULAR': False, 'JSONIFY_MIMETYPE': 'application/json', 'TEMPLATES_AUTO_RELOAD': None, 'MAX_COOKIE_SIZE': 4093}>
```



一般有程序有三种环境

+ development开发环境
+ testing测试环境
+ production生成环境

可以通过配置文件来设置三种环境对于Flask项目的配置

```python
# settings.py
# 配置文件
ENV = "development"
DEBUG = True
```

然后在app.py中，通过flask的方法直接加载配置文件

```python
from flask import Flask
import settings

app = Flask(__name__)  # __name__  表示模块名
print(app.config)  # 项目的默认配置 字典格式
app.config.from_object(settings)
# app.config.from_json()  # 也可以读取json文件
# app.config.from_pyfile("settings.py")  # 这样也行
```

但是配置文件不能改端口号。



## Flask路由和变量规则

@app.rounte(url)

就是一个装饰器。

**源码:**

```python
def route(self, rule, **options):
    """A decorator that is used to register a view function for a
    given URL rule.  This does the same thing as :meth:`add_url_rule`
    but is intended for decorator usage::

        @app.route('/')
        def index():
            return 'Hello World'

    For more information refer to :ref:`url-route-registrations`.

    :param rule: the URL rule as string
    :param endpoint: the endpoint for the registered URL rule.  Flask
                     itself assumes the name of the view function as
                     endpoint
    :param options: the options to be forwarded to the underlying
                    :class:`~werkzeug.routing.Rule` object.  A change
                    to Werkzeug is handling of method options.  methods
                    is a list of methods this rule should be limited
                    to (``GET``, ``POST`` etc.).  By default a rule
                    just listens for ``GET`` (and implicitly ``HEAD``).
                    Starting with Flask 0.6, ``OPTIONS`` is implicitly
                    added and handled by the standard request handling.
    """

    def decorator(f):
        endpoint = options.pop("endpoint", None)
        self.add_url_rule(rule, endpoint, f, **options)  # 绑定url和视图方法
        return f

    return decorator
```

add_url_rule方法才是真正用来将url（路由规则rule）和视图方法绑定在一起的。

那么这样写也是可以的

```python
def index():
    return "这样也可以"

app.add_url_rule("/index", view_func=index)  # view_func指明视图函数
```



#### 变量规则

```python
# 路由的变量规则
@app.route("/user/<username>")  # 提取url信息
def show_user_name(username):
    return username

@app.route("/user/<username>/<word>")  # 也可以提两个
def show_user_name2(word, username):
    return username + "" + word
```



> AssertionError: View function mapping is overwriting an existing endpoint function: show_user_name
>
> 抛这个异常时表示存在相同的视图函数了

**转换器**

Flask可以将url中的一些信息强转成自己想要的格式

```python
@app.route("/post/<int:post_id>")  # 加上转换器
def show_post_id(post_id):
    print(type(post_id)) <class 'int'>
    return "%s"%post_id  # 不能直接返回post_id因为直接返回是在返回对象

@app.route("/path/<path:subpath>")
def show_subpath(subpath):
    print(type(subpath))  # <class 'str'>
    return subpath
# 访问 http://127.0.0.1:5000/path/abc/abc/def  返回 abc/abc/def
```

转换器类型：

| `string` | （缺省值） 接受任何不包含斜杠的文本 |
| -------- | ----------------------------------- |
| `int`    | 接受正整数                          |
| `float`  | 接受正浮点数                        |
| `path`   | 类似 `string` ，但可以包含斜杠      |
| `uuid`   | 接受 UUID 字符串                    |





## HTTP方法

处理GET和POST请求

```python
from flask import request
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        return "POST"
    else:
        return "GET"
```

使用GET方法， Flask会自动添加**HEAD**方法支持，并按照HTTPRFC来处理HEAD请求。





## 渲染模板

Flask支持**Jinja2**模板引擎

使用 `render_template()` 方法可以渲染模板，要提供模板名称和作为参数传递给模板的变量。

```python
# 渲染模板
@app.route("/hello/")
@app.route("/hello/<title>")
def hello(title=None):
    return render_template("hello.html", title=title)
```

Flask在`templates`目录下找`hello.html`（模板）文件。如果应用是一个模块， 那么模板文件夹应该在模块旁边；如果是一个包，那么就应该在包里面：

**情形 1** : 一个模块:

```
/application.py
/templates
    /hello.html
```

**情形 2** : 一个包:

```
/application
    /__init__.py
    /templates
        /hello.html
```

在模板内部可以和访问 `get_flashed_messages()`函数一样访问 `request` 、 `session` 和 `g`对象。

`g`对象是一个根据需要储存信息的东西。



另外模板可以**继承**，这样就可以把页面的公共部分抽离出来做成一个模板，新页面只要继承这样的模板就行了。比如说导航栏、页脚。侧边栏等等。



**Jinja2模板默认开启自动转义**。即在`{{ 变量 }}`中，变量时通过视图函数的return传过来的键值对中的键，如果其值内包含HTML标签（比如`"<h1>这是个含h1标签的字符串</h1>"`）这样的值放在页面中会自动转义。**即仍旧保留标签，而不是生成h1标题。**

如可以信任某个变量，且知道它是安全的 HTML ，那么可以使用 `Markup`类把它标记为安全的，或者在模板 中使用 `|safe` 过滤器。

```python
from flask import Markup

h1_str = "<h1>这是个含h1标签的字符串</h1>"
div = "<div>这 &lt;h1&gt; 是 %s div</div>"

h1_markup = Markup(div)%h1_str  # h1_str被转义了 div中还是保留标签
print(h1_markup)
"""
<div>这 &lt;h1&gt; 是 &lt;h1&gt;这是个含h1标签的字符串&lt;/h1&gt; div</div>
"""

h1_escape = Markup.escape(div)  # 就是转义标签
print(h1_escape)
"""
&lt;div&gt;这 &amp;lt;h1&amp;gt; 是 %s div&lt;/div&gt;
"""

h1_striptags = Markup(div).striptags()  # 将转义的标签变成带标签的，但是原有的标签
print(h1_striptags)
"""
这 <h1> 是 %s div
"""
```





## 操作请求数据

 Flask 中由全局对象`request`来提供请求信息。

由于是在**本地环境**所以全局对象`request`是**线程安全**的。

某些对象在 Flask 中是全局对象，但不是通常意义下的全局对象。这些对象实际上是 **特定环境下本地对象的代理**。



设想现在处于处理线程的环境中。一个请求进来了，服务器决定生成一个新线程。当 Flask 开始其内部请求处理时会把当前线程作为**活动环境**，并把当前应用和 WSGI 环境绑定到 这个环境（线程）。它以一种聪明的方式使得一个应用可以在不中断的情况下调用另一个 应用。（**不是很理解！！！**）

这个只有在做**单元测试**时才有用。在测试 时会遇到由于没有请求对象而导致依赖于请求的代码会突然崩溃的情况。对策是自己创建 一个请求对象并绑定到环境。最简单的单元测试解决方案是使用 `test_request_context()`环境管理器。通过使用 `with` 语句 可以绑定一个测试请求，以便于交互。

```python
# test_request_context() 环境管理器
# 通过使用 with 语句，可以绑定一个测试请求
with app.test_request_context('/hello', method='POST'):
    # 这里面可以做一些
    assert request.path == "/hello", "路径不是hello"  # 断言不满足条件就会抛异常
    assert request.method == "POST", "不是POST请求"
```

另一种方式是把整个 WSGI 环境传递给`request_context()`方法

```python
from flask import request

with app.request_context(environ):
    assert request.method == 'POST'
```

**这里我不知道environ是哪来的！！！！**



## 请求对象

使用flask中的request模块。

通过使用 `method`属性可以操作当前请求方法，通过使用 `form`属性处理表单数据（在 `POST` 或者 `PUT` 请求 中传输的数据）。

```python
@app.route("/login", methods=["POST", "GET"])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] == "Jiyou" and request.form['password'] == "123":
            return request.form['username']  # 这步其实应该跳转到主页的
        else:
            error = 'Invalid username/password'

    # 访问该页面是GET，直接返回login.html页面，和None
    # 如果用户名密码正确应该跳转到主页
    # 不正确就再次返回login.html页面，然后和Invalid username/password
    return render_template('login.html', error=error)
```

当form中找不到键时会抛BadRequestKeyError异常，但是不会终止程序运行。这时应该给一个友好的异常页面显示。



#### 获取URL中的参数

通过`?key=value`提交的参数可以使用request的args属性来提取。

```python
arg = request.args.get("key", default="hahah")  # default默认为None
print(arg)
```



## 文件上传

Flask 处理文件上传很容易，只要确保在HTML 表单中设置 `enctype="multipart/form-data"` 属性就可以了。否则浏览器将不会传送你的文件。

已上传的文件被储存在内存或文件系统的临时位置。可以通过请求对象 `files` 属性来访问上传的文件。每个上传的文件都储存在这个 字典型属性中。这个属性基本和标准 Python `file` 对象一样，另外多出一个 用于把上传文件保存到服务器的文件系统中的 `save()`方法。

```python
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
        status = "upload OK"
    return render_template("upload.html", status=status)
```

如果想要知道文件上传之前其在客户端系统中的名称，可以使用 `filename`属性。但是要**注意**这个值是 **可以伪造的**，永远不要信任这个值。如果想要把客户端的文件名作为服务器上的文件名， 可以通过 Werkzeug 提供的 `secure_filename()`函数:

```python
# 使用上传文件的名字存储
f1.save('uploadFiles/' + secure_filename(f1.filename))
f2.save('uploadFiles/' + secure_filename(f2.filename))
```

**但是这样文件存储后损坏！！！！**



## Cookies

要访问 cookies ，可以使用 `cookies`属性。可以使用响应对象 的 `set_cookie`方法来设置 cookies 。请求对象的`cookies`属性是一个包含了客户端传输的所有 cookies 的字典。在 Flask 中，如果使用 `Session会话`，就不要直接接使用 cookies ，因为`Session会话`比较安全一些。

```python
@app.route("/cookie", methods=["POST", "GET"])
def cookie():
    # 获取cookie中的属性
    # 这里的cookies是一个字典
    # 用get(key)而不是直接cookies[key]
    username = request.cookies.get("username", default="默认值")  # 也可以设置找不到值时返回的默认值
    print(username)

    # 显式的转换响应对象
    resp = make_response(render_template("upload.html"))
    # 设置cookies在响应对象上
    resp.set_cookie('username', 'the username')  # 在这个响应中添加cookie
    return resp
```

`make_response(render_template("upload.html"))`构建了一个返回upload.html页面的**响应对象**

Flask中**视图函数每次return的都是一个响应对象**，别看有时自己只返回一个字符串，其实它背后都给封装成响应对象了。





## URL构建

url_for()函数用于构建指定视图函数的URL。

该函数**第一个参数为视图函数名**。

可以接收任意个关键字参数对应URL中的变量

使用url_for()函数的目的

+ 相比硬编码URL，这样描述性更好
+ 可以在一个地方改变URL
+ 可以处理特殊字符串的转义和Unicode数据
+ 可以避免相对路径问题，因为这样总是绝对路径



使用test_request_context()方法来测试使用url_for()

```python
with app.test_request_context():
    print(url_for('index'))
    print(url_for('login'))
    print(url_for('login', next='/'))
    print(url_for("show_user_name2", word="哈哈哈", username="jiyou"))
```

结果

```
/index
/login
/login?next=%2F
/user/jiyou/%E5%93%88%E5%93%88%E5%93%88
```

`test_request_context()`告诉 Flask 正在处理一个请求。是在模拟url_for()的工作环境。

> 通过URL可以找到处理函数，那么通过处理函数也可以找到URL。url_for就是为了找到URL的



## 静态文件

```python
url_for('static', filename='style.css')
```

这个静态文件在文件系统中的位置应该是 `static/style.css` 。



## 重定向和错误

使用 `redirect()`函数可以重定向。使用 `abort()`可以 更早退出请求.

```python
@app.route("/redirect", methods=["POST", "GET"])
def redirect_to_login():
    # 看看cookie中有没有username，没有说明没登录，就重定向到登录页面
    if request.cookies.get("username"):
        abort(401)  # 提前中断 401 表示没有权限
        print("这句话没打印出来")
    else:
        # 这里就用到了url_for来构建URL 开头没有 /
        return redirect(url_for("login"))
```

每种出错代码都会对应显示一个黑白的出错页面。使用 `errorhandler()`装饰器可以定制出错页面:

```python
# 定制出错页面
@app.errorhandler(404)
def page_not_found(error):
    # 返回自定义的友好的404页面，并指定状态码404,（默认是200
    return render_template('page404.html'), 404
```

`404`表示页面不存在。只要出现这个问题，都会跳转到`page404.html`页面。



## Flask的响应对象

视图函数的返回值会自动转换为一个响应对象。如果返回值是一个字符串，那么会被转换为一个包含作为响应体的字符串、一个 `200 OK` 状态代码 和一个 *text/html* 类型的响应对象。如果返回值是一个字典，那么会调用 `jsonify()` 来产生一个响应。

**具体规则：**

+ 如果视图返回的是一个响应对象，那么就直接返回它。
    +  比如通过`make_response()`函数提取获得响应对象。
+ 如果返回的是一个字符串，那么根据这个字符串和缺省参数（状态码等）生成一个用于返回的响应对象。
+ 如果返回的是一个字典，那么调用 `jsonify` 创建一个响应对象。
+ 如果返回的是一个元组，那么元组中的项目可以提供额外的信息。元组中必须至少 包含一个项目，且项目应当由 `(response, status)` 、 `(response, headers)` 或者 `(response, status, headers)` 组成。 `status` 的值会重载状态代码， `headers` 是一个由额外头部值组成的列表或字典。

+ 如果以上都不是，那么 Flask 会**假定**返回值是一个有效的 WSGI 应用并把它转换为一个响应对象。

如果想要在视图内部掌控响应对象的结果，那么可以使用 `make_response()`函数。

比如

```python
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
```



### JSON格式的API

传送JSON格式数据的响应很常见。如果从视图 返回一个 `dict` ，那么它会被转换为一个 JSON响应。

```python
# 用户类
class User(object):
    
    def __init__(self, name="纪莜", age=22):
        self.name = name
        self.age = age
        
    def to_dict(self):
        return {
            "name": self.name,
            "age": self.age
        }

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
```

`jsonify`也是构造返回一个包含JSON格式数据的**响应对象**





## Session会话

除了请求对象request之外还有一种称为 `session`的对象，允许你在不同请求 之间储存信息。这个对象相当于用密钥签名加密的 cookie ，即用户可以查看你的 cookie ，但是如果没有密钥就无法修改它。

**使用会话之前必须设置一个密钥。**

```python
from flask import Flask, request, session, redirect, url_for, escape
import os
app = Flask(__name__)

# 设置Session的密钥
secret_key = os.urandom(16)  # 随机生成一个16位的密钥
# b'\x97\xc8\x7f\xbf\xd1\x95\xf3\xbe<\xe8\x86V\x8a\xe3`\xd2'
print(secret_key)
app.secret_key = secret_key

@app.route("/", methods=["POST", "GET"])
def index():
    # 判断用户名字段可在Session会话内
    if "username" in session:
        return "记录用户名：%s" % escape(session.get("username"))
    return "还没有登录！"

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        # 会话中记录这个username
        session["username"] = request.form["username"]
        
        return redirect(url_for("index"))
    
    ret_html = '''
        <form method="post">
            用户名：<input type=text name=username><br/>
            <input type=submit value=Login>
        </form>
    '''
    print(escape(ret_html))  
    # 将html中的标签全部转义，这样输出到页面上会好留标签，<input>，而不是变成一个输入框
    """
    &lt;form method=&#34;post&#34;&gt;
            用户名：&lt;input type=text name=username&gt;&lt;br/&gt;
            &lt;input type=submit value=Login&gt;
        &lt;/form&gt;
    """
    return ret_html  # 这样直接返回，会渲染表单


@app.route("/logout", methods=["POST", "GET"])
def logout():
    session.pop("username", default=None)  # 从会话中删除username，否则啥也不删
    return redirect(url_for("index"))
```

其中`escape()`函数将html中的标签**全部转义**，这样输出到页面上会好留标签，`<input>`，而不是变成一个输入框。

类似于`Markup.escape()`方法，Jinja2模板默认带转义。



**基于 cookie 的会话的说明：** 

+ Flask 会取出会话对象中的值，把值序列化后储存到 cookie 中。
+ 在打开 cookie 的情况下，如果需要查找某个值，但是这个值在请求中没有持续储存的话，那么不会得到一个清晰的出错信息。
+ 请检查页面响应中的 cookie 的大小是否与网络浏览器所支持的大小一致。

除了缺省的客户端会话之外，还有许多 Flask 扩展支持服务端会话。（**缺省不知道啥意思**



## 消息闪现

Flask 通过闪现系统来提供了一个易用的反馈方式。

闪现系统的基本工作原理：

+ 在**请求结束时** 记录一个消息，**提供且只提供给**下一个请求使用。
+ 通常通过一个**布局模板**来展现闪现的 消息。

`flash()`用于闪现一个消息。在模板中，使用 `get_flashed_messages()`来操作消息。



## 日志

有时候可能会遇到数据出错需要纠正的情况。例如因为用户篡改了数据或客户端代码出错 而导致一个客户端代码向服务器发送了明显错误的 HTTP 请求。多数时候在类似情况下 返回 `400 Bad Request` 就没事了，但也有不会返回的时候，而代码还得继续运行 下去。

这时候就需要使用日志来记录这些不正常的东西了。

```python
app.logger.debug('A value for debugging')
app.logger.warning('A warning occurred (%d apples)', 42)
app.logger.error('An error occurred')
```

`logger`是一个标准的 `Logger`Logger 类。



## 集成 WSGI 中间件

如果想要在应用中添加一个 WSGI 中间件，那么可以包装内部的 WSGI 应用。假设为了 解决 lighttpd 的错误，要使用一个来自 Werkzeug 包的中间件，那么可以这样做:

```python
from werkzeug.contrib.fixers import LighttpdCGIRootFix
app.wsgi_app = LighttpdCGIRootFix(app.wsgi_app)
```




