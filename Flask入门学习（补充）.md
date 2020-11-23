# Jinja2模板

Flask 使用 Jinja2 作为默认模板引擎。完全可以使用其它模板引擎。但是不管使用哪种模板引擎，都必须安装 Jinja2 。因为使用 Jinja2 可以让 Flask 使用更多依赖于这个模板引擎的扩展。



## Jinja设置

在 Flask 中， Jinja2 默认配置如下：

- 当使用 `render_template()` 时，扩展名为 `.html` 、 `.htm` 、 `.xml` 和 `.xhtml` 的模板中开启**自动转义**。
- 当使用 `render_template_string()` 时，字符串开启自动转义。
- 在模板中可以使用 `{% autoescape %}` 来手动设置是否转义。
- Flask 在 Jinja2 环境中加入一些全局函数和辅助对象，以增强模板的功能。

## 标准环境

缺省情况下，以下全局变量可以在 Jinja2 模板中使用：（不需要写flask，直接写后面的即可）

- `config`

    当前配置对象（ `flask.config` ）

- `request`

    当前请求对象（ `flask.request`）。 在没有活动请求环境情况下渲染模板时，这个变量不可用。

- `session`

    当前会话对象（ `flask.session`）。 在没有活动请求环境情况下渲染模板时，这个变量不可用。

- `g`

    请求绑定的全局变量（ `flask.g` ）。 在没有活动请求环境情况下渲染模板时，这个变量不可用。

- `url_for`()

    `flask.url_for()`函数。用于拼接成url

- `get_flashed_messages`()

    `flask.get_flashed_messages()`函数。获得闪现（flash）中存的值。

### Jinja 环境行为

这些添加到环境中的变量不是全局变量。与真正的全局变量不同的是这些变量在 已导入的模板的环境中是不可见的。这样做是基于性能的原因，同时也考虑让代码更有条理。

那么意义何在？假设需要导入一个宏，这个宏需要访问请求对象，那么有两个选择：

1. 显式地把请求或都该请求有用的属性作为参数传递给宏。
2. 导入“ with context ”宏。

导入方式如下：

```
{% from '_helpers.html' import my_macro with context %}
```



## 标准过滤器

在 Flask 中的模板中添加了以下 Jinja2 本身没有的过滤器：

- `tojson`()

    这个函数可以把对象转换为 JSON 格式。如果要动态生成 JavaScript ，那么这个函数非常有用。

    ```html
    <script type=text/javascript>
        doSomethingWith({{ user.username|tojson }});
    </script>
    ```

    在一个 *单引号* HTML 属性中使用 |tojson 的输出也是安全的：

```html
<button onclick='doSomethingWith({{ user.username|tojson }})'>
    Click me
</button>
```

## 控制自动转义

自动转义是指自动对特殊字符进行转义。特殊字符是指 HTML （ 或 XML 和 XHTML ） 中的 `&` 、 `>` 、 `<` 、 `"` 和 `'` 。因为这些特殊字符代表了特殊的意思，所以如果要在文本中使用它们就必须把它们替换为“实体”。如果不转义 ，那么用户就无法使用这些字符，而且还会带来安全问题。（比如：跨站脚本攻击（XSS）

有时候，如需要直接把 HTML 植入页面的时候，可能会需要在模板中关闭自动转义功能。这个可以直接植入的 HTML 一般来自安全的来源，例如一个把标记语言转换为 HTML 的 转换器。

有三种方法可以控制自动转义：

- 在 Python 代码中，可以在把 HTML 字符串传递给模板之前，用 `Markup`对象封装。一般情况下推荐使用这个方法。

- 在模板中，使用 `|safe` 过滤器显式把一个字符串标记为安全的 HTML （例如： `{{ myvariable|safe }}` ）。

- 临时关闭整个系统的自动转义。在模板中关闭自动转义系统可以使用 `{% autoescape %}` 块：
    - ```
        {% autoescape false %}
            <p>autoescaping is disabled here
            <p>{{ will_not_be_escaped }}
        {% endautoescape %}
        ```

    - 在这样做的时候，要非常小心块中的变量的安全性。



## 注册过滤器

有两种方法可以在 Jinja2 中注册自己的过滤器。要么手动把它们放入应用的 `jinja_env`中，要么使用 `template_filter()`装饰器。

下面两个例子功能相同，都是倒序一个对象:

```python
@app.template_filter('reverse')  # 使用装饰器
def reverse_filter(s):
    return s[::-1]

# 手动
def reverse_filter(s):
    return s[::-1]
app.jinja_env.filters['reverse'] = reverse_filter
```

装饰器的参数是可选的，如果不给出就使用函数名作为过滤器名。一旦注册完成后， 就可以在模板中像 Jinja2 的内建过滤器一样使用过滤器了。例如，假设在环境中有一个 名为 mylist 的 Pyhton 列表:

```
{% for x in mylist | reverse %}
{% endfor %}
```



## 环境处理器

环境处理器的作用是把新的变量自动引入模板环境中。环境处理器在模板被渲染前运行，因此可以把新的变量**自动引入模板环境**中。它是一个**函数**，**返回值是一个字典**。 在应用的所有模板中，这个字典将与模板环境合并:

```python
@app.context_processor
def inject_user():
    return dict(user=g.user)
```

上例中的环境处理器创建了一个值为 g.user 的 user 变量，并把这个变量加入了模板环境中。

这个例子只是用于说明工作原理，不是非常有用，因为在模板中， g 总是存在的。

传递值不仅仅局限于变量，还可以传递函数（ Python 提供传递函数的功能）:

```python
@app.context_processor
def utility_processor():
    def format_price(amount, currency=u'€'):
        return u'{0:.2f}{1}'.format(amount, currency)
    return dict(format_price=format_price)
```

上例中的环境处理器把 format_price 函数传递给了所有模板:

```
{{ format_price(0.33) }}  # 这样就可以在模本中执行这个Python函数了
```

还可以把 format_price 创建为一个模板过滤器（参见 注册过滤器），这里只是演示如何在一个环境处理器中传递函数。（就是类似，**{{0.33 | format_price}}**）



# 测试 Flask 应用

未经测试的应用难于改进现有的代码，因此其开发者会越改进越抓狂。 反之，经过自动测试的代码可以安全的改进，并且可以在测试过程中立即发现错误。

Flask 提供的测试渠道是使用 Werkzeug 的 `Client`类， 并处理本地环境。可以结合这个渠道使用自己喜欢的测试工具。

## 测试骨架

首先在应用的根文件夹中添加一个测试文件夹。然后创建一个 Python 文件来储存测试内容（ `test_flaskr.py` ）。名称类似 `test_*.py` 的文件会**被 pytest 自动发现**。

接着，创建一个名为 `client()` 的 pytest 固件 ，用来配置调试应用并初始化一个新的数据库:

```python
import os
import tempfile  # 用于创建临时文件的库

import pytest

from flaskr import flaskr


@pytest.fixture
def client():
    db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
    flaskr.app.config['TESTING'] = True

    with flaskr.app.test_client() as client:
        with flaskr.app.app_context():
            flaskr.init_db()  # 初始化数据库
        yield client

    # 关闭并删除临时文件和数据库连接
    os.close(db_fd)
    os.unlink(flaskr.app.config['DATABASE'])
```

这个客户端固件会被每个独立的测试调用。它提供了一个简单的应用接口，用于向应用发送请求，还可以追踪 cookie 。

在配置中， `TESTING` 配置标志是被激活的。这样在处理请求过程中，错误捕捉被关闭，以利于在测试过程得到更好的错误报告。

因为 SQLite3 是基于文件系统的，所以可以方便地使用 `tempfile`模块创建一个临时数据库并初始化它。 

+ `mkstemp()`函数返回两个东西： 一个低级别的文件句柄和一个随机文件名。
+ 这个文件名后面将作为的数据库名称。 必须把句柄保存到 db_fd 中，以便于以后用 `os.close()`函数来关闭文件。

为了在测试后删除数据库，固件关闭并删除了文件。

如果现在进行测试，那么会输出以下内容:

```
命令行中：pytest

================ test session starts ================
rootdir: ./flask/examples/flaskr, inifile: setup.cfg
collected 0 items

=========== no tests ran in 0.07 seconds ============
```

虽然没有运行任何实际测试，但是已经可以知道 `flaskr` 应用没有语法错误。否则在导入时会引发异常并中断运行。

## 第一个测试

现在开始测试应用的功能。当访问应用的根 URL （ / ）时应该显示 “ No entries here so far ”。在 `test_flaskr.py` 文件中新增一个测试 函数来测试这个功能:

```python
def test_empty_db(client):
    """Start with a blank database."""

    rv = client.get('/')
    assert b'No entries here so far' in rv.data
```

注意，调试的测试函数都是**以 test 开头**的。这样 pytest就会**自动识别**这些是用于测试的函数并运行它们。

通过使用 `client.get` ，可以向应用的指定 URL 发送 HTTP `GET` 请求，其返回的是一个 `response_class`响应对象。可以使用 `data`属性来检查应用的返回值（字节 类型）。在本例中，检查输出是否包含 `'No entries here so far'` 。

再次运行测试，会看到通过了一个测试:

```
命令行： pytest -v

================ test session starts ================
rootdir: ./flask/examples/flaskr, inifile: setup.cfg
collected 1 items

tests/test_flaskr.py::test_empty_db PASSED

============= 1 passed in 0.10 seconds ==============
```



## 登录和注销

应用的主要功能必须登录以后才能使用，因此必须测试应用的登录和注销。

测试的方法是使用规定的数据（用户名和密码）向应用发出登录和注销的请求。因为登录和注销后会重定向到别的页面，因此必须告诉客户端使用` follow_redirects `追踪重定向。

在 `test_flaskr.py` 文件中添加以下两个函数:

```python
def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)
```

现在可以方便地测试登录成功、登录失败和注销功能了。下面为新增的测试函数:

```python
def test_login_logout(client):

    rv = login(client, flaskr.app.config['USERNAME'], flaskr.app.config['PASSWORD'])  # 登录从配置文件中拿到用户名
    assert b'You were logged in' in rv.data

    rv = logout(client)
    assert b'You were logged out' in rv.data

    rv = login(client, flaskr.app.config['USERNAME'] + 'x', flaskr.app.config['PASSWORD'])
    assert b'Invalid username' in rv.data

    rv = login(client, flaskr.app.config['USERNAME'], flaskr.app.config['PASSWORD'] + 'x')
    assert b'Invalid password' in rv.data
```





## 其他测试技巧

除了使用上述测试客户端外，还可以联合 `with` 语句使用 `test_request_context()`方法来**临时**激活一个**请求环境**。在这个环境中可以像在视图函数中一样操作 `request`、 `g`和 `session`对象。示例:

```python
import flask

app = flask.Flask(__name__)

with app.test_request_context('/?name=Peter'):
    assert flask.request.path == '/'
    assert flask.request.args['name'] == 'Peter'
```

所有其他与环境绑定的对象也可以这样使用。

如果要使用不同的配置来测试应用，而且没有什么好的测试方法，那么可以考虑使用应用工厂。

注意，在测试请求环境中 `before_request()`和 `after_request()`不会被自动调用。但是当调试请求环境离开 `with` 块时会执行 `teardown_request()`函数。如果需要 `before_request()`函数和正常情况下一样被调用，那么需要自己调用 `preprocess_request()`

```python
app = flask.Flask(__name__)

with app.test_request_context('/?name=Peter'):
    app.preprocess_request()
    ...
```

在这函数中可以打开数据库连接或者根据应用需要打开其他类似东西。

如果想调用 `after_request()`函数，那么必须调用 `process_response()`，并把响应对象传递给它:

```python
app = flask.Flask(__name__)

with app.test_request_context('/?name=Peter'):
    resp = Response('...')
    resp = app.process_response(resp)
    ...
```

这个例子中的情况基本没有用处，因为在这种情况下可以直接开始使用测试客户端。



## 伪造资源和环境

通常情况下，会把**用户认证信息**和**数据库连接**储存到应用环境或者 `flask.g`对象中，并在第一次使用前准备好，然后在断开时删除。假设应用中得到当前用户的代码如下:

```python
def get_user():
    user = getattr(g, 'user', None)  # 先看看g中有没有user，有就直接返回
    if user is None:
        user = fetch_current_user_from_database() #这是自定义方法，从数据库加载个user
        g.user = user
    return user
```

在测试时可以很很方便地重载用户而不用改动代码。可以先像下面这样钩接 `flask.appcontext_pushed`信号:**（不太懂）**

```python
from contextlib import contextmanager
from flask import appcontext_pushed, g

@contextmanager
def user_set(app, user):
    def handler(sender, **kwargs):
        g.user = user
    with appcontext_pushed.connected_to(handler, app):
        yield
```

然后使用它:

```python
from flask import json, jsonify

@app.route('/users/me')
def users_me():
    return jsonify(username=g.user.username)

with user_set(app, my_user):
    with app.test_client() as c:
        resp = c.get('/users/me')
        data = json.loads(resp.data)
        self.assert_equal(data['username'], my_user.username)
```

## 保持环境

有时候这种情形是有用的：触发一个常规请求，但是保持环境以便于做一点额外的事情。在 Flask 0.4 之后可以在 `with` 语句中使用 `test_client()`来实现:

```python
app = flask.Flask(__name__)

with app.test_client() as c:  # test_client()模拟Flask项目运行环境，c类似于运行的app
    rv = c.get('/?tequila=42')
    assert request.args['tequila'] == '42'
```

如果在没有 `with` 的情况下使用 `test_client()`，那么 `assert` 会出错失败。因为**无法在请求之外**访问 request 。



## 访问和修改会话

有时候在测试客户端中访问和修改会话是非常有用的。通常有两方法。如果想测试会话中的键和值是否正确，可以使用 `flask.session`:

```python
with app.test_client() as c:
    rv = c.get('/')
    assert flask.session['foo'] == 42
```

但是这个方法无法修改会话或在请求发出前访问会话。自 Flask 0.8 开始，提供了 “会话处理”，用于打开测试环境中会话和修改会话。最后会话被保存，准备好被客户端测试。处理后的会话独立于后端实际使用的会话:

```python
with app.test_client() as c:
    with c.session_transaction() as sess:
        sess['a_key'] = 'a value'

    # 会话会被储存起来，并准备供客户端使用
    c.get(...)
```

注意在这种情况下必须使用 `sess` 对象来代替 `flask.session`代理。 `sess` 对象本身可以提供相同的接口。



## 测试 JSON API

Flask 对 JSON 的支持非常好，并且是一个创建 JSON API 的流行选择。使用 JSON 生成请求和在响应中检查 JSON 数据非常方便:

```python
from flask import request, jsonify

@app.route('/api/auth')
def auth():
    json_data = request.get_json()
    email = json_data['email']
    password = json_data['password']
    return jsonify(token=generate_token(email, password))

with app.test_client() as c:
    rv = c.post('/api/auth', json={
        'email': 'flask@example.com', 'password': 'secret'
    })
    json_data = rv.get_json()  # 获取返回的json
    assert verify_token(email, json_data['token'])
```

在测试客户端方法中传递 `json` 参数，设置请求数据为 JSON 序列化对象，并设置内容类型为 `application/json` 。可以使用 `get_json` 从请求或者响应中 获取 JSON 数据。



## 测试 CLI 命令

Click 来自于 测试工具 ，可用于测试 CLI 命令。一个 `CliRunner`**独立运行命令**并通过 `Result`对象捕获输出。

Flask 提供 `test_cli_runner()`来创建一个 `FlaskCliRunner`，以自动传递 Flask 应用给 CLI 。用 它的 `invoke()`方法调用命令，与在**命令行** 中调用一样:

```python
import click

@app.cli.command('hello')
@click.option('--name', default='World')
def hello_command(name)  # 定义一个hello命令，
    click.echo(f'Hello, {name}!')

def test_hello():
    runner = app.test_cli_runner()  # 获得一个test命令行的工作

    # 直接模拟命令行执行命令，用option来执行
    result = runner.invoke(hello_command, ['--name', 'Flask'])
    assert 'Hello, Flask' in result.output

    # 通过命令的名字来执行
    result = runner.invoke(args=['hello'])
    assert 'World' in result.output
```

在上面的例子中，通过**名称引用**命令的好处是可以验证命令是否在应用中已正确注册过。

如果要在不运行命令的情况下测试运行参数解析，可以使用 其 `make_context()`方法。这样有助于测试复杂验证规则和自定义类型:

```python
def upper(ctx, param, value):
    if value is not None:
        return value.upper()

@app.cli.command('hello')
@click.option('--name', default='World', callback=upper)
def hello_command(name)  # 定义命令，回调函数为upper
    click.echo(f'Hello, {name}!')

def test_hello_params():
    # 不运行命令下测试运行参数解析
    context = hello_command.make_context('hello', ['--name', 'flask']) 
    assert context.params['name'] == 'FLASK'
```





# 应用错误处理

应用出错，服务器出错。或早或晚，都会遇到产品出错。即使代码是百分百正确， 还是会时常看见出错。为什么？因为其他相关东西会出错。以下是一些在代码完全正确的条件下服务器出错的情况：

- 客户端已经中断了请求，但应用还在读取数据。
- 数据库已经过载，无法处理查询。
- 文件系统没有空间。
- 硬盘完蛋了。
- 后台服务过载。
- 使用的库出现程序错误。
- 服务器与另一个系统的网络连接出错。

以上只是会遇到的问题的一小部分。那么如何处理这些问题呢？如果应用运行在生产环境下，那么缺省情况下 Flask 会显示一个简单的出错页面，并把出错情况记录到 `logger`。

但可做的还不只这些，下面介绍一些更好的出错处理方法。

## 错误日志工具

当足够多的用户触发了错误时，发送关于出错信息的邮件，即使仅包含严重错误的邮件也会是一场空难。更不用提从来不会去看的日志文件了。 因此，推荐使用 Sentry来处理应用错误。 Sentry 统计重复错误，捕获堆栈数据和本地变量用于排错，并在发生新的或者指定频度的错误时发送电子邮件。

要使用 Sentry 需要安装带有 flask 依赖的 sentry-sdk 客户端:

```
pip install sentry-sdk[flask]
```

把下面内容加入 Flask 应用:

```python
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init('YOUR_DSN_HERE',integrations=[FlaskIntegration()])
```

YOUR_DSN_HERE 需要被替换为在 Sentry 安装时获得的 DSN 值。

安装好以后，内部服务出错信息会自动向 Sentry 报告，你会接收到出错通知。



## 错误处理

当错误发生时，可能想要向用户显示自定义的出错页面。注册出错处理器或以做到这点。

一个出错处理器是一个返回响应的普通视图函数。但是不同之在于它不是用于路由的 ，而是用于一个异常或者当尝试处理请求时抛出 HTTP 状态码。

### 注册

通过使用 `errorhandler()`装饰函数来注册或者稍后使用 `register_error_handler()`来注册。 记得当返回响应的时候设置出错代码:

```python
@app.errorhandler(werkzeug.exceptions.BadRequest)  # 定制出错页面
def handle_bad_request(e):
    return 'bad request!', 400

# 或者不用装饰器也行
app.register_error_handler(400, handle_bad_request)
```

当注册时， `werkzeug.exceptions.HTTPException`的子类，如 `BadRequest`，和它们的 HTTP 代码是可替换的。 （ `BadRequest.code == 400` ）

因为 Werkzeug 无法识别非标准 HTTP 代码（就是类似自己写258，这样的状态码），因此它们不能被注册。替代地，使用适当的代码定义一个 `HTTPException`子类，注册并抛出异常类:

```python
class InsufficientStorage(werkzeug.exceptions.HTTPException):
    code = 507  # 自定义状态码类
    description = 'Not enough storage space.'

# 注册这个自定义状态码的出错处理器
# 就是知道返回什么状态码，知道返回什么描述信息
app.register_error_handler(InsufficientStorage, handle_507)  

raise InsufficientStorage()
```

**出错处理器**可被用于任何异常类的注册，除了 `HTTPException`子类或者 HTTP 状态码。 出错处理器可被用于特定类的注册，也可用于一个父类的所有子类的注册。



### 处理

在处理请求时，当 Flask 捕捉到一个异常时，它首先**根据代码检索**。如果该代码没有注册处理器，它会**根据类的继承来查找**，确定最合适的注册处理器。如果找不到已注册的处理器，那么 `HTTPException`子类会显示 一个**关于代码的通用消息**。没有代码的异常会被转化为一个**通用的 500 内部服务器错误**。

例如，如果一个 `ConnectionRefusedError`的实例被抛出，并且一个出错处理器注册到 `ConnectionError`和 `ConnectionRefusedError`，那么 会使用更合适的 `ConnectionRefusedError`来处理异常实例，生成响应。

当一个蓝图在处理抛出异常的请求时，在蓝图中注册的出错处理器**优先于**在应用中全局注册的出错处理器。但是，蓝图无法处理 404 路由错误，因为 404 发生的路由级别还不能检测到蓝图。

### 通用异常处理器

可以为非常通用的基类注册异常处理器，例如 `HTTPException` 基类或者甚至 `Exception` 基类。但是，请注意，这样会捕捉到超出你预期的异常。

基于 `HTTPException` 的异常处理器对于把缺省的 HTML 出错页面转换为 JSON 非常有用，但是这个处理器会触发不由你直接产生的东西，如路由过程中产生的 404 和 405 错误。请仔细制作你的处理器，确保不会丢失关于 HTTP 错误的信息。

```python
from flask import json
from werkzeug.exceptions import HTTPException

@app.errorhandler(HTTPException)
def handle_exception(e):
    """返回JSON来替换HTML 因为 HTTP 异常."""
    # 获取这个响应
    response = e.get_response()
    # 用JSON替代
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response
```

基于 `Exception` 的异常处理器有助于改变所有异常处理的表现形式，甚至包含未处理的异常。但是，与在 Python 使用 `except Exception:` 类似，这样会捕 获 ***所有*** 未处理的异常，包括所有 HTTP 状态码。因此，在大多数情况下，设定**只针对特定异常的处理器比较安全**。 因为 `HTTPException` 实例是一个合法的 WSGI 响应，可以直接传递该实例。

```python
from werkzeug.exceptions import HTTPException

@app.errorhandler(Exception)
def handle_exception(e):
    # 传递HTTP错误
    if isinstance(e, HTTPException):
        return e

    # 这里处理非HTTP异常
    return render_template("500_generic.html", e=e), 500
```

异常处理器仍然遵循异常烦类的继承层次。如果同时基于 `HTTPException` 和 `Exception` 注册了异常处理器， `Exception` 处理器不会处理 `HTTPException` 子类，因为 `HTTPException` 更有针对性。



### 未处理的异常

当一个异常发生时，如果没有对应的异常处理器，那么就会返回一个 500 内部服务错误。关于此行为的更多内容参见 `flask.Flask.handle_exception()`。

如果针为 `InternalServerError` 注册了异常处理器，那么出现内部服务错误时就会调用这个处理器。自 Flask 1.1.0 开始，总是会传递一个 `InternalServerError` 实例给这个异常处理器，而不是以前的未处理异常。原始的异常可以通过 `e.original_error` 访问。在 Werkzeug 1.0.0 以前，这个属性只有未处理异常有。建议使用 `getattr` 访问这个属性，以保证兼容性。

```python
@app.errorhandler(InternalServerError)
def handle_500(e):
    original = getattr(e, "original_exception", None)

    if original is None:
        # 直接500错误，比如abort(500)时，才会导致original为空
        return render_template("500.html"), 500

    # 已包装的未处理错误
    return render_template("500_unhandled.html", e=original), 500
```



# 排除应用错误

在生产环境中，配置应用时出错？如果可以通过 shell 来访问主机，那么首先请在部署环境中验证是否可以通过 shell 手动运行应用。请确保验证时使用的帐户与配置的相同，这样可以排除用户权限引发的错误。可以在生产服务器上， 使用 Flask 内建的开发服务器，并且设置 debug=True ，这样有助于找到配置问题。但是，请 **只能在可控的情况下临时这样做** ，**绝不能**在生产时使用 debug=True 。



## 使用调试器

为了更深入的挖掘错误，追踪代码的执行， Flask 提供一个开箱即用的调试器（参见调试模式）。如果需要使用其他 Python 调试器，请注意调试器之间的干扰问题。在使用自己的调试器前要做一些参数调整：

- `debug` - 是否开启调试模式并捕捉异常
- `use_debugger` - 是否使用 Flask 内建的调试器
- `use_reloader` - 模块变化后是否重载并派生进程

`debug` 必须设置为 True （即必须捕获异常），另两个随便。

如果正在使用 Aptana 或 Eclipse 排错，那么 `use_debugger` 和 `use_reloader` 都必须设置为 False 。

一个有用的配置模式如下（当然要根据应用调整缩进）:

```
FLASK:
    DEBUG: True
    DEBUG_WITH_APTANA: True
```

然后，在应用入口（ main.py ），修改如下:

```python
if __name__ == "__main__":
    # 允许aptana 捕获异常, set use_debugger=False
    app = create_app(config="config.yaml")

    use_debugger = app.debug and not(app.config.get('DEBUG_WITH_APTANA'))
    app.run(use_debugger=use_debugger, debug=app.debug,
            use_reloader=use_debugger, host='0.0.0.0')
```



# 日志

Flask 使用标准 Python `logging` 。所有与 Flask 相关的消息都用 `app.logger`来记录，其名称与 `app.name`相同。这个日志记录器也可用于自己的的日志记录。

```python
@app.route('/login', methods=['POST'])
def login():
    user = get_user(request.form['username'])

    if user.check_password(request.form['password']):
        login_user(user)
        # 记录日志，表示该用户登录成功
        app.logger.info('%s logged in successfully', user.username)
        return redirect(url_for('index'))
    else:
        # 记录日志，表示该用户登录密码错误
        app.logger.info('%s failed to log in', user.username)
        abort(401)
```

## 基本配置

当想要为项目配置日志时，应当在程序启动时尽早进行配置。 如果晚了，那么 `app.logger`就会成为**缺省记录器**。 如果有可能的话，应当在**创建应用对象之前**配置日志。

这个例子使用 `dictConfig()`来创建一个类似于 Flask 缺省配置的日志记录配置:

```python
from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__)
```

### 缺省配置

如果没有自己配置日志， Flask 会自动添加一个 `StreamHandler` 到 `app.logger`。 在请求过程中，它会写到由 WSGI 服务器指定的，保存在 `environ['wsgi.errors']` 变量中的日志流（通常是 `sys.stderr`） 中。在请求之外，则会记录到 `sys.stderr`。

### 移除缺省配置

如果在操作 `app.logger` 之后配置日志，并且需要 移除缺省的日志记录器，可以导入并移除它:

```
from flask.logging import default_handler

app.logger.removeHandler(default_handler)
```



## 把出错信息通过电子邮件发送给管理者

当产品运行在一个远程服务器上时，可能不会经常查看日志信息。 WSGI 服务器可能会在一个文件中记录日志消息，而只会在当用户告诉你出错的时候才会查看日志文 件。

为了主动发现并修复错误，可以配置一个 `logging.handlers.SMTPHandler`，用于在一般错误或者更高级别错误发生 时发送一封电子邮件:

```python
import logging
from logging.handlers import SMTPHandler

mail_handler = SMTPHandler(
    mailhost='127.0.0.1',
    fromaddr='server-error@example.com',
    toaddrs=['admin@example.com'],
    subject='Application Error'
)
mail_handler.setLevel(logging.ERROR)
mail_handler.setFormatter(logging.Formatter(
    '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
))

if not app.debug:
    app.logger.addHandler(mail_handler)
```

这需要在同一台服务器上拥有一个 SMTP 服务器。

## 注入请求信息

看到更多请求信息，如 IP 地址，有助调试某些错误。可以继承 `logging.Formatter`来注入自己的内容，以显示在日志消息中。然后，可以修改 Flask 缺省的日志记录器、上文所述的电子邮件日志记录器或者其他日志记录器的格式器。:

```python
from flask import has_request_context, request
from flask.logging import default_handler

class RequestFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.remote_addr = request.remote_addr
        else:
            record.url = None
            record.remote_addr = None

        return super().format(record)

formatter = RequestFormatter(
    '[%(asctime)s] %(remote_addr)s requested %(url)s\n'
    '%(levelname)s in %(module)s: %(message)s'
)
default_handler.setFormatter(formatter)
mail_handler.setFormatter(formatter)
```

## 其他库

其他库可能也会产生大量日志，当正好需要查看这些日志。最简单的方法是向根记录器中添加记录器。:

```python
from flask.logging import default_handler

root = logging.getLogger()
root.addHandler(default_handler)
root.addHandler(mail_handler)
```

单独配置每个记录器更好还是只配置一个根记录器更好，取决项目。:

```
for logger in (
    app.logger,
    logging.getLogger('sqlalchemy'),
    logging.getLogger('other_package'),
):
    logger.addHandler(default_handler)
    logger.addHandler(mail_handler)
```

### Werkzeug

Werkzeug 记录基本的请求/响应信息到 `'werkzeug'` 日志记录器。如果根记录器 没有配置，那么 Werkzeug 会向记录器添加一个 `StreamHandler`。

### Flask 扩展

根据情况不同，一个扩展可能会选择记录到 `app.logger`或者其自己的日志记录器。