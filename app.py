from flask import Flask, render_template, request, redirect, url_for, session, send_file, send_from_directory
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '6300'  # Replace with your MySQL password
app.config['MYSQL_DB'] = 'geeklogin'

mysql = MySQL(app)

@app.route('/')
@app.route('/index')
def index():
    if 'loggedin' in session:
        # Specify the full path to your HTML file
        html_path = r"D:\\HTML\\Yax\\Untitled-1.html"
        return send_file(html_path)
    return redirect(url_for('login_register'))

@app.route('/login_register', methods=['GET', 'POST'])
def login_register():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form.get('email')  # Use get() to handle registration without email

        hashed_password = generate_password_hash(password)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        if 'login' in request.form:
            cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
            account = cursor.fetchone()

            if account and check_password_hash(account['password'], password):
                session['loggedin'] = True
                session['id'] = account['id']
                session['username'] = account['username']
                msg = 'Logged in successfully!'
                return render_template('index.html', username=session['username'], msg=msg)
            else:
                msg = 'Incorrect username/password!'

        elif 'register' in request.form:
            cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
            account = cursor.fetchone()

            if account:
                msg = 'Account already exists!'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Invalid email address!'
            elif not re.match(r'[A-Za-z0-9]+', username):
                msg = 'Username must contain only characters and numbers!'
            elif not username or not password or not email:
                msg = 'Please fill out the form!'
            else:
                confirm_password = request.form['confirm_password']
                if password != confirm_password:
                    msg = 'Passwords do not match!'
                else:
                    cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, hashed_password, email))
                    mysql.connection.commit()
                    msg = 'You have successfully registered!'

        cursor.close()

    return render_template('login_register.html', msg=msg)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login_register'))

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'img/user.png', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run(debug=True)
