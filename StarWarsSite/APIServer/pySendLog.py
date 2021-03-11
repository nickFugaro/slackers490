import pika
import simplejson as json
import uuid

filename = ''
stacktrace = ''
class theClient(object):

    def __init__(self):
        creds = pika.PlainCredentials('test','test')
        print('Establishing Connection To Server')
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('25.93.61.112',5672,'vhost',creds))
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(queue='clientLogCallback', exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(queue=self.callback_queue, on_message_callback=self.on_response, auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='testExchange', routing_key='rpc_queue', properties=pika.BasicProperties(reply_to=self.callback_queue, correlation_id=self.corr_id),
        body = json.dumps({
            'type' : 'log',
            'vm_name' : filename,
            'function' : stacktrace,
            'message' : 'Error!'
            }))
        while self.response is None:
            self.connection.process_data_events()
        return self.response

def main(file, stack):
    global filename
    filename = file
    global stacktrace
    stacktrace = stack
    message = theClient()

    print("Sending")
    response = message.call()
    print(response)