# Guide for the developers

Chern软件包里包括bin,Chern,doc,profile,templates,test,tmp几个目录

## bin: 运行文件
+ thischern.sh: 设定环境变量，定义 CHERNSYSROOT, CHERNCONFIGPATH. 并将chern加入到对应的PATH和PYTHONPATH中去，定义Chern, chern和chen命令
+ Chern: 启动Chern命令的基本文件，使用一个start_ipython命令来启动一个ipython，并且指定需要的profile文件。
+ test.py: 现在没什么卵用

## Chern: 主要库文件
+ \_\_init\_\_.py 
