# How to run the code 
supposed that your kafka is runnning in the docker-machine and the ip is 192.168.99.100, to run the code and submit python code to spark, you should type the following command
```sh
spark-submit --jars spark-streaming-kafka-0-8-assembly_2.11-2.0.0.jar stream-processing.py stock-analyzer average-stock-price 192.168.99.100:9092
```
