from kafka import KafkaProducer 
from googlefinance import getQuotes
from kafka.errors import KafkaError, KafkaTimeoutError

import random
import argparse
import time 
import json
import logging
import schedule
import atexit
import datetime 

topic_name=''
kafka_broker=''
logger_format='%(asctime)-15s %(message)s'
logging.basicConfig(format=logger_format)
logger=logging.getLogger('data_producer')
logger.setLevel(logging.DEBUG)



def fetch_price(producer,symbol):
	#price=json.dumps(getQuotes(symbol));
	try:
		price=random.randint(30,120)
		timestamp=datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%dT%H:%MZ')
		payload=('[{"StockSymbol":"AAPL","LastTradePrice":%d,"LastTradeDateTime":"%s"}]'%(price,timestamp)).encode('utf-8')
		logger.debug('Get stock price %s',price)
		producer.send(topic=topic_name,value=payload,timestamp_ms=time.time())
		logger.debug('Sent stock price for %s to Kafka',symbol)
	except KafkaTimeoutError as timeout_error:
		logger.warn('Failed to send message for %s to kafka, caused by %s',(symbol,timeout_error.message))
	except Exception:
		logger.warn('Failed to fetch stock price for %s',symbol)


#	logger.debug('Successfully Sent data to Kafka')



def shutdown_hook(producer):
	try:
		logger.info('preparing to shutdown, waiting for producer to flush message to 10s')
		producer.flush(10)
		logger.info('producer flush finished to kafka')
	except KafkaError as kafka_error:
		logger.warn('Failed to flush pending messages to kafka, caused by: %s',kafka_error.message)
	finally:
		try:
			logger.info('Closing kafka connection')
			producer.close(10)	
		except Exception as e:
			logger.warn('Failed to close kafka connction, caused by: %s', e.message)




if __name__=='__main__':
	parser=argparse.ArgumentParser()
	parser.add_argument('symbol',help='the stock symbol')
	parser.add_argument('topic_name',help='the kafka topic to push to')
	parser.add_argument('kafka_broker',help='location of kafka broker')

	args=parser.parse_args()
	symbol=args.symbol
	topic_name=args.topic_name
	kafka_broker=args.kafka_broker

	producer=KafkaProducer(bootstrap_servers=kafka_broker) 

	# - schedule and run every second
	schedule.every(1).second.do(fetch_price,producer,symbol)
	

	# - register shutdown hook
	atexit.register(shutdown_hook,producer)

	#-kick start 
	while True:
		schedule.run_pending()
		time.sleep(1)