import yaml
import tarfile
import io
import shutil
from flask import Flask, request, jsonify, send_file
from smtpwrapper import smtpwrapper
from smtpwrapper import Email

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

class Struct:
        def __init__(self, **entries):
            self.__dict__.update(entries)
def Get_config(config):
    import yaml
    with open(config) as f:
        return Struct(**yaml.safe_load(f))

cfg=Get_config('config.yml')

smtp=smtpwrapper(**cfg.smtp)


@app.route('/sendMail')
def sendMail():
    try:
        response = jsonify(smtp.sendEmail(**request.args.to_dict()))
        return response
    except TypeError:
        return 'Wrong parameters'


@app.route('/sendTemplate')
def sendTemplate():
    try:
        response = jsonify(smtp.sendTemplate(**request.args.to_dict()))
        return response
    except TypeError:
        return 'Wrong parameters'

if __name__ == '__main__':
    app.run()