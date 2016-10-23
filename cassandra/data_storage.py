from kafka import KafkaConsumer
from cassandra.cluster import Cluster




import argparse
import atexit
import logging 
import json


topic_name=''
kafka_broker=''
key_space=''
data_table=''
cassandra_broker=''



logger_format='%(asctime)-15s %(message)s'
logging.basicConfig(format=logger_format)
logger=logging.getLogger('data-storager')
logger.setLevel(logging.DEBUG)


def save_data(msg,cassandra_session):
	# - msg is kakfa ConsumerRecord
	parsed=json.loads(msg)[0]
	symbol=parsed.get('StockSymbol')
	tradeprice=float(parsed.get('LastTradePrice'))
	tradetime=parsed.get('LastTradeDateTime')
	logger.info('received data from Kafka %s',parsed)
	logger.info('symbol %s, tradeprice %f, tradetime %s' %(symbol,tradeprice,tradetime))

	# - use CQL statement to insert data
	statement="INSERT INTO %s (stock_symbol,trade_time,trade_price) VALUES ('%s','%s',%f)" % (data_table,symbol,tradetime,tradeprice)

	cassandra_session.execute(statement)
	logger.info('Saved data to cassandra, symbol: %s, tradetime: %s, tradeprice: %f' % (symbol,tradetime,tradeprice))


if __name__=='__main__':  
	parser=argparse.ArgumentParser()
	parser.add_argument('topic_name',help='the kafka topic')
	parser.add_argument('kafka_broker',help='the location of kafka broker')
	parser.add_argument('key_space',help='the keyspace of cassandra')
	parser.add_argument('data_table',help='the data table to use')
	parser.add_argument('cassandra_broker',help='the cassandra location')

	# - parse command line arguments
	args=parser.parse_args()
	topic_name=args.topic_name
	kafka_broker=args.kafka_broker
	key_space=args.key_space
	data_table=args.data_table
	cassandra_broker=args.cassandra_broker

	logger.info('topic_name %s, kafka_borker %s, key_space %s, data_table %s, cassandra_broker %s' %(topic_name,kafka_broker,key_space,data_table,cassandra_broker))


	# - setup kafka consumer
	consumer=KafkaConsumer(topic_name,bootstrap_servers=kafka_broker) 


	# - setup cassandra client/session
	cassandra_cluster=Cluster(contact_points=cassandra_broker.split(','))
	session=cassandra_cluster.connect(key_space) 



	for msg in consumer:
		save_data(msg.value,session)