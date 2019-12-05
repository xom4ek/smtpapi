import yaml
import tarfile
import io
import shutil
from flask import Flask, request, jsonify, send_file
from smtpwrapper import smtpwrapper
import logging
from jinja2 import Template
from easycfg import Config


LOGGER = logging.getLogger(__name__)
LOG_FORMAT = (
    '{"time":"%(asctime)s", "name": "%(name)s", "level": "%(levelname)s", "message": "%(message)s"}')

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

logging.basicConfig(level=logging.INFO)

cfg = Config('config.yml')

smtp = smtpwrapper(**cfg.smtp)


@app.route('/sendTemplate', methods=['GET', 'POST'])
def sendTemplate():
    if request.method == 'POST':
        try:
            l_files = []
            body = Template(str(request.files['template'].read().decode(
                'utf-8'))).render(request.form.to_dict())
            for key in request.files:
                if key == 'template':
                    pass
                else:
                    l_files.append({key: request.files[key].read()})
            response = smtp.sendTemplate(
                **request.form.to_dict(), body=body, files=l_files)
            if response:
                response['response_code'] = '500'
            else:
                response['response_code'] = '200'
            return jsonify(response)
        except ConnectionRefusedError as e:
            return jsonify({
                'response_code': '501',
                'response_text': e.__str__()
            })
        except ValueError as e:
            return jsonify({
                'response_code': '402',
                'response_text': e.__str__()
            })
    if request.method == 'GET':
        try:
            response = smtp.sendTemplate(**request.args)
            if response:
                response['response_code'] = '500'
            else:
                response['response_code'] = '200'
            return jsonify(response)
        except ConnectionRefusedError as e:
            return jsonify({
                'response_code': '501',
                'response_text': e.__str__()
            })
        except ValueError as e:
            return jsonify({
                'response_code': '402',
                'response_text': e.__str__()
            })
        except TypeError as e:
            return jsonify({
                'response_code': '402',
                'response_text': e.__str__()
            })
