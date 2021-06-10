import flask
from flask import request
from storage import *

storage_api = flask.Flask(__name__)
storage_api.config["DEBUG"] = False


@storage_api.route('/test/', methods=['GET'], strict_slashes=False)
def api_home():
    return "Hello from Storage API"


@storage_api.route('/newuser/', methods=['POST'],strict_slashes=False)
def new_container():
    container_name = request.args['name']
    response = create_container(container_name)
    return response


@storage_api.route('/upload/', methods=['POST'], strict_slashes=False)
def new_file():
    if 'file' not in request.files:
        print("No file detected")
        return "No file detected"

    file = request.files["file"]
    container_name = request.args["user"]
    response = upload_file(container_name, file)
    return response


@storage_api.route('/download/', methods=['POST'], strict_slashes=False)
def dowload_file():
    container_name = request.args["user"]
    filename = request.args["filename"]

    response = download(container_name, filename)
    return response


@storage_api.route('/ping')
def ping():
    return 'PONG', 200

storage_api.run(host='0.0.0.0')
