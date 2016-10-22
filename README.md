#StockAnalyzer
a stock analyser using docker, kafka, cassandra, redis and node.js 
## Overview of the Project 

![Image of Yaktocat](https://github.com/ZhengKuang/StockAnalyzer/blob/master/images/overview.JPG)

## Environment Setup for Windows
### Docker Toolbox

 - Install

https://github.com/docker/toolbox/releases/download/v1.12.0/DockerToolbox-1.12.0.exe

 - Check

Open your cmd, and input
```sh
docker-machine ls
```
Output:

### Python 2.7.10（Pip automatically included）

 - Install

https://www.python.org/ftp/python/2.7.10/python-2.7.10.msi

 - User guide for env setup for Python

https://www.youtube.com/watch?v=54-wuFsPi0w

 - Check

Open your cmd, and input:
```sh
python --version
python
pip --version
```
Output:
### Java 1.7.0_79

 - Install

http://download.oracle.com/otn-pub/java/jdk/7u79-b15/jdk-7u79-windows-x64.exe?AuthParam=1476862241_a8e4b0626fd8bf2d14e28255593735f2

**Warning: you should install Java in a path that contain no space, otherwise kafak will not run due to the path problem**

 - User guide for env setup for Java

https://guides.github.com/features/mastering-markdown/

 - Check

Open your cmd, and input:
```sh
java -version
java
javac -version
javac
```
Output:
### Scala 

 - Install & Environment setup

http://www.runoob.com/scala/scala-install.html

 - Check

Open your cmd, and input:
```sh
scala -version
```
Output:
### Sbt

 - Install

http://www.scala-sbt.org/0.13/docs/zh-cn/Installing-sbt-on-Windows.html

 - Check

Open your cmd, and input 
```sh
sbt sbtVersion
```
Output:

## Quick Start 

