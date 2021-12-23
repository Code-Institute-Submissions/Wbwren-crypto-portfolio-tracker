import os
import sys
import nomics
import time
from flask import (
    Flask, flash, render_template, json,
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


@app.route('/')
@app.route('/home')
def home():
    if 'user' in session:
        return redirect(url_for('dashboard'))
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



def get_price(coins):
    coin_list = nomics.ExchangeRates.get_rates()
    selected_coins = []
       
    for i in coins:
        for coin in coin_list:
            if coin['currency'] == i.upper():
                selected_coins.append(coin)
    return selected_coins



@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))

    
    def updateBalance():
        transactions = mongo.db.transactions.find( {'user': session['user']} )
        balance = 0
        coinsSold = []
        quantitiesSold = []
        coinsPurchased = []
        quantitiesPurchased= []

        for transaction in transactions:
            if transaction['transactionType'] == 'buy':
                if transaction['coin'] not in coinsPurchased:
                    coinsPurchased.append(transaction['coin'])
                    quantitiesPurchased.append(transaction['quantity'])
                else:
                    for i in range(len(coinsPurchased)):
                        if coinsPurchased[i] == transaction['coin']:
                            quantitiesPurchased[i] += transaction['quantity']
                            break
                    
            else:
                if transaction['coin'] not in coinsSold:
                    coinsSold.append(transaction['coin'])
                    quantitiesSold.append(transaction['quantity'])
                else:
                    for i in range(len(coinsSold)):
                        if coinsSold[i] == transaction['coin']:
                            quantitiesSold[i] += transaction['quantity']
                            break

        try:
            nomics_coins = get_price(coinsPurchased)
        except:
            flash('Failed to retrieve live prices')
    
        prices = []
        for coin in nomics_coins:
            prices.append(coin['rate'])
        
        for i in range(len(coinsPurchased)):
            balance += float(quantitiesPurchased[i]) * float(prices[i])

        return balance


    def getTotalCost():
        transactions = mongo.db.transactions.find( {'user': session['user']} )
        totalCost = 0
        
        for transaction in transactions:
            totalCost += transaction['cost']
        return totalCost
    

    
    def getUserCoinList():
        coinsPurchased = []
        quantitiesPurchased= []
        transactions = mongo.db.transactions.find( {'user': session['user']} )
        for transaction in transactions:
            if transaction['transactionType'] == 'buy':
                if transaction['coin'] not in coinsPurchased:
                    coinsPurchased.append(transaction['coin'])
                    quantitiesPurchased.append(transaction['quantity'])
                else:
                    for i in range(len(coinsPurchased)):
                        if coinsPurchased[i] == transaction['coin']:
                            quantitiesPurchased[i] += transaction['quantity']
                            break
        
        user_coin_list = {}
        for i in range(len(coinsPurchased)):
            user_coin_list[coinsPurchased[i]] = quantitiesPurchased[i]
        return user_coin_list

    balance = updateBalance()
    cost = getTotalCost()
    profit_loss = balance - cost
    user_coin_list = getUserCoinList()


    coins = mongo.db.ticker_symbols.find()
   
    list_of_coins = []
    
    for coin in coins:
        list_of_coins.append(coin['ticker_symbol'])
        

    if request.method == 'POST':
        transaction = {
            'user': session['user'],
            'coin': request.form.get('coin'),
            'transactionType': request.form.get('transactionType'),
            'quantity': float(request.form.get('quantity')),
            'cost': float(request.form.get('cost')),
            'fee': float(request.form.get('fee')),
            'date': request.form.get('date')
        }
        mongo.db.transactions.insert_one(transaction)
        # delay api call as limited to one call per second
        time.sleep(1)
        balance = updateBalance()
        cost = getTotalCost()
        getUserCoinList()
        flash('Transaction Successfully Saved')


    return render_template('dashboard.html', balance=balance, cost=cost, profit_loss=profit_loss, user_coin_list=user_coin_list, list_of_coins=list_of_coins)



@app.route('/transactions', methods=['GET', 'POST'])
def transactions():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    transactions = mongo.db.transactions.find( {'user': session['user']} )

    transactions_list = []
    for transaction in transactions:
        transaction.pop('_id')
        transaction.pop('user')
        transactions_list.append(transaction)
    return render_template('transactions.html', transactions=transactions_list)
    


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
