#StockAnalyzer
a stock analyser using docker, kafka, cassandra, redis and node.js 
## Overview of the Project 

![Image of overview](https://github.com/ZhengKuang/StockAnalyzer/blob/master/images/overview.gif)

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

![Image of docker](https://github.com/ZhengKuang/StockAnalyzer/blob/master/images/docker-machine%20ls.JPG)

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

![Image of python](https://github.com/ZhengKuang/StockAnalyzer/blob/master/images/python.JPG)

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

![Image of Java](https://github.com/ZhengKuang/StockAnalyzer/blob/master/images/Java.JPG)

![Image of Javac](https://github.com/ZhengKuang/StockAnalyzer/blob/master/images/javac.JPG)

### Scala 

 - Install & Environment setup
 
http://scala-lang.org/download/

http://scala-lang.org/download/install.html

 - Check

Open your cmd, and input:
```sh
scala -version
```
Output:

![Image of scala](https://github.com/ZhengKuang/StockAnalyzer/blob/master/images/scala.JPG)

### Sbt

 - Install

http://www.scala-sbt.org/0.13/docs/zh-cn/Installing-sbt-on-Windows.html

 - Check

Open your cmd, and input 
```sh
sbt sbtVersion
```
Output:

![Image of sbt](https://github.com/ZhengKuang/StockAnalyzer/blob/master/images/sbt.JPG)


# Quick Start & StockAnalyzer Review

首先是要打开docker-machine
```
docker-machine start bigdata
```
然后windows下面打开命令切换环境
```
FOR /f "tokens=*" %i IN ('docker-machine env --shell cmd bigdata') DO %i
```

首先建立kafka的data_producer，从google_finace里面采集股票的信息：
```
python data_producer.py AAPL stock-analyzer 192.168.99.100:9092
```
然后启动cassandra的data_storage.py,从kafka里面拿取数据并且保存到cassandra里面
```
python data_storage.py stock-analyzer 192.168.99.100:9092 stock stock 192.168.99.100
```
然后启动spark，从kafka的stock-analyzer里面拿取数据，并且求每五秒的平均，然后存放到kafka的stock-average-price的topic中
```
spark-submit --jars spark-streaming-kafka-0-8-assembly_2.11-2.0.0.jar stream_process.py 192.168.99.100:9092  stock-analyzer stock-average-price
```
然后启动redis的py文件，从kafka的stock-average-price中拿取数据，存放到redis的stock-price这个channel中
```
python redis-publisher.py stock-average-price 192.168.99.100:9092 stock-price 192.168.99.100 6379
```

启动application里面的nodejs模块的index.js，监听redis，consumeredis里面的stock-price这个channel
```
node index.js --port=3000 --redis_host=192.168.99.100 --redis_port=6379 --subscribe_channel=stock-price
```


