from flask import Flask, request, Response
import json
import numpy
import time
import hashlib
# from celery import Celery
#
# broker_url = 'amqp://guest@localhost'          # Broker URL for RabbitMQ task queue

app = Flask(__name__)


def sort_array(array_, hash_, sort_reverse=False):
    cleared_array = [element for element in array_ if isinstance(element, int) or isinstance(element, float)]
    cleared_array.sort(reverse=sort_reverse)
    cleared_array.append(round(numpy.average(cleared_array), 2))
    time.sleep(5)
    tasks[hash_] = cleared_array

tasks = {}

# celery = Celery(app.name, broker=broker_url)
# celery.config_from_object('celeryconfig')      # Your celery configurations in a celeryconfig.py

# @celery.task(bind=True)
# def some_long_task(self, x, y):
#     # Do some long task
#     ...

@app.route('/api/sorting', methods=['POST'])
def get_sort():
    if request.method == 'POST':
        data = request.get_json()
        if data.get('token'):
            token = data['token']
            if token in tasks.keys():
                if not isinstance(tasks[token], False):
                    return Response(
                        json.dumps({'array': tasks[token]}),
                        content_type='application/json',
                        status=200
                    )
                else:
                    return Response(
                        json.dumps({'array': 'in progress'}),
                        content_type='application/json',
                        status=200
                    )
            else:
                return Response(
                    status=400,
                    response=f'Can\'t find token {token} in DB'
                )
        elif data.get('array'):
            user_ip = request.remote_addr
            current_timestamp = time.time()
            hashed_ts = hashlib.md5(f'{current_timestamp}{user_ip}'.encode()).hexdigest()
            tasks[hashed_ts] = False
            sort_array(data['array'], hashed_ts)
            return Response(
                json.dumps({'token': hashed_ts}),
                content_type='application/json',
                status=200
            )
        else:
            return Response(
                status=400,
                response = 'Response without \'array\' or \'token\'in JSON. Check right response structure'
            )


if __name__ == '__main__':
    app.run()

