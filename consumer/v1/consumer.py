from confluent_kafka import Consumer

conf = {'bootstrap.servers': "broker:9092",
        'group.id': "foo",
        'auto.offset.reset': 'smallest'}

consumer = Consumer(conf)

running = False

try:
    consumer.subscribe(["firstTest"])

    msg = consumer.poll(timeout=1.0)
    if msg is None: 
        pass
    elif msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            # End of partition event
            sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                (msg.topic(), msg.partition(), msg.offset()))
        elif msg.error():
            raise KafkaException(msg.error())
    else:
        print(msg.value())
        
finally:
    # Close down consumer to commit final offsets.
    consumer.close()