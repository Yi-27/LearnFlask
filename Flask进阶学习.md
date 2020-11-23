# 配置管理

应用总是需要一定的配置的。根据应用环境不同，会需要不同的配置。比如**开关调试模式**、**设置密钥**以及其他依赖于环境的东西。

Flask 的设计思路是在**应用开始时载入配置**。可以在代码中直接**硬编码**写入配置， 对于许多小应用来说这不一定是一件坏事，但是还有更好的方法。

不管使用何种方式载入配置，都可以使用 `Flask`对象的 `config`属性来操作配置的值。 Flask 本身就使用这个对象来保存一些配置，扩展也可以使用这个对象保存配置。同时这也是自己保存配置的地方。



## 配置入门

`config`实质上是一个字典的子类，可以像字典一样操作:

```python
app = Flask(__name__)
app.config['TESTING'] = True
```

某些配置值还转移到了 `Flask`对象中，可以直接通过 `Flask`来操作:

```python
app.testing = True
```

一次更新多个配置值可以使用 `dict.update()`方法:

```python
app.config.update(
    TESTING=True,
    SECRET_KEY=b'_5#y2L"F4Q8z\n\xec]/'  # 秘钥
)
```

## 环境和调试特征

`ENV`和 `DEBUG`配置值是特殊的，因为它们如果在应用设置完成之后改变，那么可以会有不同的行为表现。为了更可靠的设置环境和调试， Flask 使用环境变量。

环境用于为 Flask 、扩展和其他程序（如 Sentry ）指明 Flask 运行的情境是什么。 环境由 `FLASK_ENV` 环境变量控制，缺省（default）值为 `production` 。

把 `FLASK_ENV` 设置为 `development` 可以打开**调试模式**。 在调试模式下， `flask run` 会缺省（默认）使用**交互调试器**和**重载器**。如果需要脱离环境，单独控制调试模式，请使用 `FLASK_DEBUG` 标示。

为把 Flask 转换到开发环境并开启调试模式，设置 `FLASK_ENV`:

```
export FLASK_ENV=development
flask run
```

（在 Windows 下，使用 `set` 代替 `export` 。）

推荐使用如上文的方式设置环境变量。虽然可以在配置或者代码中设置环境变量，但是无法及时地被 `flask` 命令读取，一个系统或者扩展就可能会使用自己已定义的环境变量。



## 内置配置变量

以下配置变量由 Flask 内部使用：

#### Flask项目配置

**app.config**

```
<Config {'ENV': 'production', 'DEBUG': False, 'TESTING': False, 'PROPAGATE_EXCEPTIONS': None, 'PRESERVE_CONTEXT_ON_EXCEPTION': None, 'SECRET_KEY': None, 'PERMANENT_SESSION_LIFETIME': datetime.timedelta(31), 'USE_X_SENDFILE': False, 'SERVER_NAME': None, 'APPLICATION_ROOT': '/', 'SESSION_COOKIE_NAME': 'session', 'SESSION_COOKIE_DOMAIN': None, 'SESSION_COOKIE_PATH': None, 'SESSION_COOKIE_HTTPONLY': True, 'SESSION_COOKIE_SECURE': False, 'SESSION_COOKIE_SAMESITE': None, 'SESSION_REFRESH_EACH_REQUEST': True, 'MAX_CONTENT_LENGTH': None, 'SEND_FILE_MAX_AGE_DEFAULT': datetime.timedelta(0, 43200), 'TRAP_BAD_REQUEST_ERRORS': None, 'TRAP_HTTP_EXCEPTIONS': False, 'EXPLAIN_TEMPLATE_LOADING': False, 'PREFERRED_URL_SCHEME': 'http', 'JSON_AS_ASCII': True, 'JSON_SORT_KEYS': True, 'JSONIFY_PRETTYPRINT_REGULAR': False, 'JSONIFY_MIMETYPE': 'application/json', 'TEMPLATES_AUTO_RELOAD': None, 'MAX_COOKIE_SIZE': 4093}>
```

+ `ENV`

    应用运行于什么环境。 Flask 和 扩展可以根据环境不同而行为不同，如打开或关闭调试模式。 `env`属性映射了这个配置键。本变量由 `FLASK_ENV` 环境变量设置。如果本变量是在代码中设置的话，可能出现意外。

    **在生产环境中不要使用 development 。**

    缺省值： `'production'`

+ `DEBUG`

    是否开启调试模式。使用 `flask run` 启动开发服务器时，遇到未能处理的异常时会显示一个**交互调试器**，并且当代码变动后服务器会重启。 `debug`属性映射了这个配置键。当 `ENV`是 `'development'` 时，本变量会启用，并且会被 `FLASK_DEBUG` 环境变量重载。如果本变量是在代码中设置的话，可能会出现意外。

    **在生产环境中不要开启调试模式。**

    缺省值：当 `ENV` 是 `'development'` 时，为 `True` ；否则为 `False` 。

+ `TESTING`

    开启**测试模式**。异常会被**广播**而不是被应用的错误处理器处理。扩展可能也会为了测试方便而改变它们的行为。应当在自己的调试中开启本变量。

    缺省值： `False`

- `PROPAGATE_EXCEPTIONS`

    **异常会重新引发**而不是被应用的错误处理器处理。在没有设置本变量的情况下， 当 `TESTING` 或 `DEBUG` 开启时，本变量**隐式地为真**。

    缺省值： `None`

- `PRESERVE_CONTEXT_ON_EXCEPTION`

    当异常发生时，不要弹出请求情境。在没有设置该变量的情况下，如果 `DEBUG` 为真，则本变量为真。这样允许调试器错误请求数据。本变量通常不需要直接设置。

    缺省值： `None`

- `TRAP_HTTP_EXCEPTIONS`

    如果没有处理 `HTTPException` 类型异常的处理器，重新引发该异常用于被交互调试器处理，而不是作为一个简单的错误响应来返回。

    缺省值： `False`

- `TRAP_BAD_REQUEST_ERRORS`

    尝试操作一个请求字典中不存在的键，如 `args` 和 `form` ，会返回一个 400 Bad Request error 页面。开启本变量，可以把这种错误作为一个未处理的异常处理，这样就可以使用交互调试器了。本变量是一个特殊版本的 `TRAP_HTTP_EXCEPTIONS` 。如果没有设置，本变量会在**调试模式**下开启。

    缺省值： `None`

+ `SECRET_KEY`

    密钥用于会话 cookie 的安全签名，并可用于应用或者扩展的其他安全需求。本变量应当是一个字节型长随机字符串，虽然 unicode 也是可以接受的。例如， 复制如下输出到配置中:

```
$ python -c 'import os; print(os.urandom(16))'
b'_5#y2L"F4Q8z\n\xec]/'
```

​		**当发贴提问或者提交代码时，不要泄露密钥。**

​		缺省值： `None`

- `SESSION_COOKIE_NAME`

    会话 cookie 的名称。假如已存在同名 cookie ，本变量可改变。

    缺省值： `'session'`

- `SESSION_COOKIE_DOMAIN`

    认可会话 cookie 的域的匹配规则。如果本变量没有设置，那么 cookie 会被 `SERVER_NAME`的所有子域认可。如果本变量设置为 `False` ，那么 cookie 域不会被设置。

    缺省值： `None`

- `SESSION_COOKIE_PATH`

    认可会话 cookie 的路径。如果没有设置本变量，那么路径为 `APPLICATION_ROOT` ，如果 `APPLICATION_ROOT` 也没有设置，那么会是 `/` 。

    缺省值： `None`

- `SESSION_COOKIE_HTTPONLY`

    为了安全，浏览器不会允许 JavaScript 操作标记为“ HTTP only ”的 cookie 。

    缺省值： `True`

- `SESSION_COOKIE_SECURE`

    如果 cookie 标记为“ secure ”，那么浏览器只会使用基于 HTTPS 的请求发送 cookie 。应用必须使用 HTTPS 服务来启用本变量。

    缺省值： `False`

- `SESSION_COOKIE_SAMESITE`

    限制来自外部站点的请求如何发送 cookie 。可以被设置为 `'Lax'` （推荐） 或者 `'Strict'` 。

    缺省值： `None`

- `PERMANENT_SESSION_LIFETIME`

    如果 `session.permanent` 为真， cookie 的有效期为本变量设置的数字， 单位为秒。本变量可能是一个 `datetime.timedelta` 或者一个 `int` 。Flask 的缺省 cookie 机制会验证电子签章不老于这个变量的值。

    缺省值： `timedelta(days=31)` （ `2678400` 秒）

- `SESSION_REFRESH_EACH_REQUEST`

    当 `session.permanent` 为真时，控制是否每个响应都发送 cookie 。每次都发送 cookie （缺省情况）可以有效地防止会话过期，但是会使用更多的带宽。 会持续会话不受影响。

    缺省值： `True`

- `USE_X_SENDFILE`

    当使用 Flask 提供文件服务时，设置 `X-Sendfile` 头部。有些网络服务器， 如 Apache ，识别这种头部，以利于更有效地提供数据服务。本变量只有使用这种服务器时才有效。

    缺省值： `False`

- `SEND_FILE_MAX_AGE_DEFAULT`

    当提供文件服务时，设置缓存，控制最长存活期，以秒为单位。可以是一个 `datetime.timedelta`或者一个 `int` 。在一个应用或者蓝图上使用 `get_send_file_max_age()`可以基于单个文件重载本变量。

    缺省值： `timedelta(hours=12)` （ `43200` 秒）

- `SERVER_NAME`

    通知应用其所绑定的主机和端口。子域路由匹配需要本变量。如果配置了本变量， `SESSION_COOKIE_DOMAIN`没有配置，那么本变量会被用于会话 cookie 的域。现代网络浏览器不会允许为没有点的域设置 cookie 。为了使用一个本地域，可以在自己的 `host` 文件中为应用路由添加 任意名称。:`127.0.0.1 localhost.dev `如果这样配置了， `url_for` 可以为应用生成一个单独的外部 URL ，而不是 一个请求情境。

    缺省值： `None`

- `APPLICATION_ROOT`

    通知应用应用的根路径是什么。这个变量用于生成请求环境之外的 URL （请求内的会根据 `SCRIPT_NAME` 生成）。如果 `SESSION_COOKIE_PATH` 没有配置，那么本变量会用于会话 cookie 路径。

    缺省值： `'/'`

- `PREFERRED_URL_SCHEME`

    当不在请求情境内时使用些预案生成外部 URL 。

    缺省值： `'http'`

- `MAX_CONTENT_LENGTH`

    在进来的请求数据中读取的最大字节数。如果本变量没有配置，并且请求没有指定 `CONTENT_LENGTH` ，那么为了安全原因，不会读任何数据。

    缺省值： `None`

- `JSON_AS_ASCII`

    把对象序列化为 ASCII-encoded JSON 。如果禁用，那么 JSON 会被返回为一个 Unicode 字符串或者被 `jsonify` 编码为 `UTF-8` 格式。本变量应当保持启用，因为在模块内把 JSON 渲染到 JavaScript 时会安全一点。

    缺省值： `True`

- `JSON_SORT_KEYS`

    按字母排序 JSON 对象的键。这对于缓存是有用的，因为不管 Python 的哈希种子是什么都能够保证数据以相同的方式序列化。为了以缓存为代价的性能提高可以禁用它，虽然不推荐这样做。

    缺省值： `True`

- `JSONIFY_PRETTYPRINT_REGULAR`

    `jsonify` 响应会输出新行、空格和缩进以便于阅读。在调试模式下总是启用的。

    缺省值： `False`

- `JSONIFY_MIMETYPE`

    `jsonify` 响应的媒体类型。

    缺省值： `'application/json'`

- `TEMPLATES_AUTO_RELOAD`

    当模板改变时重载它们。如果没有配置，在调试模式下会启用。

    缺省值： `None`

- `EXPLAIN_TEMPLATE_LOADING`

    记录模板文件如何载入的调试信息。使用本变量有助于查找为什么模板没有载入或者载入了错误的模板的原因。

    缺省值： `False`

- `MAX_COOKIE_SIZE`

    当 cookie 头部大于本变量配置的字节数时发出警告。缺省值为 `4093` 。 更大的 cookie 会被浏览器悄悄地忽略。本变量设置为 `0` 时关闭警告。



## 使用配置文件

如果把配置放在一个单独的文件中会更有用。理想情况下配置文件应当放在应用包之外。这样可以使用不同的工具进行打包与分发， 而后修改配置文件也没有影响。

因此，常见用法如下:

```python
app = Flask(__name__)
app.config.from_object('yourapplication.default_settings')
app.config.from_envvar('YOURAPPLICATION_SETTINGS')
```

首先从 yourapplication.default_settings 模块载入配置，然后根据 `YOURAPPLICATION_SETTINGS` 环境变量所指向的文件的内容重载配置的值。 在启动服务器前，在 Linux 或 OS X 操作系统中，这个环境变量可以在终端中使用 export 命令来设置:

```
$ export YOURAPPLICATION_SETTINGS=/path/to/settings.cfg
$ python run-app.py
 * Running on http://127.0.0.1:5000/
 * Restarting with reloader...
```

在 Windows 系统中使用内置的 set 来代替:

```
> set YOURAPPLICATION_SETTINGS=\path\to\settings.cfg
```

**配置文件本身实质是 Python 文件（也可以直接导入Python文件）**。只有全部是大写字母的变量才会被配置对象所使用。因此请确保使用大写字母。

一个配置文件的例子:



```
# Example configuration
DEBUG = False
SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]/'
```

请确保尽早载入配置，以便于扩展在启动时可以访问相关配置。除了从文件载入配置外， 配置对象还有其他方法可以载入配置。



## 使用环境变量来配置

除了使用环境变量指向配置文件之外，可能会发现直接从环境中控制配置值很有用 （或必要）。

启动服务器之前，可以在 Linux 或 OS X 上使用 shell 中的export命令设置环境变量:

```
$ export SECRET_KEY='5f352379324c22463451387a0aec5d2f'
$ export MAIL_ENABLED=false
$ python run-app.py
 * Running on http://127.0.0.1:5000/
```

在 Windows 系统中使用内置的 `set` 来代替:

```
> set SECRET_KEY='5f352379324c22463451387a0aec5d2f'
```

尽管这种方法很简单易用，但重要的是**要记住环境变量是字符串**，它们不会自动反序列化为 Python 类型。

以下是使用环境变量的配置文件示例:

```python
import os

_mail_enabled = os.environ.get("MAIL_ENABLED", default="true")
MAIL_ENABLED = _mail_enabled.lower() in {"1", "t", "true"}

SECRET_KEY = os.environ.get("SECRET_KEY")

if not SECRET_KEY:
    raise ValueError("No SECRET_KEY set for Flask application")
```

请注意，除了空字符串之外的任何值都将被解释为 Python 中的布尔值 `True` ， 如果环境显式设置值为 `False` ，则需要注意。

确保尽早加载配置，以便扩展能够在启动时访问配置。除了从文件加载，配置对象还有其他方法可以加载。



## 配置的最佳实践

前面提到的方法的缺点是它使测试更加困难。一般来说，这个问题没有一个 100％ 完美的解决方案，但可以牢记几件事以改善这种体验：

1. 在一个函数中创建你的应用并注册“蓝图”。这样就可以使用不同配置创建多个 实例，极大方便单元测试。可以按需载入配置。
2. 不要编写在导入时就访问配置的代码。如果限制自己只能通过请求访问代码， 那么就可以在以后按需重设配置对象。



## 开发/生产

大多数应用需要一个以上的配置。最起码需要一个配置用于生产服务器，另一个配置用于开发。应对这种情况的最简单的方法总是载入一个缺省（默认）配置，并把这个缺省配置 作为版本控制的一部分。然后，把需要重载的配置，如前文所述，放在一个独立的文件中:

```python
app = Flask(__name__)
app.config.from_object('yourapplication.default_settings')
app.config.from_envvar('YOURAPPLICATION_SETTINGS')
```

然后你只要增加一个独立的 config.py 文件并导出 `YOURAPPLICATION_SETTINGS=/path/to/config.py` 即可。当然还有其他方法可选， 例如可以使用导入或子类。

在 Django 应用中，通常的做法是在文件的开关增加 `from yourapplication.default_settings import *` 进行显式地导入，然后手工重载配置。还可以通过检查一个 `YOURAPPLICATION_MODE` 之类的环境变量（ 变量值设置为 production 或 development 等等）来导入不同的配置文件。



一个有趣的方案是使用类和类的继承来配置:

**configmodule.py**

```python
class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'sqlite:///:memory:'

class ProductionConfig(Config):
    DATABASE_URI = 'mysql://user@localhost/foo'

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
```

如果要使用这样的方案，那么必须使用 `from_object()`:

```python
app.config.from_object('configmodule.ProductionConfig')
```

注意 `from_object()`不会实例化类对象。如果要操作已经实例化的类，比如读取一个属性，那么在调用 `from_object()`之前应当先实例化这个类:

```python
from configmodule import ProductionConfig
app.config.from_object(ProductionConfig())

# 或者, import via string:
from werkzeug.utils import import_string
cfg = import_string('configmodule.ProductionConfig')()
app.config.from_object(cfg)
```

在配置类中，实例化配置对象时允许使用 `@property`

```python
class Config(object):
	"""基础配置, 使用临时数据库服务器."""
    DEBUG = False
    TESTING = False
    DB_SERVER = '192.168.1.56'

    @property
    def DATABASE_URI(self):         # 注意：大写字母
        return 'mysql://user@{}/foo'.format(self.DB_SERVER)

class ProductionConfig(Config):
    """使用生产环境的数据库."""
    DB_SERVER = '192.168.19.32'

class DevelopmentConfig(Config):
    DB_SERVER = 'localhost'
    DEBUG = True

class TestingConfig(Config):
    DB_SERVER = 'localhost'
    DEBUG = True
    DATABASE_URI = 'sqlite:///:memory:'
```

配置的方法多种多样，由自己定度。以下是一些好的建议：

- 在版本控制中保存一个缺省配置。要么在应用中使用这些缺省配置，要么先导入缺省配置然后用自己的配置文件来重载缺省配置。
- 使用一个环境变量来切换不同的配置。这样就可以在 Python 解释器外进行切换， 而根本不用改动代码，使开发和部署更方便，更快捷。如果经常在不同的项目间切换，那么甚至可以创建代码来激活 virtualenv 并导出开发配置。
- 在生产应用中使用` fabric`之类的工具，向服务器分别传送代码和配置。



## 实例文件夹

Flask 0.8 引入了实例文件夹。 Flask 花了很长时间才能够直接使用应用文件夹的 路径（通过 `Flask.root_path` ）。这也是许多开发者载入应用文件夹外的配置的方法。不幸的是这种方法只能用于**应用不是一个包的情况下**，即根路径指向包的内容的情况。

Flask 0.8 引入了一个新的属性： `Flask.instance_path` 。它指向一个新名词：“实例文件夹”。实例文件夹应当处于版本控制中并进行特殊部署。这个文件夹**特别适合存放需要在应用运行中改变的东西或者配置文件**。

可以要么在创建 Flask 应用时显式地提供实例文件夹的路径，要么让 Flask 自动探测实例文件夹。显式定义使用 instance_path 参数:

```python
app = Flask(__name__, instance_path='/path/to/instance/folder')
```

请记住，这里提供的路径 ***必须*** 是绝对路径。**？？？你管这叫绝对路径？？？**



如果 instance_path 参数没有提供，那么会使用以下缺省位置：

- 未安装的模块:

    ```
    /myapp.py
    /instance
    ```

- 未安装的包:

    ```
    /myapp
        /__init__.py
    /instance
    ```

- 已安装的模块或包:

    ```
    $PREFIX/lib/python2.X/site-packages/myapp
    $PREFIX/var/myapp-instance
    ```

    `$PREFIX` 是 Python 安装的前缀。可能是 `/usr` 或你的 virtualenv 的路径。可以通过打印 `sys.prefix` 的值来查看当前的前缀的值。



既然可以通过使用配置对象来**根据关联文件名从文件中载入配置**，那么就可以通过**改变与实例路径相关联的文件名**来按需要载入不同配置。在配置文件中的关联路径的行为可以在 “关联到应用的根路径”（缺省的）和 “关联到实例文件夹”之间变换， 具体通过应用构建函数中的 instance_relative_config 来实现:

```python
app = Flask(__name__, instance_relative_config=True)
```

以下是一个完整的配置 Flask 的例子，从一个模块预先载入配置，然后从实例文件夹中的一个配置文件（如果这个文件存在的话）载入要重载的配置:

```python
app = Flask(__name__, instance_relative_config=True)
app.config.from_object('yourapplication.default_settings')
app.config.from_pyfile('application.cfg', silent=True)
```

通过 `Flask.instance_path` 可以找到实例文件夹的路径。Flask 还提供一 个打开实例文件夹中的文件的快捷方法： `Flask.open_instance_resource()` 。

举例说明:

```python
filename = os.path.join(app.instance_path, 'application.cfg')
with open(filename) as f:
    config = f.read()

# 或者通过open_instance_resource:
with app.open_instance_resource('application.cfg') as f:
    config = f.read()
```



# 信号

Flask 自 0.6 版本开始在内部支持信号。信号功能由优秀的 `blinker`库提供支持， 如果没有安装该库就无法使用信号功能，但不影响其他功能。

什么是信号？当核心框架的其他地方或另一个 Flask 扩展中发生动作时，信号通过发送通知来帮助解耦应用。简言之，信号允许某个发送者通知接收者有事情发生了。

Flask 自身有许多信号，其他扩展可能还会带来更多信号。请记住，信号使用目的是 **通知接收者**，**不应该鼓励**接收者修改数据。你会注意到信号的功能与一些内建的装饰器类似（如 `request_started`与 `before_request()`非常相似），但是它们的工作原理不同。例如 核心的 `before_request()`处理器以一定的顺序执行，并且可以提前退出请求，返回一个响应。相反，所有的信号处理器是乱序执行的，并且不修改任何数据。

信号的最大优势是**可以安全快速的订阅**。比如，在单元测试中这些临时订阅十分有用。 假设想知道请求需要渲染哪个模块，信号可以给答案。



## 订阅信号

使用信号的 `connect()`方法可以订阅该信号。该方法的第一个参数是当信号发出时所调用的函数。第二个参数是可选参数，定义一个发送者。使用 `disconnect()`方法可以退订信号。

所有核心 Flask 信号的发送者是**应用本身**。因此当订阅信号时请指定发送者，除非真的想要收听应用的所有信号。当正在开发一个扩展时，尤其要注意这点。

下面是一个情境管理器的辅助工具，可用于在单元测试中辨别哪个模板被渲染了，哪些变量被传递给了模板:

```python
from flask import template_rendered
from contextlib import contextmanager

@contextmanager  # 情景管理器
def captured_templates(app):
    recorded = []
    def record(sender, template, context, **extra):
        recorded.append((template, context))
    
    # 订阅信号
    template_rendered.connect(record, app)  # record是发送时调用的函数，app是发送者
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)  # 退订信号
```

上例可以在测试客户端中轻松使用:

```python
with captured_templates(app) as templates:
    rv = app.test_client().get('/')
    assert rv.status_code == 200
    assert len(templates) == 1
    template, context = templates[0]
    assert template.name == 'index.html'
    assert len(context['items']) == 10
```

为了使 Flask 在向信号中添加新的参数时不发生错误，请确保使用一个额外的 `**extra` 参数。

在 with 代码块中，所有由 app 渲染的模板会被记录在 templates 变量中。每 当有模板被渲染，模板对象及环境就会追加到变量中。



另外还有一个方便的辅助方法（ `connected_to()`）。 它允许临时把一个使用环境对象的函数订阅到一个信号。因为环境对象的返回值不能被指定，所以必须把列表作为参数:

```python
from flask import template_rendered

def captured_templates(app, recorded, **extra):
    def record(sender, template, context):
        recorded.append((template, context))
    return template_rendered.connected_to(record, app)
```

上例可以这样使用:

```python
templates = []
with captured_templates(app, templates, **extra):
    ...
    template, context = templates[0]
```



## 创建信号

如果相要在自己的应用中使用信号，那么可以直接使用 blinker 库。最常见的,也是最推荐的方法是在自定义的 `Namespace`中命名信号:

```python
from blinker import Namespace
my_signals = Namespace()
```

现在可以像这样创建新的信号:

```python
model_saved = my_signals.signal('model-saved')
```

信号的名称应当是唯一的，并且应当简明以便于调试。可以通过 `name` 属性获得信号的名称。

如果你正在编写一个 Flask 扩展，并且想要妥善处理 blinker 安装缺失的情况， 那么可以使用 `flask.signals.Namespace`类。



## 发送信号

如果想要发送信号，可以使用 `send()`方法。它的第 一个参数是一个发送者，其他参数是要发送给订阅者的东西，其他参数是可选的:

```
class Model(object):
    ...

    def save(self):
        model_saved.send(self)
```

请谨慎选择发送者。如果是一个发送信号的类，请把 self 作为发送者。如果发送信号的是一个随机的函数，那么可以把 `current_app._get_current_object()` 作为发送者。



**传递代理作为发送者**：

不要把 `current_app`作为发送者传递给信号。请使用 `current_app._get_current_object()` 。因为 `current_app`是一个代理，不是实际的应用对象。



## 信号与 Flask 的请求环境

信号在接收时，完全支持 请求情境。在 `request_started`和 `request_finished`本地环境变量 始终可用。因此可以依赖 `flask.g`及其他本地环境变量。 请注意在 发送信号 中所述的限制和 `request_tearing_down`信号。

## 信号订阅装饰器

Blinker 1.1 版本中还可以通过使用新的 `connect_via()` 装饰器轻松订阅信号:

```python
from flask import template_rendered

@template_rendered.connect_via(app)
def when_template_rendered(sender, template, context, **extra):
    print ()'Template %s is rendered with %s' % (template.name, context))
```





# 可插拔视图

Flask 0.7 版本引入了可插拨视图。可插拨视图**基于使用类**来代替函数，其灵感来自于 **Django 的通用视图**。可插拨视图的主要用途是**用可定制的、可插拨的视图**来替代部分实现。



## 基本原理

假设有一个函数用于从数据库中载入一个对象列表并在模板中渲染:

```python
@app.route('/users/')
def show_users(page):
    users = User.query.all()  # 假设从数据库汇总加载一组用户对象
    return render_template('users.html', users=users)
```

上例简单而灵活。但是如果要把这个视图变成一个**可以用于其他模型和模板的通用视图**， 那么这个视图还是不够灵活。因此，就需要引入**可插拨的**、**基于类**的视图。

第一步， 可以把它转换为一个基础视图:

```python
from flask.views import View
class ShowUsers(View):

    def dispatch_request(self):
        users = User.query.all()
        return render_template('users.html', objects=users)

app.add_url_rule('/users/', view_func=ShowUsers.as_view('show_users'))
```

必须做的是创建一个 `flask.views.View`的子类，并且执行 `dispatch_request()`。然后必须通过使用 `as_view()`方法**把类转换为实际视图函数**。传递给函数的字符串是最终视图的名称。但是这本身没有什么帮助，所以要小小地重构一下:



```python
from flask.views import View

# 抽象出来的获取列表的通用视图
class ListView(View):

    def get_template_name(self):
        raise NotImplementedError()  # 如果没重写，就抛异常

    def render_template(self, context):  # 返回渲染的模板
        return render_template(self.get_template_name(), **context)

    def dispatch_request(self):  # 分发请求
        context = {'objects': self.get_objects()}  # 真正获得的列表
        return self.render_template(context)


# 我们真正用到的用户视图
class UserView(ListView):

    def get_template_name(self):
        return 'users.html'

    def get_objects(self):
        return User.query.all()
```

这样做对于示例中的小应用没有什么用途，但是可以足够清楚的解释基本原理。当有一个基础视图类时，问题就来了：类的 `self` 指向什么？

解决之道是：每当请求发出时就创建一个类的新实例，并且根据来自 URL 规则的参数调用 `dispatch_request()`方法。类本身根据参数实例化后传递给 `as_view()`函数。

例如可以这样写一个类:

```python
class RenderTemplateView(View):
    def __init__(self, template_name):
        self.template_name = template_name
    def dispatch_request(self):
        return render_template(self.template_name)
```

然后可以这样注册:

```python
app.add_url_rule('/about', view_func=RenderTemplateView.as_view(
    'about_page', template_name='about.html'))
```

## 方法提示

可插拨视图可以像普通函数一样加入应用。加入的方式有两种，一种是使用 `route()` ，另一种是使用更好的 `add_url_rule()`。在加入的视图中应该提供所使用的 HTTP 方法的名称。提供名称的方法是使用 `methods`属性:

```python
class MyView(View):
    methods = ['GET', 'POST']

    def dispatch_request(self):
        if request.method == 'POST':
            ...
        ...

app.add_url_rule('/myview', view_func=MyView.as_view('myview'))
```

## 基于方法调度

对于 REST 式的 API 来说，为每种 HTTP 方法提供相对应的不同函数显得尤为有用。使用 `flask.views.MethodView`可以轻易做到这点。在这个类中，每个 HTTP 方法 都映射到一个同名函数（**函数名称为小写字母**）:

```python
from flask.views import MethodView

class UserAPI(MethodView):

    def get(self):
        users = User.query.all()
        ...

    def post(self):
        user = User.from_form_data(request.form)
        ...

app.add_url_rule('/users/', view_func=UserAPI.as_view('users'))
```

使用这种方式，不必提供 `methods`属性，它会自动使用相应的类方法。

## 装饰视图

视图函数会被添加到路由系统中，而视图类则不会。因此视图类不需要装饰，只能以手工使用 `as_view()`来装饰返回值:

```python
def user_required(f):
    """检测用户是否登录 没登录则返回401"""
    def decorator(*args, **kwargs):  # 装饰器
        if not g.user:
            abort(401)
        return f(*args, **kwargs)
    return decorator

view = user_required(UserAPI.as_view('users'))
app.add_url_rule('/users/', view_func=view)
```

自 Flask 0.8 版本开始，新加了一种选择：在视图类中定义装饰的列表:

```python
class UserAPI(MethodView):
    decorators = [user_required]
```

请牢记：因为从调用者的角度来看，类的 self 被隐藏了，所以**不能在类的方法上单独使用装饰器**。



## 用于 API 的方法视图

网络 API 经常直接对应 HTTP 变量，因此很有必要实现基于 `MethodView`的 API 。即多数时候， API 需要把不同的 URL 规则应用到同一个方法视图。例如，假设需要这样使用一个 user 对象：

| URL       | 方法     | 说明                       |
| --------- | -------- | -------------------------- |
| `/users/` | `GET`    | 给出一个包含所有用户的列表 |
| `/users/` | `POST`   | 创建一个新用户             |
| `/users/` | `GET`    | 显示一个用户               |
| `/users/` | `PUT`    | 更新一个用户               |
| `/users/` | `DELETE` | 删除一个用户               |

那么如何使用 `MethodView`来实现呢？方法是使用多个规则对应到同一个视图。

假设视图是这样的:

```python
class UserAPI(MethodView):

    # get方法
    def get(self, user_id):
        if user_id is None:
            # 返回一个包含所有用户的列表
            pass
        else:
            # 显示一个用户
            pass
        
	# post方法
    def post(self):
        # 创建一个新用户
        pass

    # delete方法
    def delete(self, user_id):
        # 删除一个用户
        pass
	
    # put方法
    def put(self, user_id):
        # update a single user
        pass
```

那么如何把这个视图挂接到路由系统呢？方法是**增加两个规则并为每个规则显式声明方法**:

```python
user_view = UserAPI.as_view('user_api')
app.add_url_rule('/users/', defaults={'user_id': None},
                 view_func=user_view, methods=['GET',])
app.add_url_rule('/users/', view_func=user_view, methods=['POST',])
app.add_url_rule('/users/<int:user_id>', view_func=user_view,
                 methods=['GET', 'PUT', 'DELETE'])
```

如果你有许多类似的 API ，那么可以代码如下:

```python
def register_api(view, endpoint, url, pk='id', pk_type='int'):
    # 表示用endpoint对应的视图函数作为视图处理函数
    # 但是这里就只是个名字
    # 真正用来作为视图处理函数的是view，是一个方法视图
    view_func = view.as_view(endpoint) 
    app.add_url_rule(url, defaults={pk: None},
                     view_func=view_func, methods=['GET',])
    app.add_url_rule(url, view_func=view_func, methods=['POST',])
    app.add_url_rule('%s<%s:%s>' % (url, pk_type, pk), view_func=view_func,
                     methods=['GET', 'PUT', 'DELETE'])

register_api(UserAPI, 'user_api', '/users/', pk='user_id')
```

> endpoint其实就是视图函数的名称。





# 应用情境

应用情境在**请求**， **CLI 命令**或**其他活动期间**跟踪**应用级**数据。不是将应用程序传递给每个函数，而是代之以访问 `current_app` 和 `g`代理。

这与**请求情境**类似，它在请求期间跟踪请求级数据。推送请求情境时会推送相应的应用情境。

## 情境的目的

`Flask`应用对象具有诸如 `config`之类的属性，这些属性对于在视图和 CLI commands中访问很有用。但是，在项目中的模块内导入 `app` 实例容易导致循环导入问题。当使用 应用程序工厂方案 或编写可重用的 blueprints 或 extensions 时，根本不会有应用程序实例导入。

- Flask 通过 *应用情境* 解决了这个问题。不是直接引用一个 `app` ，而是使用

    `current_app`代理，该代理指向处理当前活动的应用。

处理请求时， Flask 自动 *推送* 应用情境。在请求期间运行的视图函数、错误处理器和其他函数将有权访问 `current_app`。

运行使用 `@app.cli.command()` 注册到 `Flask.cli` 的 CLI 命令时， Flask 还会自动推送应用情境。

## 情境的生命周期

应用情境根据需要创建和销毁。当 Flask 应用开始处理请求时，它会推送`应用情境` 和 `请求情境`。当请求结束时，它会在请求情境中弹出，然后在应用情境中弹出。通常，应用情境将具有与请求相同的生命周期。



## 手动推送情境

如果尝试在应用情境之外访问`current_app`，或其他任何使用它的东西， 则会看到以下错误消息：

```
RuntimeError: Working outside of application context.

这通常意味着正试图使用功能需要以某种方式与当前的应用程序对象进行交互。
要解决这个问题，请使用 app.app_context（）设置应用情境。
```

如果在配置应用时发现错误（例如初始化扩展时），那么可以手动推送上下文。因为可以直接访问 `app` 。在 `with` 块中使用 `app_context()`， 块中运行的所有内容都可以访问 `current_app`。:

```python
def create_app():
    app = Flask(__name__)

    with app.app_context(): # 获取应用上下文情景
        init_db()

    return app
```

如果在代码中的其他地方看到与配置应用无关的错误，则很可能表明应该将该代码移到视图函数或 CLI 命令中。

## 存储数据

应用情境是在请求或 CLI 命令期间存储公共数据的好地方。Flask 为此提供了 `g 对象` 。它是一个简单的命名空间对象，与应用情境具有相同的生命周期。

# 应用情境

应用情境在请求， CLI 命令或其他活动期间跟踪应用级数据。不是将应用程序传递 给每个函数，而是代之以访问 `current_app` 和 `g`代理。

这与 **请求情境**类似，它在请求期间跟踪请求级数据。推送请求情境时会 推送相应的应用情境。

## 情境的目的

`Flask`应用对象具有诸如 `config`之类的属性，这些属 性对于在视图和 CLI commands中访问很有用。但是，在项目中的模 块内导入 `app` 实例容易导致循环导入问题。当使用应用程序工厂方案或编写可重用的 blueprints 或 extensions时，根 本不会有应用程序实例导入。

- Flask 通过 *应用情境* 解决了这个问题。不是直接引用一个 `app` ，而是使用

    `current_app`代理，该代理指向处理当前活动的应用。

处理请求时， Flask 自动 *推送* 应用情境。在请求期间运行的视图函数、错误处 理器和其他函数将有权访问 `current_app`。

运行使用 `@app.cli.command()` 注册到 `Flask.cli` 的 CLI 命令时， Flask 还会自动推送应用情境。

## 情境的生命周期

应用情境根据需要创建和销毁。当 Flask 应用开始处理请求时，它会推送**应用情境** 和 **请求情境**。当请求结束时，它会在请求情境中弹出，然后在应用情境中弹出。通常，应用情境将具有与请求相同的生命周期。



## 手动推送情境

如果尝试在应用情境之外访问 `current_app`，或其他任何使用它的东西， 则会看到以下错误消息：

```
RuntimeError: Working outside of application context.

这通常意味着正在试图使用功能需要以某种方式与当前的应用程序对象进行交互。
要解决这个问题，请使用 app.app_context（）设置应用情境。
```

如果在配置应用时发现错误（例如初始化扩展时），那么可以手动推送上下文。因为可以直接访问 `app` 。在 `with` 块中使用 `app_context()`， 块中运行的所有内容都可以访问 `current_app`。:

```python
def create_app():
    app = Flask(__name__)

    with app.app_context():
        init_db()

    return app
```

如果在代码中的其他地方看到与配置应用无关的错误，则很可能表明应该将该代码移到视图函数或 CLI 命令中。

## 存储数据

应用情境是在请求或 CLI 命令期间存储公共数据的好地方。Flask 为此提供了 `g 对象`。它是一个简单的命名空间对象，与应用情境具有相同的生命 周期。

**Note：**

`g` 表示“全局”的意思，但是指的是数据在 *情境* 之中是全局的。 `g` 中的数据**在情境结束后丢失**，因此它不是在请求之间存储数据的恰当位置。使用`session`或数据库跨请求存储数据。

`g`的常见用法是在**请求期间**管理资源。

1. `get_X()` 创建资源 `X` （如果它不存在），将其缓存为 `g.X` 。
2. `teardown_X()` 关闭或以其他方式解除分配资源（如果存在）。它被注册为 `teardown_appcontext()`处理器。

例如，可以使用以下方案管理数据库连接:

```python
from flask import g

def get_db():
    if 'db' not in g:
        g.db = connect_to_database()

    return g.db

@app.teardown_appcontext  # 关闭或以其他方式解除分配资源
def teardown_db():
    db = g.pop('db', None)

    if db is not None:
        db.close()
```

在一个请求中，每次调用 `get_db()` 会返回同一个连接，并且会在请求结束时自动关闭连接。

可以使用`LocalProxy`基于 `get_db()` 生成一个新的本地情境:

```python
from werkzeug.local import LocalProxy
db = LocalProxy(get_db)
```

访问 `db` 就会内部调用 `get_db` ，与`current_app`的工作方式相同。

------

如果正在编写扩展， `g`应该保留给用户。可以将内部数据存储在情境本身中，但一定要使用足够唯一的名称。当前上下文使用`_app_ctx_stack.top`访问。

## 事件和信号

当应用情境被弹出时，应用将调用使用 `teardown_appcontext()`注册的函数。

如果 `signals_available`为真，则发送以下信号： `appcontext_pushed`、 `appcontext_tearing_down`和`appcontext_popped`。







# 请求情境

请求情境**在请求期间**跟踪**请求级**数据。不是将请求对象传递给请求期间运行的每个函数，而是访问 `request`和 `session`代理。

这类似于 **应用情境**，它跟踪独立于请求的应用级数据。推送请求情境时会推送相应的应用情境。

## 情境的用途

当 `Flask`应用处理请求时，它会根据从 WSGI 服务器收到的环境创建一个`Request`对象。因为 *工作者* （取决于服务器的线程，进程或协程）一 次只能处理一个请求，所以在该请求期间请求数据可被认为是该工作者的全局数据。 Flask 对此使用术语 *本地情境* 。

处理请求时， Flask 自动 *推送* 请求情境。在请求期间运行的视图函数，错误处理器和其他函数将有权访问`request`代理，该请求代理指向当前请求的请求对象。

## 情境的生命周期

当 Flask 应用**开始处理请求时**，它会推送**请求情境**，这也会推送 **应用情境**。当请求结束时，它会弹出请求情境，然后弹出应用程序情境。

情境对于每个线程（或其他工作者类型）是**唯一**的。 `request`不能传递给另一个线程，另一个线程将拥有不同的情境堆栈，并且不会知道父线程指向的请求。

本地情境在 Werkzeug 中实现。

## 手动推送情境

如果尝试在请求情境之外访问 `request`或任何使用它的东西，那么会收到 这个错误消息：

```
RuntimeError: Working outside of request context.

这通常表示正在试图使用功能需要一个活动的 HTTP 请求。
有关如何避免此问题的信息，请参阅测试文档
```

通常只有在测试代码期望活动请求时才会发生这种情况。一种选择是使用`测试客户端`来模拟完整的请求。或者，可以在 `with` 块中使用`test_request_context()`，块中运行的所有内容 都可以访问请求，并填充测试数据。:

```python
def generate_report(year):
    format = request.args.get('format')
    ...

with app.test_request_context(
        '/make_report/2017', data={'format': 'short'}):
    generate_report()
```

如果在代码中的其他地方看到与测试无关的错误，则说明可能应该将该代码移到 视图函数中。



## 情境如何工作

处理每个请求时都会调用`Flask.wsgi_app()`方法。它在请求期间管理情境。 在**内部，请求和应用程序情境实质**是 `_request_ctx_stack`和`_app_ctx_stack`堆栈。当情境被压入堆栈时，依赖它们的代理可用并指向堆栈顶部情境中的信息。

当请求开始时，将创建并推送`RequestContext`，如果该应用程序的情境尚不是顶级情境，则该请求会首先创建并推送 `AppContext`。在推送这些情境时， `current_app`、 `g`、 `request`和 `session`代理可用于处理请求的原始线程。

由于**情境是堆栈**，因此在请求期间可能会压入其他情境导致代理变更。虽然这不是一 种常见模式，但它可以在高级应用使用。比如，执行内部重定向或将不同应用程序链接在一起。

在分派请求并生成和发送响应之后，会弹出请求情境，然后弹出应用情境。在紧临弹出之前，会执行 `teardown_request()`和 `teardown_appcontext()`函数。即使在调度期间发生未处理的异常， 也会执行这些函数。



## 回调和错误

Flask 会在多个阶段调度请求，这会影响请求，响应以及如何处理错误。情境在所有这些阶段都处于活动状态。

`Blueprint`可以为该蓝图的事件添加处理器，处理器会在蓝图与请求路由匹配的情况下运行。

1. 在每次请求之前， `before_request()`函数都会被调用。如果其中一个函数返回了一个值，则其他函数将被跳过。返回值被视为响应，并且视图函数不会被调用。
2. 如果`before_request()`函数没有返回响应，则调用匹配路由的 视图函数并**返回响应**。
3. 视图的返回值被转换为实际的**响应对象**并传递给`after_request()`函数。每个函数都返回一个**修改过的或新的响应对象**。
4. 返回响应后，将弹出情境，该情境调用 `teardown_request()`和 `teardown_appcontext()`函数。即使在上面任何一处引发了未处 理的异常，也会调用这些函数。

如果在拆卸函数之前引发了异常， Flask 会尝试将它与 `errorhandler()`函数进行匹配，以处理异常并返回响应。如果找不到错误处理器，或者处理器本身引发异常， Flask 将返回一个通用的 `500 Internal Server Error` 响应。拆卸函数仍然被调用，并传递异常对象。

如果开启了调试模式，则未处理的异常不会转换为 `500` 响应，而是会传播到 WSGI 服务器。这允许开发服务器向交互式调试器提供回溯。

### 拆解回调

拆除回调与请求派发无关，而在情境弹出时由情境调用。即使在调度过程中出现未处理的异常，以及手动推送的情境，也会调用这些函数。这意味着不能保证请求调度的任何其他部分都先运行。 一定要以不依赖其他回调的方式编写这些函数，并且不会失败。

在测试期间，推迟请求结束后弹出情境会很有用，这样可以在测试函数中访问它们的数据。在 `with` 块中使用 `test_client()`来保存情境，直到 with 块结束。

```python
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def hello():
    print('during view')
    return 'Hello, World!'

@app.teardown_request  # 拆卸请求情境
def show_teardown(exception):
    print('after with block')

with app.test_request_context():  # 得到测试用的请求情境
    print('during with block')

# 在with代码块结束后，调用拆卸方法

with app.test_client() as client:  # 获得测试客户端
    client.get('/')
    # 在这里请求结束，请求情境也不会从弹出去，
    print(request.path)  # 所以才能访问请求中的参数

# with代码块结束后执行情境的拆卸函数
# 测试客户端也已经被关闭
```

### 信号

如果 `signals_available`为真，那么会发送以下信号：

1. `request_started`发送于 `before_request()`函数被调用之前。
2. `request_finished`发送于 `after_request()`函数被调用之后。
3. `got_request_exception`发送于异常开始处理的时候 但早于 an `errorhandler()`被找到或者调用的时候。
4. `request_tearing_down`发送于 `teardown_request()`函数被调用之后。

我有点领悟信号的作用了！

## 出错情境保存

在请求结束时，会弹出请求情境，并且与其关联的所有数据都将被销毁。如果在开发过程中发生错误，延迟销毁数据以进行调试是有用的。

当开发服务器以开发模式运行时（ `FLASK_ENV` 环境变量设置为 `'development'` ），错误和数据将被保留并显示在交互式调试器中。

该行为可以通过`PRESERVE_CONTEXT_ON_EXCEPTION`配置进行控制。如前文所述，它在开发环境中默认为 `True` 。

不要在生产环境中启用`PRESERVE_CONTEXT_ON_EXCEPTION`，因为它会导致应用在发生异常时泄漏内存。



## 关于代理的说明

Flask 提供的一些对象是其他对象的代理。每个工作线程都能以相同的方式访问代理，但是在后台每个工作线程绑定了唯一对象。

多数情况下，不必关心这个问题。但是也有例外，在下列情况有下，知道对象是一个代理对象是有好处的：

- 代理对象不能将它们的类型伪装为实际的对象类型。如果要执行实例检查，则必须检查被代理的原始对象。
- 对象引用非常重要的情况，例如发送 **信号**或将**数据**传递给后台线程。

如果需要访问被代理的源对象，请使用`_get_current_object()`方法:

```python
app = current_app._get_current_object()
my_signal.send(app)  # 发送信号给它
```