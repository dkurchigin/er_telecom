import requests
import json
import time
from base_logger import logger

if __name__ == '__main__':
    server_addr = 'http://127.0.0.1:5000/api/sorting'
    list_ = [1, "4", 5, 6, 7, "a", "azaza", 12, 34, 0]
    several_attempts = 3
    delay = 2

    token = None

    while several_attempts != 0:
        try:
            if token:
                logger.info(f'Try to get array by token: {token}')
                response = requests.get(server_addr, data=json.dumps({'token': token}), headers={'content-type': 'application/json'})
                array_answer = response.json()
                if array_answer['array'] == 'in progress':
                    logger.info('Waiting for result...')
                else:
                    logger.info(f'We have result: {array_answer["array"]}')
                    break
            else:
                logger.info('Try to push array to server...')
                response = requests.post(server_addr, data=json.dumps({'array': list_, 'sort_reverse': True}), headers={'content-type': 'application/json'})
                status_code = response.status_code
                if status_code == 200:
                    answer = response.json()
                    if answer.get('token'):
                        token = answer['token']

                elif status_code // 400 == 1:
                    logger.error(f'Bad request {status_code}\n{response.text}\n')
        except Exception as e:
            logger.error(f'Have exception: {e}')

        time.sleep(delay)
        several_attempts -= 1
