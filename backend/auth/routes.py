from flask import Flask, Blueprint, render_template, redirect, request, flash, url_for, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from models.models import db, User
import os
from .recommend_routes import recommend_bp  # This route for topic recommendation feature


auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['POST'])
def register_user():
    data = request.json
    new_user = User(**data)
    new_user.save()
    return jsonify({"message": "User registered successfully."}), 201

# Route to register the recommendation feature
def register_routes(app):
    app.register_blueprint(auth)  
    app.register_blueprint(recommend_bp, url_prefix='/api')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash('Incorrect email or password')
            return redirect(url_for('auth.login'))

        login_user(user)
        return redirect(url_for('index'))

    return render_template('login.html')


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        hashed_pw = generate_password_hash(password)

        if User.query.filter_by(email=email).first():
            flash('Email already exists.')
            return redirect(url_for('auth.signup'))

        user = User(email=email, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Account created! Please log in.')
        return redirect(url_for('auth.login'))

    return render_template('signup.html')



@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')


##  For the admin
@auth.route('/admin-dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:  # Make sure this flag exists in User model
        return redirect('/')
    return render_template('admin_dashboard.html')

