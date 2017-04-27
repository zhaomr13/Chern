# Chern

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

### Tasks and algorithms
The key concept of Chern project are tasks and algorithms.
An analysis is usually divided into many small steps, for instance, one of which might be fit in a specific bin. Many such small steps will use a same program but only different parameters or inputs. We call the steps **"task"** and the programs **"algorithms"**. What you need to do about the analysis is simply to setting parameters and start tasks.

### 任务和算法
Chern的核心概念是task（任务）和algorithm（算法）
一个物理分析通常会划分成非常多的小步骤，比如说，在某个动力学区间中做拟合就是其中的一个步骤。很多这样的小步骤会使用同一个程序，但只是输入文件与参数不同。我们把这些小的步骤成为

You can use the default algorithms, and you can also write algorithms by yourself, a framework for writing algorithm is provided. See Algorithm for details.

## Installation
I don't know either, but you can try this: `git clone git@github.com:zhaomr13/Chern.git`

## Usage

### Configuration
+ `Chern config`: edit the global configuration file for all the projects, the default editor is nano 

### About project management
+ `Chern projects`: list all the current projects
    * `Chern projects config`: config the current project
    * `Chern projects [project]`: change the current project to [project] and jump its root directory, if the [project] doesn't exists, it will 
+ `Chern tasks`:


