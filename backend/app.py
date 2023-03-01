# make sure you are in the backend folder in cmd
# create myenv or enter existing one (to enter existing one, skip to activate step)
# python -m venv myenv
# install all packages 
# pip install -r requirements.txt
# activate 
# .\myenv\Scripts\activate
# flask run --port=8000
# http://localhost:8000/userdata to see data

from flask import Flask, jsonify, render_template, url_for, redirect
from flask_pymongo import PyMongo
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError, Email
from flask_bcrypt import Bcrypt
import uuid
import os

template_dir = os.path.abspath('../frontend/src/templates')
static_dir = os.path.abspath('../frontend/src/static')
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

app.config['MONGO_URI'] = 'mongodb+srv://gabrielaperezgil:ECE461L@cluster0.5v3hp19.mongodb.net/Existing_Users'
app.secret_key = 'secretkey'

mongo = PyMongo(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, username, email, password, userId=None):
        self.username = username
        self.email = email
        self.password = password
        self.userId = uuid.uuid4().hex if userId is None else userId
    
    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return self.userId
    
    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def get_by_userId(cls, userId):
        return cls.query.filter_by(userId=userId).first()
    
    @staticmethod
    def login_valid(username, password):
        user = User.get_by_username(username)
        if user is not None:
            return bcrypt.check_password_hash(user.password, password)
        return False
    
    @staticmethod
    def register(cls, username, email, password):
        user = cls.get_by_username(username)
        if user is None:
            new_user = cls(username, email, password)
            new_user.save_to_mongo()
            # session['email'] = email
            return True
        else:
            return False
    
    def json(self):
        return{
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "userId": self.userId
        }
    
    def save_to_mongo(self):
        mongo.db.insert(collection='userInfo', data=self.json())

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_userId(user_id)

class RegisterForm(FlaskForm):
    username = StringField('username_label', validators=[InputRequired(message="Username required"), Length(min=4, max=15, message="Username must be between 4 and 15 characters")])
    # email = StringField('email_label', validators=[InputRequired(message="Email required"), Email(message="Invalid email"), Length(max=50)])
    email = StringField('email_label')
    password = PasswordField('password_label', validators=[InputRequired(message="Password required"), Length(min=4, max=80, message="Password must be between 4 and 80 characters")])
    submit_button = SubmitField('Register')

    def validate_username(self, username):
        user_object = User.get_by_username(username.data)
        if user_object is not None:
            raise ValidationError("Username already exists. Select a different username.")
    
    # def validate_email(self, email):
    #     email_object = User.get_by_email(email.data)
    #     if email_object is not None:
    #         raise ValidationError("Email already exists.")
        
class LoginForm(FlaskForm):
    username = StringField('username_label', validators=[InputRequired(message="Username required"), Length(min=4, max=15, message="Username must be between 4 and 15 characters")])
    password = PasswordField('password_label', validators=[InputRequired(message="Password required"), Length(min=4, max=80, message="Password must be between 4 and 80 characters")])
    submit_button = SubmitField('Login')

@app.route('/')
def home():
    return render_template('dashboard.html') # change to index.html

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_object = User.get_by_username(form.username.data)
        login_user(user_object)
        return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)

@app.route('/static/login.js')
def login_js():
    return render_template('static/login.js')

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.username)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        User.register(User, form.username.data, form.email.data, hashed_password)
        return redirect(url_for('login'))
    return render_template('register.html', form=form)



# this is a simple API that returns User Information data
# this will be called by the react front end
@app.route('/userdata')

def get_data():
    collection = mongo.db.userInfo
    data = []

    for document in collection.find():
        data.append({'username is': document['userName'], 'userID is': document['userID'], 'password is': document['password']})
    return jsonify(data)

if __name__ == '__main__':
    app.run(port=8000, debug=True)
