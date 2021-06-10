import pika
import uuid

# 5672
class storage_requester:
    def __init__(self, host='localhost'):
        self.EXCHANGE = "broker"
        self.RESPONSE = "broker_response"
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
        self.channel = self.connection.channel()
        self.queues = ['storage_sas', 'storage_new_user']

        self.channel.exchange_declare(exchange=self.EXCHANGE, exchange_type='direct')

        result = self.channel.queue_declare(queue=self.RESPONSE, exclusive=True) #Cola de respuesta.
        self.callback_queue = result.method.queue
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body


    def get_sas(self, id):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        id_ = "{\"id\": \"" + id + "\"}"
        self.channel.basic_publish(
            exchange=self.EXCHANGE,
            routing_key='sas_rk',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=id_)
        while self.response is None:
            self.connection.process_data_events()
        return self.response.decode("utf-8")


req = storage_requester()
print(req.get_sas("3"))
#print(req.GET_compare("textoprueba.txt"))
req.connection.close()

#https://dev.to/usamaashraf/microservices--rabbitmq-on-docker-e2f