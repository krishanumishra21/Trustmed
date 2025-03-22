from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient
from cryptography.fernet import Fernet

app = Flask(__name__)
app.secret_key = 'your_secret_key' 

# MongoDB setup k lie
client = MongoClient('mongodb://localhost:27017/')
db = client['health_data'] 
users = db['users'] 

#encryption setup k lie
key = Fernet.generate_key()  
cipher_suite = Fernet(key)  # Create a Fernet object


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        # Check if user already exists
        if users.find_one({'username': username}):
            flash('Username already exists!', 'error')
            return redirect(url_for('register'))  # Redirect to the register route

        # Encrypt password
        encrypted_password = cipher_suite.encrypt(password.encode())

        # Insert user into MongoDB
        users.insert_one({
            'username': username,
            'password': encrypted_password,
            'role': role
        })
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))  # Redirect to the login route

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Find user in MongoDB
        user = users.find_one({'username': username})

        # Check if user exists and password is correct
        if user and cipher_suite.decrypt(user['password']).decode() == password:
            session['username'] = username
            session['role'] = user['role']
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))  # Redirect to the dashboard route
        else:
            flash('Invalid username or password!', 'error')

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'], role=session['role'])
    else:
        flash('Please login to access the dashboard.', 'error')
        return redirect(url_for('login'))  # Redirect to the login route

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))  # Redirect to the home route

if __name__ == '__main__':
    app.run(debug=True)