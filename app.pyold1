import json
import os
from flask import Flask, render_template, request, redirect, url_for, session
from engine import calculate_arbitrage, get_exchange_name
from config import EXCHANGES  # Import the EXCHANGES dictionary
from auth import authenticate_user, is_admin

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set the secret key before using the session object

# Load user data from the JSON file
with open('user_data.json', 'r') as f:
    users = json.load(f)
    
# Function to update user password and save back to the JSON file
def update_user_password(username, new_password):
    if not os.access('user_data.json', os.W_OK):
        return False  # No write permission

    users[username] = new_password
    with open('user_data.json', 'w') as f:
        json.dump(users, f, indent=4)
    
    return True

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not session.get('logged_in') or not session.get('username'):
        return redirect(url_for('login'))

    if not is_admin(session['username']):
        return render_template('admin.html', admin=False)

    return render_template('admin.html', admin=True, users=users)
        
    
@app.route('/admin/edit', methods=['POST'])
def edit_user_data():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if not is_admin(session['username']):
        return redirect(url_for('admin'))

    username = request.form['username']
    new_password = request.form['new_password']
    if update_user_password(username, new_password):
        return redirect(url_for('admin'))
    else:
        return "Failed to update password due to write permission issue."
   
    
@app.route('/')
def index():
    if session.get('logged_in'):
        return render_template('index.html', positive_count=0, negative_count=0, exchanges=EXCHANGES)
    return redirect(url_for('login'))

@app.route('/main')
def main():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    return render_template('index.html', positive_count=0, negative_count=0, exchanges=EXCHANGES)
 
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if authenticate_user(username, password):
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('main'))
        else:
            return render_template('login.html', error_message='Invalid username or password')
    
    return render_template('login.html', error_message=None)

@app.route('/calculate', methods=['POST'])
def calculate():
    exchange1 = request.form['exchange1']
    exchange2 = request.form['exchange2']

    data = calculate_arbitrage(exchange1, exchange2)
    
    # Count the number of positive and negative arbitrage opportunities
    positive_count = sum(1 for item in data if item['arbitrage'] > 0)
    negative_count = sum(1 for item in data if item['arbitrage'] < 0)
    
    # Get the exchange names for display
    exchange1_name = get_exchange_name(exchange1)
    exchange2_name = get_exchange_name(exchange2)
    
    return render_template(
        'index.html',
        positive_count=positive_count,
        negative_count=negative_count,
        data=data,
        exchange1_name=exchange1_name,
        exchange2_name=exchange2_name,
        exchanges=EXCHANGES
    )

if __name__ == '__main__':
    app.run()
