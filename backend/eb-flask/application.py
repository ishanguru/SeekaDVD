
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

application = Flask(__name__,template_folder='templates')

CORS(application)

application.config['MONGO_DBNAME'] = 'userdb'
application.config['MONGO_URI'] = 'mongodb://Gunnernet:nachiket_99@ds147069.mlab.com:47069/userdb'

mongo = PyMongo(application)

#class User(object):
#    def __init__(self, id, inputEmail, password):
#        self.id = id
#        self.inputEmail = inputEmail
#        self.password = password
#
#    def __str__(self):
#        return "User(id='%s')" % self.id
    
#user = User(1, 'user', 'password')

#def authenticate(inputEmail, password):
#    if inputEmail == user.inputEmail and password == user.password:
#        return user
#
#def identity(payload):
#    return user

#jwt = JWT(app, authenticate, identity)

@application.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    if request.method == 'OPTIONS':
        response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
        headers = request.headers.get('Access-Control-Request-Headers')
        if headers:
            response.headers['Access-Control-Allow-Headers'] = headers
    return response





@application.route('/')
def index():
#    if 'inputEmail' in session:
        #return 'You are logged in as ' + session['inputEmail']

    return render_template('login.html')
#
##@application.route('/home', methods=['POST','GET'])
##def home():
##    return render_template(index.html)
#
@application.route('/login', methods=['POST', 'GET'])
#@jwt_required()
def login():
    print('Cool stuff bro')
    users = mongo.db.users
    login_user = users.find_one({'name' : request.form['inputEmail']})

    if login_user:
        #return ("You are a New User")
        #m = request.form['pass'].encode('utf-8'), login_user['password'].encode('utf-8')
        #if bcrypt.hashpw(request.form['pass'], login_user['password']) == login_user['password'] :
        if request.form['inputPassword'] == login_user['password'] :    
            session['inputEmail'] = request.form['inputEmail']
            email = request.form['inputEmail']
            # return redirect(url_for('login'))
            print email
            #return ("Successful Login")
            return render_template('index3.html', email=email)

    return 'Invalid inputEmail/password combination'
#
@application.route('/register', methods=['POST', 'GET'])
#@jwt_required()
def register():
    print('registering user')
    if request.method == 'POST':
        try: 
            users = mongo.db.users
            existing_user = users.find_one({'name' : request.form['inputEmail']})
        except:
            print "failed to find user"

        if existing_user is None:
            #hashpass = bcrypt.hashpw(request.form['pass'], bcrypt.gensalt())
            print('creating user')
            hashpass = request.form['inputPassword']
            users.insert({'name' : request.form['inputEmail'], 'password' : hashpass})
            session['inputEmail'] = request.form['inputEmail']
            email = request.form['inputEmail']
            # return redirect(url_for('login'))
            print email
            return render_template('index3.html', email=email)
        
        return 'That inputEmail already exists!'
#
    return render_template('login.html')


@application.route('/payment', methods=['POST', 'GET'])
def payment():
    
    print("Making payment")
    token = request.form['stripeToken']
    # Amount in cents
    amount = 25000
    print(token)

    # customer = stripe.Customer.create(
    #    email=request.form['stripeEmail'],
    #    source=request.form['stripeToken']
    # )

    # print("Customer created")
    # print(customer)

    print("Charging Customer")
    charge = stripe.Charge.create(
        amount=amount,
        currency='usd',
        # customer=request.form['stripeEmail'],
        description='A payment for the Hello World project',
        source=token
    )
    print(charge)

    return render_template('index3.html')

if __name__ == '__main__':
    
    application.secret_key = 'newsecret'
    application.run(debug=True, host='0.0.0.0')
