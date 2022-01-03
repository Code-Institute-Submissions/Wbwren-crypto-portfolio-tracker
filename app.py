import os
from dns.query import _set_selector_class
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
def forgot_password():
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



def get_price(coins_purchased):
    coins_string = ""
    for k, v in coins_purchased.items():
        coins_string += k.upper() + ","
    coins_string = coins_string[:-1]
    
    return nomics.Currencies.get_currencies(coins_string)
    
 



@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))

    
    def update_balance():
        transactions = mongo.db.transactions.find( {'user': session['user']} )
        balance = 0
        coins_purchased = {}
        coins_sold = {}

        for transaction in transactions:
            if transaction['transactionType'] == 'buy':
                if transaction['coin'] not in coins_purchased:
                    coins_purchased[transaction['coin']] = float(transaction['quantity'])
                else:
                    for k in coins_purchased.items():
                        if k == transaction['coin']:
                            coins_purchased[k] += float(transaction['quantity'])
                            break  
            else:
                if transaction['coin'] in coins_purchased:
                    for k in coins_purchased.items():
                        if k == transaction['coin']:
                            coins_purchased[k] -= float(transaction['quantity'])
                            break

        try:
            nomics_coins = get_price(coins_purchased)
        except:
            print('could not retrieve prices')
            flash('Failed to retrieve live prices')
    
        prices = []
        for coin in nomics_coins:
            prices.append(coin['price'])
        
        i = 0
        for k, v in coins_purchased.items():
            if k in coins_sold:
                coins_purchased[k] -= coins_sold[k]
            # print('coin quantity: {0}, coin price: {1}'.format(coins_purchased[k], prices[i]))
            balance += coins_purchased[k] * float(prices[i])
            i += 1
        return balance


    coins = mongo.db.ticker_symbols.find()
   
    list_of_coins = []
    i = 0
    for coin in coins:
        print('fetching a coin')
        print(i)
        i += 1
        list_of_coins.append(coin['id'])


    def get_total_cost():
        transactions = mongo.db.transactions.find( {'user': session['user']} )
        total_cost = 0
        
        for transaction in transactions:
            if transaction['transactionType'] == 'buy':
                total_cost += transaction['cost']
            elif transaction['transactionType'] == 'sell':
                total_cost -= transaction['cost']
        return total_cost
    

    
    def get_user_coin_list():
        user_coin_list = {}

        transactions = mongo.db.transactions.find( {'user': session['user']} )
        for transaction in transactions:
            if transaction['transactionType'] == 'buy':
                if transaction['coin'] not in user_coin_list:
                    user_coin_list[transaction['coin']] = float(transaction['quantity'])
                else:
                    for k, v in user_coin_list.items():
                        if k == transaction['coin']:
                            user_coin_list[k] += float(transaction['quantity'])
                            break  
            else:
                if transaction['coin'] in user_coin_list:
                    for k, v in user_coin_list.items():
                        if k == transaction['coin']:
                            user_coin_list[k] -= float(transaction['quantity'])
                            break
        return user_coin_list

 
    if request.method == 'POST':
        transaction = {
            'user': session['user'],
            'coin': request.form.get('coin'),
            'transactionType': request.form.get('transactionType'),
            'quantity': float(request.form.get('quantity')),
            'cost': float(request.form.get('cost'))
        }
        mongo.db.transactions.insert_one(transaction)
        # delay API call as limited to one call per second
        time.sleep(1)
        flash('Transaction Successfully Saved')

    user_coin_list = get_user_coin_list()
    balance = update_balance()
    cost = get_total_cost()
    profit_loss = balance - cost

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
