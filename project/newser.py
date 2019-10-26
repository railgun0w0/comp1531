from json import dumps
from flask import Flask, request

from testnew import fn_channel_create

APP = Flask(__name__)

@APP.route('/channels/create', methods=['POST'])
def create():
    channel = fn_channel_create(request.form.get('token'), request.form.get('is_public'), request.form.get('name'))
    return dumps(channel)

if __name__ == '__main__':
    APP.run(port=20000)


