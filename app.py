from flask import Flask, Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
import json
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import func


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Mackee'

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///database.db'
else:
    try:
        import psycopg2
        app.debug = False
        # Replace actual credentials with placeholders
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@hostname:5432/database_name'
    except ImportError:
        print("Warning: PostgreSQL dependencies not available. Falling back to SQLite.")
        app.debug = True
        ENV = 'dev' 
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///database.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    sex = db.Column(db.String(20))
    birthdate = db.Column(db.String(50))
    joined = db.Column(db.DateTime(timezone=True), default=func.now())
    message = db.relationship('Message')


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String, db.ForeignKey('user.username'))
    #changed to string from integer
    receiver = db.Column(db.String(100))
    message = db.Column(db.String(10000))
    time_sent = db.Column(db.DateTime(timezone=True), default=func.now())

class Global_Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String, db.ForeignKey('user.username'))
    global_message = db.Column(db.String(10000))
    time_sent = db.Column(db.DateTime(timezone=True), default=func.now())


views = Blueprint('views', __name__)
auth = Blueprint('auth', __name__)


@views.route('/', methods=['GET', 'POST'])
def home():
    messages = Message.query.all()
    if request.method == 'POST':
        message = request.form.get('message')
        receiver = request.form.get('tousername')
        if len(message) >= 10000:
            flash("Message is too long.", category='error')
        elif User.query.filter_by(username=receiver).first():
            new_message = Message(sender=current_user.username, receiver=receiver, message=message)
            db.session.add(new_message)
            db.session.commit()
        else:
            flash("User does not exist.", category='error')
    return render_template("home.html", user=current_user, messages=messages)


@views.route('/delete-message', methods=['POST'])
def delete_message():
    message = json.loads(request.data)
    message_id = message['message_id']
    message = Message.query.get(message_id)
    if message:
        if message.receiver == current_user.username:
            db.session.delete(message)
            db.session.commit()

    return jsonify({})


@views.route('/messageboard', methods=['GET', 'POST'])
@login_required
def messageboard():
    global_messages = Global_Messages.query.all()
    global_messages.reverse()
    if request.method == 'POST':
        global_message = request.form.get('global_message')
        if len(global_message) >= 10000:
            flash("Message is too long.", category='error')
        else:
            new_global_message = Global_Messages(sender=current_user.username, global_message=global_message)
            db.session.add(new_global_message)
            db.session.commit()
    return render_template("messageboard.html", global_messages=global_messages, user=current_user)


@views.route('/delete-global-message', methods=['POST'])
def delete_global_message():
    global_message = json.loads(request.data)
    global_message_id = global_message['global_message_id']
    global_message = Global_Messages.query.get(global_message_id)
    if global_message:
        if global_message.sender == current_user.username or current_user.username == 'Mackee' or current_user.username == 'lukesch':
            db.session.delete(global_message)
            db.session.commit()
    return jsonify({})



@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Username does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        sex = request.form.get('sex')
        birthdate = request.form.get('birthdate')

        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif len(last_name) < 2:
            flash('Last name must be greater than 1 character.', category='error')
        elif len(username) < 6:
            flash('Username must be at least 6 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(first_name=first_name,
                            last_name=last_name,
                            username=username,
                            password=generate_password_hash(password1, method='sha256'),
                            sex=sex,
                            birthdate=birthdate,)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("signup.html", user=current_user)


app.register_blueprint(views, url_prefix='/')
app.register_blueprint(auth, url_prefix='/')


login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, threaded=True)

