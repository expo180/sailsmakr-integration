from flask import render_template, request, jsonify, flash, redirect, url_for, flash, session
from flask_login import login_user
from werkzeug.security import check_password_hash
from . import auth
from ..models import db, User, generate_password_hash
from flask_babel import _
from flask_login import login_user, current_user

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
    flash(_('Veuillez vous connecter à votre compte!'),'error')
    return redirect(url_for('auth.login'))