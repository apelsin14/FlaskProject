from flask import Flask, request
from config import config_logging
import logging.config

app = Flask(__name__)

logging.config.dictConfig(config_logging)
logger = logging.getLogger('server_logger')


@app.route('/logs')
def logs_get():
    logger.info('GET-request received')
    with open('utils.log', 'r') as file:
        return file.read().replace('\n', '</br>')


@app.route('/logs', methods=['POST'])
def logs_post():
    logger.info('POST-request received')
    data = request.json
    try:
        logger.log(getattr(logging, data['level'].upper()), f"{data['service']}: {data['message']}", extra=data)
        return "Success", 200
    except (ValueError, KeyError) as ex:
        logger.error(f"Failed: \n{ex}")
        return f"Failed: {ex}", 400


if __name__ == '__main__':
    app.run(debug=True)
