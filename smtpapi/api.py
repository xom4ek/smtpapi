import yaml
import tarfile
import io
import shutil
from flask import Flask, request, jsonify, send_file
from smtpwrapper import smtpwrapper
import logging
from jinja2 import Template


LOGGER = logging.getLogger(__name__)
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


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
            body = Template(
                str(request.files['template'].read().decode('utf-8'))).render(request.form.to_dict())
            response = jsonify(smtp.sendTemplate(
                **request.form.to_dict(), body=body))
            return response
        except ConnectionRefusedError as e:
            return e.__str__()
        except ValueError as e:
            return e.__str__()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True, host=cfg.h['host'])
