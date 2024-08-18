from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import  generate_password_hash, check_password_hash

from models import db, User, Sponsor, Influencer

from app import app

def auth_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if 'user_id' in session:
            result = func(*args, **kwargs)
            return result
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return inner
    
@app.route('/')
@auth_required
def index():
    return render_template('index.html', user = User.query.get(session['user_id']))

@app.route('/profile')
@auth_required
def profile():
    return render_template('profile.html', user = User.query.get(session['user_id']))

@app.route('/profile', methods=['POST'])
@auth_required
def profile_post():
    username = request.form.get('username')
    name = request.form.get('name')
    password = request.form.get('password')
    cpassword = request.form.get('cpassword')

    if username == '' or password == '' or cpassword == '' :
        flash('Username or password cannot be empty.')
        return redirect(url_for('profile'))
    
    
    user = User.query.get(session['user_id'])
    
    if not check_password_hash(user.password_hash, cpassword):
        flash('Incorrect password.')
        return redirect(url_for('profile'))
    
    if username != user.username :
        new_username = User.query.filter_by(username = username).first()
        if new_username :
            flash('Username already exists.')
            return redirect(url_for('profile'))
    
    new_password_hash = generate_password_hash(password)
    user.username = username
    user.name = name
    user.password_hash = new_password_hash
    db.session.commit()
    flash('Profile updated successfully.')
    return redirect(url_for('profile'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    if username == '' or password == '':
        flash('Username or password cannot be empty.')
        return redirect(url_for('login'))
    user = User.query.filter_by(username=username).first()
    if not user:
        flash('User does not exist.')
        return redirect(url_for('login'))
    if not user.check_password(password):
        flash('Incorrect password.')
        return redirect(url_for('login'))
    #Login Sucsessful
    session['user_id'] = user.id
    return redirect(url_for('index'))

@app.route('/Sponsor_Registration')
def Sponsor_Registration():
    return render_template('Sponsor_Registration.html')

@app.route('/Sponsor_Registration', methods=['POST'])
def Sponsor_Registration_post():
    username = request.form.get('username')
    name = request.form.get('name')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    industry = request.form.get('industry')
    if username == '' or password == '':
        flash('Username or password cannot be empty.')
        return redirect(url_for('Sponsor_Registration'))
    if industry == '':
        flash('Industry cannot be empty.')
        return redirect(url_for('Sponsor_Registration'))
    if password != confirm_password:
        flash('Passwords do not match.')
        return redirect(url_for('Sponsor_Registration'))
    if User.query.filter_by(username=username).first():
        flash('User with this username already exists. Please choose some other username')
        return redirect(url_for('Sponsor_Registration'))
    user = User(username=username,name=name, password=password)
    db.session.add(user)
    db.session.commit()
    flash('User successfully registered.')
    return redirect(url_for('login'))

@app.route('/Influencer_Registration')
def Influencer_Registration():
    return render_template('Influencer_Registration.html')

@app.route('/Influencer_Registration', methods=['POST'])
def Influencer_Registration_post():
    username = request.form.get('username')
    name = request.form.get('name')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    if username == '' or password == '':
        flash('Username or password cannot be empty.')
        return redirect(url_for('Influencer_Registration'))
    if password != confirm_password:
        flash('Passwords do not match.')
        return redirect(url_for('Influencer_Registration'))
    if User.query.filter_by(username=username).first():
        flash('User with this username already exists. Please choose some other username')
        return redirect(url_for('Influencer_Registration'))
    user = User(username=username,name=name, password=password)
    db.session.add(user)
    db.session.commit()
    flash('User successfully registered.')
    return redirect(url_for('login'))

@app.route('/logout')
@auth_required
def logout():
    session.pop('user_id')
    return redirect(url_for('login'))
