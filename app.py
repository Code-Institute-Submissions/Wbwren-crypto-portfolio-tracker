import os
import sys
import nomics
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists('env.py'):
    import env

app = Flask(__name__)

app.config['MONGO_DBNAME'] = os.environ.get('MONGO_DBNAME')
app.config['MONGO_URI'] = os.environ.get('MONGO_URI')
app.secret_key = os.environ.get('SECRET_KEY')

mongo = PyMongo(app)

api_key = os.environ.get('NOMICS_API_KEY')
nomics = nomics.Nomics(api_key)

# Function to get current prices of coins


def get_price(*argv):
    try:
        print('try')
        coin_list = nomics.get_prices()
        selected_coins = []
        for arg in argv:
            for coin in coin_list:
                if coin['currency'] == arg:
                    selected_coins.append(coin)
        price = []
        for coin in selected_coins:
            price.append(coin['price'])
        return price
    except:
        print('except')
        flash('Error connecting to server')

@app.route('/')
@app.route('/home')
def home():
    return render_template('base.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {'username': request.form.get('username').lower()})

        if existing_user:
            flash('Username already exists')
            return redirect(url_for('register'))

        register = {
            'username': request.form.get('username').lower(),
            'password': generate_password_hash(request.form.get('password'))
        }
        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session['user'] = request.form.get('username').lower()
        flash('Registration Successful!')
        return render_template('dashboard.html')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {'username': request.form.get('username').lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user['password'], request.form.get('password')):
                session['user'] = request.form.get('username').lower()
                flash('Welcome, {}'.format(request.form.get('username')))
                return redirect(url_for('dashboard'))
            else:
                # invalid password match
                flash('Incorrect Username and/or Password')
                return redirect(url_for('login'))

        else:
            # username doesn't exist
            flash('Incorrect Username and/or Password')
            return redirect(url_for('login'))

    return render_template('login.html')



@app.route('/forgotPassword', methods=['GET', 'POST'])
def forgotPassword():
    if request.method == 'POST':
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {'username': request.form.get('username').lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user['password'], request.form.get('password')):
                session['user'] = request.form.get('username').lower()
                flash('Welcome, {}'.format(request.form.get('username')))
                return redirect(url_for('dashboard'))
            else:
                # invalid password match
                flash('Incorrect Username and/or Password')
                return redirect(url_for('login'))

        else:
            # username doesn't exist
            flash('Incorrect Username and/or Password')
            return redirect(url_for('login'))

    return render_template('forgotPassword.html')


@app.route('/logout')
def logout():
    # remove user from session cookie
    session.pop('user')
    flash('You have been logged out')
    return redirect(url_for('login'))


@app.route('/dashboard')
def dashboard():
    # if 'user' not in session
    if 'user' not in session:
        return redirect(url_for('login'))
    transactions = mongo.db.transactions.find( {'user': session['user']} )
    coins = []
    for transaction in transactions:
        # add different coins to a set
        #loop through and get value of each ocin w/ 1 sec delay
        coins.append(transaction['coin'])
        
    coins_string = ' '.join(coins)
    new_string = ' '.join('"{},"'.format(word) for word in coins_string.split(' '))
    
    print('2', coins_string)

    print('4', new_string)
    print('34', new_string.split(-1))

    print('5', get_price('BTC', 'XRP'))
    
        
    
    return render_template('dashboard.html')


@app.route('/transaction')
def transaction():
    return render_template('transaction.html')


@app.route('/transaction', methods=['GET', 'POST'])
def makeTransaction():
    if request.method == 'POST':
        task = {
            'user': session['user'],
            'coin': request.form.get('coin'),
            'transactionType': request.form.get('transactionType'),
            'quantity': request.form.get('quantity'),
            'price': request.form.get('price'),
            'fee': request.form.get('fee'),
            'notes': request.form.get('notes'),
            'date': request.form.get('date')
        }
        mongo.db.transactions.insert_one(task)
        flash('Transaction Successfully Saved')
        return render_template('dashboard.html')

    # categories = mongo.db.categories.find().sort('category_name', 1)
    # return render_template('add_task.html', categories=categories)

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
