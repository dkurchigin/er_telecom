from flask import Flask, request, Response
import json
import numpy
import time
import hashlib
from celery import Celery
import redis

broker_url = 'redis://localhost:6379/0'
app = Flask(__name__)
r = redis.Redis()

celery = Celery(app.name, broker=broker_url)
app.config.from_object("config")

@celery.task
def sort_array(array_, hash_, sort_reverse=False):
    r.get(hash_)
    cleared_array = [element for element in array_ if isinstance(element, int) or isinstance(element, float)]
    cleared_array.sort(reverse=sort_reverse)
    cleared_array.append(round(numpy.average(cleared_array), 2))
    # time.sleep(20)
    r.set(hash_, json.dumps(cleared_array))

def calc_hash(addr):
    current_timestamp = time.time()
    return hashlib.md5(f'{current_timestamp}{addr}'.encode()).hexdigest()

@app.route('/api/sorting', methods=['POST'])
def get_sort():
    if request.method == 'POST':
        data = request.get_json()

        if data.get('token'):
            # CHECK OUR ARRAY BY TOKEN
            token = data['token']
            if r.exists(token):
                entry = r.get(token)
                if entry != b'':
                    entry = json.loads(entry)
                    return Response(json.dumps({'array': entry}), content_type='application/json', status=200)
                else:
                    return Response(json.dumps({'array': 'in progress'}), content_type='application/json', status=200)
            else:
                return Response(status=400, response=f'Can\'t find token {token} in DB')

        elif data.get('array'):
            # TRY TO SORT ARRAY
            hashed_ts = calc_hash(request.remote_addr)
            r.set(hashed_ts, '')
            sorting_type = data.get('sort_reverse') if isinstance(data.get('sort_reverse'), bool) else False
            sort_array.delay(data['array'], hashed_ts, sorting_type)
            return Response(json.dumps({'token': hashed_ts}), content_type='application/json', status=200)

        else:
            return Response(status=400, response = 'Response without \'array\' or \'token\'in JSON. Check right response structure')

if __name__ == '__main__':
    r.flushall()
    app.run()

