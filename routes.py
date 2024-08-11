from flask import Flask, render_template, request, redirect, url_for, flash

from models import db, User, Sponsor, Influencer, Campaign, AdRequest

from app import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    if username == '' or password == '':
        flash('Username or password cannot be empty.')
    user = User.query.filter_by(username=username).first()
    if not user:
        flash('User does not exist.')
        return redirect(url_for('login'))
    if not user.check_password(password):
        flash('Incorrect password.')
        return redirect(url_for('login'))
    #Login Sucsessful
    return redirect(url_for('index'))

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register_post():
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    role = request.form.get('role')
    if username == '' or password == '':
        flash('Username or password cannot be empty.')
        return redirect(url_for('register'))
    if password != confirm_password:
        flash('Passwords do not match.')
        return redirect(url_for('register'))
    if User.query.filter_by(username=username).first():
        flash('User with this username already exists. Please choose some other username')
        return redirect(url_for('register'))
    user = User(username=username, password=password, role=role)
    db.session.add(user)
    db.session.commit()
    flash('User successfully registered.')
    return redirect(url_for('login'))

