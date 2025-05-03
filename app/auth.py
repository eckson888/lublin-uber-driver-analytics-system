from app.model import User
from app.app import db
from flask import Blueprint, render_template
from werkzeug.security import check_password_hash, generate_password_hash
from flask import request, redirect, url_for, render_template, flash
from flask_login import login_user, logout_user, login_required


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = db.session.query(User).filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('main.home'))
        flash('Invalid credentials')
    return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_exists = db.session.query(db.session.query(User).filter_by(username=request.form['username']).exists()).scalar()
        if user_exists:
            flash("Login taken")
            return redirect(url_for('auth.login'))
        username = request.form['username']
        password = generate_password_hash(request.form['password'], method="scrypt")
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash("Registered Successfully!")
        return redirect(url_for('auth.login'))
    return render_template('register.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))



# @auth.route('/add', methods=['GET', 'POST'])
# def add():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']       

#         hashed_password = generate_password_hash(password, method='scrypt')

#         new_user = User(username=username, password=hashed_password)
#         db.session.add(new_user)
#         db.session.commit()

#         flash('User added successfully!', 'success')
#         return redirect(url_for('main.explore_plots'))  # Assuming you have an 'explore' route
#     return render_template('add.html')