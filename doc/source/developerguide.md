# Guide for the developers

Chern软件包里包括bin,Chern,doc,profile,templates,test,tmp几个目录

## bin: 运行文件
+ thischern.sh: 设定环境变量，定义 CHERNSYSROOT, CHERNCONFIGPATH. 并将chern加入到对应的PATH和PYTHONPATH中去，定义Chern, chern和chen命令
+ Chern: 启动Chern命令的基本文件，使用一个start_ipython命令来启动一个ipython，并且指定需要的profile文件。
+ test.py: 现在没什么卵用

## Chern: 主要库文件
+ \_\_init\_\_.py: python package的必须文件其中定义了函数create_object_instance，从一个目录生成一个节点的实例，并且根据这个目录的配置指定实例的类型
+ utils.py: 各个类共用的一些函数，目前有:
    + strip_path_string: 去掉路径后面的/以及前后可能加入的一些空格。
    + ConfigFile类: 用于读写配置文件，配置文件保存在.py文件中
+ VObject.py: 表示抽象的节点的类
    + get_type
    + ls
    + readme

+ VData: data类，前面的V只是为了好看以及防止出现奇怪的命名问题
+ VAlgorithm:
+ VDirectory:
+ VProject:
+ VTask:
+ run_standalone.py: 通过一个参数文件和一个算法文件运行一个python脚本

+ ChernManager.py: 单例类，在启动ipython之后事例化，用来管理project
+ 其他的东西暂时是废弃的，应该是我之前做的一个版本的想法。

