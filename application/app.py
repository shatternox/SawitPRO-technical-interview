from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, session, abort
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from functools import wraps
from werkzeug.utils import secure_filename
import MySQLdb.cursors
import os
import re
import secrets

app = Flask(__name__)

bcrypt = Bcrypt(app)

app.secret_key = '4528f440-1791-4770-b153-73dae6de7f73'

app.config['MYSQL_HOST'] = 'db'  # Docker service name for MySQL container
app.config['MYSQL_USER'] = 'sawidproadmin'
app.config['MYSQL_PASSWORD'] = 'vaeiiGbL%j3jjQ!6duFKk79koKYLch%d'
app.config['MYSQL_DB'] = 'sawitpro'

mysql = MySQL(app)

# Create Blueprint for authentication
auth = Blueprint('auth', __name__)

# User Registration & Login routes

# Image Upload, Storage, Retrieval, and Deletion
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def authorize(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        if 'loggedin' not in session or not session['loggedin']:
            return redirect(url_for('login'))
        return f(*args, **kws)
    return decorated_function

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ""
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'confirm_password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        email = request.form['email']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s OR username = %s', (email, username))
        account = cursor.fetchone()
        if account:
            message = 'Account already exists!'
            flash(f'{message}', 'alert alert-danger')
            return redirect(url_for('register'))
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            message = 'Invalid email address!'
            flash(f'{message}', 'alert alert-danger')
            return redirect(url_for('register'))
        elif not username or not password or not email:
            message = 'Please fill out the form!'
            flash(f'{message}', 'alert alert-danger')
            return redirect(url_for('register'))
        elif password != confirm_password:
            message = 'Passwords do not match!'
            flash(f'{message}', 'alert alert-danger')
            return redirect(url_for('register'))
        else:
            image_key = secrets.token_hex(16)
            hash_password = bcrypt.generate_password_hash(password).decode('utf-8')
            cursor.execute('INSERT INTO users VALUES (NULL, %s, %s, %s, %s)', (username, hash_password, email, image_key))
            mysql.connection.commit()
            message = 'You have successfully registered!'
            flash(f'{message}', 'alert alert-success')
            return redirect(url_for('login'))

    elif request.method == 'POST':
        message = 'Please fill out the form!'
        flash(f'{message}', 'alert alert-danger')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        data = cursor.fetchone()

        if data:
            is_valid = bcrypt.check_password_hash(data['password'], password)
        
            if is_valid:
                session['loggedin'] = True
                session['id'] = data['user_id']
                session['username'] = data['username']
                session['email'] = data['email']
                message = "Logged in successfully!"
                flash(f'{message}', 'alert alert-success')
                return redirect(url_for('home'))
            else:
                message = 'Incorrect email or password!'
                flash(f'{message}', 'alert alert-danger')
        else:
            message = 'Incorrect email or password!'
            flash(f'{message}', 'alert alert-danger')

    return render_template('login.html')


@app.route('/logout')
def logout():

    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('email', None)

    return redirect(url_for('login'))


@app.route('/', methods=['GET'])
@authorize
def home():
    return render_template('index.html', username=session['username'])
        

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part', 'error')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File uploaded successfully', 'success')
            # Save the filename into the database or perform other actions
            return redirect(url_for('home'))
        else:
            flash('File type not allowed', 'error')
            return redirect(request.url)

@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    # Delete file from storage
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    # Perform necessary actions in the database to delete the filename entry
    flash('File deleted successfully', 'success')
    return redirect(url_for('home'))

# User Feedback
@app.route('/feedback', methods=['POST'])
def feedback():
    if request.method == 'POST':
        # Get form data
        feedback = request.form['feedback']
        # Insert feedback into database or perform necessary actions
        flash('Thank you for your feedback!', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.register_blueprint(auth)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.run(host='0.0.0.0', port=6969, debug=True)


