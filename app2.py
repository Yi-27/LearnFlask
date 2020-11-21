from flask import Flask, request, session, redirect, url_for, escape
import os
import settings
app = Flask(__name__)
app.config.from_object(settings)
# 设置Session的密钥
secret_key = os.urandom(16)  # 随机生成一个16位的密钥
# b'\x97\xc8\x7f\xbf\xd1\x95\xf3\xbe<\xe8\x86V\x8a\xe3`\xd2'
print(secret_key)
app.secret_key = secret_key

@app.route("/", methods=["POST", "GET"])
def index():
    # 判断用户名字段可在Session会话内-+++++++
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
    print(escape(ret_html))  # 将html中的标签全部转义，这样输出到页面上会好留标签，<input>，而不是变成一个输入框
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


if __name__ == '__main__':
    app.run()