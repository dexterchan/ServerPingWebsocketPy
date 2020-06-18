from PyPingServer.app import  app
from flask import request, jsonify,abort
from PyPingServer.service.issueJwtToken import encodeKey



@app.route("/", methods = ['POST'])
def authenticate():
    if not request.json or not 'user' in request.json:
        abort(400)
    userObj = request.json
    k = encodeKey(userObj["user"],request.url)
    return jsonify(
        {
            "user" : userObj["user"],
            "token" : k
        }
    )






from flask import make_response
@app.errorhandler(400)
def incorrectFormat(error):
    return make_response(jsonify({'error': 'incorrect request format'}), 400)
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
