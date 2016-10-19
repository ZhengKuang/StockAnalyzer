#coding=utf-8

# - read from kafka
# = do average 
# - save data back

import logging 
import time
import sys
import json

from pyspark import SparkContext
from pyspark.streaming import StreamingContext    
from kafka import KafkaProducer
from kafka.errors import KafkaError
from pyspark.streaming.kafka import KafkaUtils



logger_format='%(asctime)-15s %(message)s'
logging.basicConfig(format=logger_format)
logger=logging.getLogger('data_producer')
logger.setLevel(logging.DEBUG)


kafka_broker='192.168.99.100:9092'
kafka_topic='stock-analyzer'
new_topic='test'



def process(timeobj,rdd):
	# - do something
	number_of_records=rdd.count()
	#if number_of_records == 0:
	if number_of_records==0:
		return 
	# sum up all the price in the rdd
	# - for each rdd, take out the LastTradeinPrice, json -> map 
	# - for all the  rdd record, sum up -> reduce 

	# - Exception handling

	price_sum=rdd.map(lambda record: float(json.loads(record[1].decode('utf-8'))[0].get('LastTradePrice'))). reduce(lambda a,b:a + b )
	average=price_sum/number_of_records
	logger.info('Received records from Kafka, average price is %f' %average)
	current_time=time.time()
	data=json.dumps({'timestamp':current_time,'average':average})
	kafka_producer.send(new_topic,value=data) 

if __name__ == '__main__':
	if(len(sys.argv)!=4):
		print("Not enough argument [kafka broker location], [kafka topic location], [kafka new topic location]")
		exit(1)

	sc=SparkContext("local[2]","StockAveragePrice")
	sc.setLogLevel('ERROR') 
	ssc=StreamingContext(sc, 5 ) 

	kafka_broker, kafka_topic, new_topic=sys.argv[1:]


	# - setup a kafka stream
	directKafkaStream=KafkaUtils.createDirectStream(ssc,[kafka_topic],{'metadata.broker.list':kafka_broker})
 	directKafkaStream.foreachRDD(process)

 	kafka_producer=KafkaProducer(bootstrap_servers=kafka_broker)


 	# - shutdown hook




 	ssc.start()
 	ssc.awaitTermination()



 

