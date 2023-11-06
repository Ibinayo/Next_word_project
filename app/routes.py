#!/usr/bin/env python3
"""Routes for user authentication"""

from app import app
from flask import redirect, render_template, flash, Blueprint, request, url_for, Response
from flask_login import login_required, login_user, logout_user, current_user
from app.forms import *


@app.route('/', methods=['GET'])
def index():
    """index page for app"""
    return render_template('index.html')

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET'])
def contact():
    return render_template('contact.html')

@app.route('/sign-in', methods=['GET', 'POST'])
def sign_in():
    """Route for signing in to the app"""
    form = SignInForm()
    if form.validate_on_submit():
        username = form.username.data.rstrip()
        user = User.query.filter_by(username=username).first()
        if user is not None:
            if check_password_hash(user.password_hash, form.password.data.rstrip()):
                login_user(user)
                return redirect(url_for('home', username=user.username.rstrip()))
            else:
                flash('Password is incorrect. Please try again.')
        else:
            flash('Username does not exist. Please try again.')
    return render_template('index.html', sign_form=form, sign_in=True)

@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    """Route for signing up to the app"""
    form = SignUpForm()
    if form.validate_on_submit():
        username = form.username.data.rstrip()
        email = form.email.data.rstrip()
        user = User(username=username, email=email)
        user.set_password_hash(form.password.data.rstrip())
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('sign_in'))
    return render_template('index.html', sign_form=form, sign_up=True)

@app.route('/<username>/profile', methods=['GET', 'POST'])
@login_required
def profile(username):
    """Route function to user profile"""
    if username != current_user.username:
        return redirect(url_for('index'))
    user = User.query.get(current_user.id)
    if request.args.get('act') == 'edit':
        form = EditDetails()
        if form.validate_on_submit():
            user.username = form.username.data.rstrip()
            user.email = form.email.data.rstrip()
            db.session.commit()
            return redirect(url_for('profile', username=current_user.username.rstrip(), act='edit'))
    elif request.args.get('act') == 'change':
        form = EditPassword()
        if form.validate_on_submit():
            user.set_password_hash(form.new_password.data.rstrip())
            db.session.commit()
            return redirect(url_for('profile', username=current_user.username.rstrip(), act='change'))
    elif request.args.get('act') == 'delete':
        form = DeleteAccount()
        if form.validate_on_submit():
            if check_password_hash(user.password_hash, form.password.data.rstrip()):
                db.session.delete(user)
                db.session.commit()
                return redirect(url_for('index'))
    return render_template('profile.html', username=username, form=form, user=current_user, act=request.args.get('act'))


@app.route('/<username>/home', methods=['GET'])
@login_required
def home(username):
    if username != current_user.username:
        return redirect(url_for('index'))
    return render_template('home.html', username=username)

@app.route('/sign-out', methods=['GET'])
@login_required
def sign_out():
    """Route for signing out of the app"""
    logout_user()
    return redirect(url_for('index'))