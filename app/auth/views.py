from flask import render_template, request, jsonify, flash, redirect, url_for, flash, session
from flask_login import login_user
from werkzeug.security import check_password_hash
from . import auth
from ..models import db, User, generate_password_hash
from flask_babel import _
from flask_login import login_user, current_user, logout_user
import os
from dotenv import load_dotenv
from .. import oauth

load_dotenv()


google = oauth.remote_app(
    'google',
    consumer_key=os.environ.get('GOOGLE_OAUTH_CLIENT_ID'),
    consumer_secret=os.environ.get('GOOGLE_OAUTH_CLIENT_SECRET'),
    request_token_params={
        'scope': 'email',
        'prompt': 'consent'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_data = request.get_json(force=True)
        email = login_data.get('email')
        password = login_data.get('password')

        user = User.query.filter_by(email=email).first()

        if not user:
            return jsonify({'success': False, 'errorType': 'incorrectEmail'}), 401

        if not check_password_hash(user.password_hash, password):
            return jsonify({'success': False, 'errorType': 'incorrectPassword'}), 401
       
        
        login_user(user)
        session['email'] = email 
        return jsonify({'success': True})

    return render_template('auth/login.html')


@auth.route('/google_login_authorized')
def google_authorized():
    resp = google.authorized_response()
    if resp is None or resp.get('access_token') is None:
        flash('Access denied: reason={0} error={1}'.format(
            request.args['error_reason'],
            request.args['error_description']
        ))
        return redirect(url_for('auth.login'))

    session['google_token'] = (resp['access_token'], '')
    user_info = google.get('userinfo')

    email = user_info.data['email']

    user = User.query.filter_by(email=email).first()

    if not user:
        flash('Veuillez créer un compte pour vous connecter', 'error')
        return redirect(url_for('auth.signup'))

    login_user(user)

    return redirect(url_for('main.user_home'))

@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')

@auth.route('/google_login')
def google_login():
    return google.authorize(callback=url_for('auth.google_authorized', _external=True))


@auth.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        SignUpData = request.get_json(force=True)
        email = SignUpData.get('email')
        password = SignUpData.get('password')
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({'success':False})
        
        new_user = User(
            email=email,
            password_hash=generate_password_hash(password)
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({'success':True})
     
    return render_template("auth/signup.html")


@auth.route('/google_signup')
def google_signup():
    return google.authorize(callback=url_for('auth.google_signup_authorized', _external=True))

@auth.route('/google_signup_authorized')
def google_signup_authorized():
    resp = google.authorized_response()
    if resp is None or resp.get('access_token') is None:
        flash('Access denied: reason={0} error={1}'.format(
            request.args['error_reason'],
            request.args['error_description']
        ))
        return redirect(url_for('auth.signup'))

    session['google_token'] = (resp['access_token'], '')
    user_info = google.get('userinfo')

    email = user_info.data['email']
    name = user_info.data.get('name', 'User')

    user = User.query.filter_by(email=email).first()
    if user:
        flash('Ce compte existe déja, veuillez vous connecter', 'error')
        return redirect(url_for('auth.login'))

    new_user = User(
        email=email, 
        first_name=name,
        last_name=name, 
        password=generate_password_hash(os.urandom(24).hex())
    )

    db.session.add(new_user)
    db.session.commit()

    login_user(new_user)
    return redirect(url_for('main.user_home'))

@auth.route("/reset_password", methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        print("This is a post request")
    
    return render_template("auth/reset_password.html")

@auth.route("/reset_email", methods=['GET', 'POST'])
def reset_email():
    if request.method == 'POST':
        print('This is a post request')
    
    return render_template("auth/reset_email.html")

@auth.route("/logout", methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('auth.login'))