# Chern
这个项目是一个非常棒的项目，但是我没有很多时间去推进和维护它

## Introduction
Chern is a program intended to simplify the progress of physics analysis.
It provides the following features:
+ Project management:
+ Work flow:

## 简介
Chern是一个为了简化物理分析而做的项目
它提供了如下的一些特性：
+ 项目管理
+ 工作流

The name of the project is in memory of a Chinese-American mathematica, [Shiing-Shen Chern](documents/SSChern.md)
这个项目的命名是为了几年一位美籍华人数学家，[陈省身](documents/SSChern.md)

### Basic consideration
### 基本想法
这个项目的基本想法的产生是由于我们在数据分析中经常会遇到一些如下的问题：代码重用非常复杂，无法重复之前的实验结果，实验结果的存储不方便等。为了解决这些问题，我们需要引入版本控制和更干净的项目结构，并且希望提供更加方便的编辑方式。

因此，我的整体想法是**将程序与运行位置分开**，每次运行的程序有相应的**版本控制**，每次运行时，使用的数据，程序和参数都被完全的记录下来。

### Tasks and algorithms
The key concept of Chern project are tasks and algorithms.
An analysis is usually divided into many small steps, for instance, one of which might be fit in a specific bin. Many such small steps will use a same program but only different parameters or inputs. We call the steps **"task"** and the programs **"algorithm"**. What you need to do about the analysis is simply to setting parameters and start tasks.

### 任务和算法
Chern的核心概念是task（任务）和algorithm（算法）
一个物理分析通常会划分成非常多的小步骤，比如说，在某个动力学区间中做拟合就是其中的一个步骤。很多这样的小步骤会使用同一个程序，但只是输入文件与参数不同。我们把这些小的步骤称为**"task"**把使用的程序称为**"algorithm"**。你所需要做的事情仅仅是设置参数并开始任务。

You can use the default algorithms, and you can also write algorithms by yourself, a framework for writing algorithm is provided. See Algorithm for details.
你可以使用默认的算法，也可以

## Installation
I don't know either, but you can try this: `git clone https://github.com/zhaomr13/Chern.git`

## Usage

### Configuration
+ `Chern config`: edit the global configuration file for all the projects, the default editor is nano 

### About project management
+ `Chern projects`: list all the current projects
    * `Chern projects config`: config the current project
    * `Chern projects [project]`: change the current project to [project] and jump its root directory, if the [project] doesn't exists, it will 
+ `Chern tasks`:

### 希望实现的操作
+ `Chern config`: 打开整体的配置文件并对配置文件进行编辑
+ `Chern projects`: 列出所有的项目
    * `Chern projects config`: 配置当前的项目
    * `Chern projects [project]`: 把当前的项目改变为 [project] 并且跳到它的根目录下
+ `Chern tasks`:
    * `Chern tasks` 查看目前正在运行的所有task


`Chern` 进入chen的ipython环境
`ls projects` 列出所有的project
`lsp` 列出所有的projects
`cdp` 跳转到某个project并且设置好相关信息
`mkproject` 新建project
`mktask` 新建任务
`mkdata` 新建数据
`mkalgorithm` 新建算法

atask.set_algorithm
atask.link_input
atask.link_output
