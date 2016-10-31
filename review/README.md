# StockAnalyzer Review

首先是要打开docker-machine
```
docker-machine start bigdata
```
然后windows下面打开命令切换环境
```
FOR /f "tokens=*" %i IN ('docker-machine env --shell cmd bigdata') DO %i
```
---
首先建立kafka的data_producer，从google_finace里面采集股票的信息：
```
python data_producer.py AAPL stock-analyzer 192.168.99.100:9092
```
与此对应的是kafka的docker image如何开放
```
docker run -d -p 9092:9092 -e KAFKA_ADVERTISED_HOST_NAME=192.168.99.100 -e
KAFKA_ADVERTISED_PORT=9092 --name kafka --link zookeeper:zookeeper confluent/kafka
```
从这里我们可以看出，kafka的地址是192.168.99.100：9092的端口，并且用link打开了zookeepr和kafka的端口



-----
然后启动cassandra的data_storage.py,从kafka里面拿取数据并且保存到cassandra里面
```
python data_storage.py stock-analyzer 192.168.99.100:9092 stock stock 192.168.99.100
```
cassandra的启动命令
```
docker run -d -p 7199:7199 -p 9042:9042 -p 9160:9160 -p 7001:7001 --name cassandra
cassandra:3.7
```
这里我们可以看到没有任何关于ip地址的消息，在stock-analyzer的参数为[kafka-topic][kafka-broker][key-space][table][cassandra-broker]



---
然后启动spark，从kafka的stock-analyzer里面拿取数据，并且求每五秒的平均，然后存放到kafka的stock-average-price的topic中
```
spark-submit --jars spark-streaming-kafka-0-8-assembly_2.11-2.0.0.jar stream_process.py 192.168.99.100:9092  stock-analyzer stock-average-price

```
然后启动redis的py文件，从kafka的stock-average-price中拿取数据，存放到redis的stock-price这个channel中

stream_process 的参数 [kakfe-broker][kafka-topic] [kafka-new topic]




------
```
python redis-publisher.py stock-average-price 192.168.99.100:9092 stock-price 192.168.99.100 6379
```
redis-publish的参数 [kafka-new topic] [kafka broker] [redis channel][redis host][redis port]



-------

启动application里面的nodejs模块的index.js，监听redis，consumeredis里面的stock-price这个channel
```
node index.js --port=3000[可有可无] --redis_host=192.168.99.100 --redis_port=6379 --subscribe_channel=stock-price
```
这里就不必说些什么了


-----


