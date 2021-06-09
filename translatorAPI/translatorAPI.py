from flask import Flask, jsonify, request
from flask_cors import CORS
from requester_broker import requester_broker

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'application/json'


@app.route('/Login', methods=['GET'], strict_slashes=False)
def get_Login():
    user_ = request.headers["user"]
    pass_ = request.headers["password"]
    req = requester_broker(host='192.168.48.2')
    response_ = req.get_login(user_, pass_)
    req.connection.close()
    return jsonify(response_)


@app.route('/Books', methods=['GET'], strict_slashes=False)
def get_DocumentName():
    '''user_ = request.headers["user"]
    req = requester_broker(host='192.168.48.2')
    response_ = req.get_books(user_)
    req.connection.close()
    return jsonify(response_)'''
    # formato de la respuesta [{"name": "LOR"},{"name": "LOR2"},{"name": "LOR3"}]


@app.route('/Workers', methods=['GET'], strict_slashes=False)
def get_Workers():
    requestDocument = request.headers["documentName"]
    if (requestDocument != ""):
        req = requester_broker(host='192.168.48.2')
        response_ = req.GET_compare(requestDocument)
        req.connection.close()
        return jsonify(response_)
    else:
        response_ = jsonify({"name": ""})
        return response_
        # formato de la respuesta es [{"name": "", "lastName": ""}]


@app.route('/Progress', methods=['GET'], strict_slashes=False)
def get_Progress():
    '''user_ = request.headers["user"]
    req = requester_broker(host='192.168.48.2')
    response_ = req.GET_progress(user_)
    req.connection.close()
    return jsonify(response_)
    '''
    # formato de respuest [{"document":"LOR", "progress": "100", "documentFeel": "Hapyy", "ofensiveContent": "No"}]


@app.route('/Link', methods=['GET'], strict_slashes=False)
def get_Link():
    id_ = "2"
    req = requester_broker(host='192.168.48.2')
    response_ = req.get_sas(id_)
    req.connection.close()  # {"id": "xyz" }
    return jsonify(response_)


@app.route('/Upload', methods=['GET'], strict_slashes=False)
def get_Upload():
    document_ = request.headers["documentName"]
    req = requester_broker(host='192.168.48.2')
    responseNLP_ = req.GET_nlp_analyze(document_)
    # responseFeeling_ = req.GET_feeling_analyze(document)
    # responseContent_ = req.GET_Content_analyze(document)
    req.connection.close()
    response_ = [{"status": "ok"}]
    return jsonify(response_)


# Se ejecuta el api
if __name__ == '__main__':
    app.run(port=4000, host='0.0.0.0')
