import pika
import uuid

# 5672
class requester_broker:
    def __init__(self, host='localhost'):
        self.EXCHANGE = "broker"
        self.RESPONSE = "broker_response"
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
        self.channel = self.connection.channel()
        self.queues = ['login, nlp', 'nlp_response' 'storage', 'storage_sas', 'storage_new_user']

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

    def get_login(self, user_, pass_):
        self.response = None
        self.corr_id = str(uuid.uuid4())

        body = "{\"user\":\""+ user_ + "\", \"pass\":\"" + pass_ + "\"}"

        self.channel.basic_publish(
            exchange=self.EXCHANGE,
            routing_key='login_rk',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=body)
        while self.response is None:
            self.connection.process_data_events()
        return self.response.decode("utf-8")

    def get_sas(self, id):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        id_ = "{\"id\": \"" + id + "\"}"
        user_ = "{}"
        self.channel.basic_publish(
            exchange=self.EXCHANGE,
            routing_key='new_user_rk',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=id_)
        while self.response is None:
            self.connection.process_data_events()
        return self.response.decode("utf-8")
    
    def GET_nlp_analyze(self, file):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange=self.EXCHANGE,
            routing_key='analyze_rk',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=file)
        while self.response is None:
            self.connection.process_data_events()
        return self.response.decode("utf-8")

    def GET_compare(self, file):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange=self.EXCHANGE,
            routing_key='compare_rk',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=file)
        while self.response is None:
            self.connection.process_data_events()
        return self.response