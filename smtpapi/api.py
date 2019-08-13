import yaml
import tarfile
import io
import shutil
from flask import Flask, request, jsonify, send_file
from smtpwrapper import smtpwrapper
import logging
from jinja2 import Template


LOGGER = logging.getLogger(__name__)
LOG_FORMAT = (
    '{"time":"%(asctime)s", "name": "%(name)s", "level": "%(levelname)s", "message": "%(message)s"}')

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

logging.basicConfig(level=logging.INFO)


class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)


def Get_config(config):
    import yaml
    with open(config) as f:
        return Struct(**yaml.safe_load(f))


cfg = Get_config('config.yml')

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
                    # print(key)
                    # print(request.files[key])
                    l_files.append({key: request.files[key].read()})
                    # print(l_files)
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


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True, host=cfg.h['host'])
