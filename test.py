from flask import Flask, escape, url_for, request, render_template, Markup
import settings

app = Flask(__name__)  # __name__  表示模块名
print(app.config)  # 项目的默认配置 字典格式
app.config.from_object(settings)
# app.config.from_json()

@app.route("/")  # 路由 URL
def hello_world():  # 视图函数  -> MTV中的view视图 函数
    return "hello world!"

@app.route("/login")
def login():
    return "login"


def index():
    return "这样也可以"

app.add_url_rule("/index", view_func=index)  # view_func指明视图函数

# 路由的变量规则
@app.route("/user/<username>")  # 提取url信息
def show_user_name(username):
    return username

@app.route("/user/<username>/<word>")  # 也可以提两个
def show_user_name2(word, username):
    return username + "" + word

@app.route("/post/<int:post_id>")  # 加上转换器
def show_post_id(post_id):
    print(type(post_id))
    return "%s"%post_id  # 不能直接返回post_id因为直接返回时在返回对象

@app.route("/path/<path:subpath>")
def show_subpath(subpath):
    print(type(subpath))
    return subpath


def test_view_func(name, password):
    return name+password

with app.test_request_context():
    print(url_for('index'))
    print(url_for('login'))
    print(url_for('login', next='/'))
    print(url_for("show_user_name2", word="哈哈哈", username="jiyou"))
    print(url_for("show_user_name2", word="哈哈哈", username="jiyou", other="other"))
    # print(url_for("test_view_func", name="123", password="456"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        return "POST"
    else:
        return "GET"

# url_for('static', filename="style.css")


# 渲染模板
@app.route("/hello/")
@app.route("/hello/<title>")
def hello(title=None):
    h1_str = "<h1>这是个含h1标签的字符串</h1>"
    h2_str = "&lt;h1&gt;这是个含h1标签的字符串&lt;/h1&gt;"
    div = "<div>这 &lt;h1&gt; 是 %s div</div>"
    h1_markup = Markup(div)%h1_str
    print(h1_markup)
    """
    <div>这 &lt;h1&gt; 是 &lt;h1&gt;这是个含h1标签的字符串&lt;/h1&gt; div</div>
    """
    h1_escape = Markup.escape(div)
    print(h1_escape)
    """
    &lt;div&gt;这 &amp;lt;h1&amp;gt; 是 %s div&lt;/div&gt;
    """
    h1_striptags = Markup(div).striptags()
    print(h1_striptags)
    """
    这 <h1> 是 %s div
    """
    return render_template("hello.html", titleValue=title, h1=h2_str)



if __name__ == '__main__':
    app.run()
    # app.run(host="ip", port="端口号", debug=false)  # debug True表示一改动代码就重新部署