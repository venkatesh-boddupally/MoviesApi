import jwt

from datetime import datetime, timedelta
from flask import Flask, jsonify, request, make_response
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'asdggwdvashjdgaskdgqe'


def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'message': 'Token is missing'})
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message': 'Token is invalid'})
        return func(*args, **kwargs)
    return decorated

@app.route('/')
@token_required
def protected():
    return 'hello'


@app.route('/login')
def login():
    auth = request.authorization
    if auth and auth.password == 'password':
        token = jwt.encode({'user': auth.username, 'exp': datetime.utcnow() + timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('UTF-8')})
    return make_response('Could not verify', 401,  {'WWW-Authenticate': 'Basic realm="Login Required"'})


app.run(port=5004, debug=True)
