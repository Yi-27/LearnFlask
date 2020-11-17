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

