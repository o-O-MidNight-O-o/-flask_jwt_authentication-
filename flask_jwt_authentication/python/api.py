from flask import Flask, json , jsonify , request , make_response
import jwt
import datetime
from functools import wraps

app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisisthesecretkey'

def token_required(f):
    @wraps(f)
    def  decorated(*args, **kwargs):
        token = request.args.get('token') #http://127.0.0.1:5000/route?token=adkjsd289488sadsadsazxscdzxwerfghfsde

        if not token:
            return jsonify({'message' : 'Token is missing'}),403
            
        try:
            data = jwt.decode(token,app.config["SECRET_KEY"])
        except:
            return jsonify({'message' : 'Token is invalid'}),403

        return f(*args,**kwargs)
    return decorated

@app.route('/unprotected')
def unprotected():
    return  jsonify({'message' : 'anyone can view this'})

@app.route('/protected')
@token_required
def protected():
    return jsonify({'message' : 'this is only valid for people with valid tokens'})

@app.route('/login')
def login():
    auth = request.authorization

    if auth and auth.password=='password':
        token = jwt.encode({'user' : auth.username},app.config['SECRET_KEY'])
        return jsonify({'token' : token})
    
    return make_response('could not verify!',401,{'WWW-Authenticate':'Basic realm="Login Required'})



if __name__ == "__main__":
    app.run(debug=True)