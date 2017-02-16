import os
from flask import Flask, render_template, request
import stripe

stripe_keys = {
# THESE ARE ASSOCIATED WITH A TEST STRIPE ACCOUNT I CREATED
# EMAIL: jcv2130@columbia.edu   PASSWORD: Stripe-6998
  'secret_key': 'sk_test_3j6MZnoQAeouutV20UvLYbDc',
  'publishable_key': 'pk_test_SZibWcrgprftGMkKK0d3PBdi'
}

stripe.api_key = stripe_keys['secret_key']

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', key=stripe_keys['publishable_key'])

@app.route('/charge', methods=['POST'])
def charge():
    # Amount in cents
    amount = 500

    customer = stripe.Customer.create(
        email='customer@example.com',
        source=request.form['stripeToken']
    )

    charge = stripe.Charge.create(
        customer=customer.id,
        amount=amount,
        currency='usd',
        description='Flask Charge'
    )

    return render_template('charge.html', amount=amount)

if __name__ == '__main__':
    app.run(debug=True)
