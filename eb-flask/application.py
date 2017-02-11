
from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp
#import bcrypt
import stripe

from flask_cors import CORS, cross_origin 

STRIPE_PUBLISHABLE_KEY = 'pk_test_HPcZRSKmS17XqjEEA48QoYvh'  
STRIPE_SECRET_KEY = 'sk_test_TRBGyYCU1ze6s9uOhBSr52f5'

stripe.api_key = STRIPE_SECRET_KEY




app = Flask(__name__,template_folder='templates')

CORS(app)

app.config['MONGO_DBNAME'] = 'userdb'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/userdb'

mongo = PyMongo(app)

#class User(object):
#    def __init__(self, id, username, password):
#        self.id = id
#        self.username = username
#        self.password = password
#
#    def __str__(self):
#        return "User(id='%s')" % self.id
    
#user = User(1, 'user', 'password')

#def authenticate(username, password):
#    if username == user.username and password == user.password:
#        return user
#
#def identity(payload):
#    return user

#jwt = JWT(app, authenticate, identity)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    if request.method == 'OPTIONS':
        response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
        headers = request.headers.get('Access-Control-Request-Headers')
        if headers:
            response.headers['Access-Control-Allow-Headers'] = headers
    return response





@app.route('/')
def index():
#    if 'username' in session:
        #return 'You are logged in as ' + session['username']

    return render_template('home.html')
#
##@app.route('/home', methods=['POST','GET'])
##def home():
##    return render_template(index.html)
#
@app.route('/login', methods=['POST', 'GET'])
#@jwt_required()
def login():
    
    users = mongo.db.users
    login_user = users.find_one({'name' : request.form['username']})

    if login_user:
        #return ("You are a New User")
        #m = request.form['pass'].encode('utf-8'), login_user['password'].encode('utf-8')
        #if bcrypt.hashpw(request.form['pass'], login_user['password']) == login_user['password'] :
        if request.form['pass'] == login_user['password'] :    
            session['username'] = request.form['username']
            #return ("Successful Login")
            return render_template('index3.html')

    return 'Invalid username/password combination'
#
@app.route('/register', methods=['POST', 'GET'])
#@jwt_required()
def register():
    
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            #hashpass = bcrypt.hashpw(request.form['pass'], bcrypt.gensalt())
            hashpass = request.form['pass']
            users.insert({'name' : request.form['username'], 'password' : hashpass})
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        
        return 'That username already exists!'
#
    return render_template('register.html')


@app.route('/payment', methods=['POST'])
def payment_proceed():
    
    token = request.POST['stripeToken']
    # Amount in cents
    amount = 25000

#    customer = stripe.Customer.create(
#        email=request.form['stripeEmail'],
#        source=request.form['stripeToken']
#    )

    charge = stripe.Charge.create(
        amount=amount,
        currency='usd',
        customer=customer.id,
        description='A payment for the Hello World project'
    )

    return render_template('payment_complete.html')

if __name__ == '__main__':
    
    

    app.secret_key = 'newsecret'
    app.run(debug=True, host='0.0.0.0')
