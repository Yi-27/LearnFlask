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

通常情况下，会把用户认证信息和数据库连接储存到应用环境或者 `flask.g`对象中，并在第一次使用前准备好，然后在断开时删除。假设应用中得到当前用户的代码如下:

```python
def get_user():
    user = getattr(g, 'user', None)
    if user is None:
        user = fetch_current_user_from_database()
        g.user = user
    return user
```

在测试时可以很很方便地重载用户而不用改动代码。可以先像下面这样钩接 [`flask.appcontext_pushed`](https://dormousehole.readthedocs.io/en/latest/api.html#flask.appcontext_pushed) 信号:

```
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

```
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

<details class="changelog"><summary style="cursor: pointer; font-style: italic; margin-bottom: 10px;">Changelog</summary></details>

有时候这种情形是有用的：触发一个常规请求，但是保持环境以便于做一点额外的事 情。在 Flask 0.4 之后可以在 `with` 语句中使用 [`test_client()`](https://dormousehole.readthedocs.io/en/latest/api.html#flask.Flask.test_client) 来实现:

```
app = flask.Flask(__name__)

with app.test_client() as c:
    rv = c.get('/?tequila=42')
    assert request.args['tequila'] == '42'
```

如果你在没有 `with` 的情况下使用 [`test_client()`](https://dormousehole.readthedocs.io/en/latest/api.html#flask.Flask.test_client) ，那么 `assert` 会出错失败。因为无法在请求之外访问 request 。