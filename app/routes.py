#!/usr/bin/env python3
"""Routes for user authentication"""


from app import app
from flask import redirect, render_template, flash, request
from flask import url_for, Response, json, jsonify
from flask_login import login_required, login_user, logout_user, current_user
from app.forms import *
import re


import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import json
import os


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
            if check_password_hash(user.password_hash,
                                   form.password.data.rstrip()):
                login_user(user)
                return redirect(url_for('home',
                                        username=user.username.rstrip()))
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
            return redirect(url_for('profile',
                                    username=current_user.username.rstrip(),
                                    act='edit'))
    elif request.args.get('act') == 'change':
        form = EditPassword()
        if form.validate_on_submit():
            user.set_password_hash(form.new_password.data.rstrip())
            db.session.commit()
            return redirect(url_for('profile',
                                    username=current_user.username.rstrip(),
                                    act='change'))
    elif request.args.get('act') == 'delete':
        form = DeleteAccount()
        if form.validate_on_submit():
            if check_password_hash(user.password_hash,
                                   form.password.data.rstrip()):
                db.session.delete(user)
                db.session.commit()
                return redirect(url_for('index'))
    return render_template('profile.html', username=username,
                           form=form, user=current_user,
                           act=request.args.get('act'))


@app.route('/<username>/home', methods=['GET'])
@login_required
def home(username):
    """Route function to user home page"""
    if username != current_user.username:
        return redirect(url_for('index'))
    return render_template('home.html', username=username)


@app.route('/sign-out', methods=['GET'])
@login_required
def sign_out():
    """Route for signing out of the app"""
    logout_user()
    return redirect(url_for('index'))


@app.route('/input', methods=['GET', 'POST'])
@login_required
def input():
    """Input functon to store user inputs in the database"""
    if request.method == 'POST':
        data = request.get_json()
        in_put = data['input']
        user_id = current_user.id
        inputs = re.split("[,.?\\-!]", in_put)
        for input in inputs:
            input = Input(input=input, user_id=user_id)
            db.session.add(input)
            db.session.commit()
        return Response(status=200)
    else:
        data = Input.query.filter_by(user_id=current_user.id).all()
        inputs = [datum.input for datum in data]
        return json.dumps(inputs)


# File paths
text_file_path = 'trim.txt'
model_path = 'model2.h5'

with open(text_file_path, 'r', encoding='utf-8') as myfile:
    text = myfile.read()

new_tokenizer = Tokenizer()
new_tokenizer.fit_on_texts([text])

loaded_model = load_model(model_path)

# Max sequence length
max_sequence_len = 67


def predict_next_words(input_text, predict_next_words):
    """Prdeict the next words"""
    token_list = new_tokenizer.texts_to_sequences([input_text])[0]
    token_list = pad_sequences([token_list], maxlen=max_sequence_len - 1,
                               padding='pre')

    # Ensure the correct input shape
    token_list = np.reshape(token_list, (1, max_sequence_len - 1))

    predicted_words = []
    for _ in range(predict_next_words):
        predicted_index = np.argmax(loaded_model.predict(token_list), axis=-1)
        output_word = ""
        for word, index in new_tokenizer.word_index.items():
            if index == predicted_index:
                output_word = word
                break
        input_text += " " + output_word
        predicted_words.append(output_word)
        # Update the token_list for the next iteration
        token_list = np.append(token_list[0, 1:], [predicted_index])
        token_list = np.reshape(token_list, (1, max_sequence_len - 1))

    return predicted_words


@app.route('/predict', methods=['POST', 'GET'])
def predict():
    """Route function to predict the next word"""
    if not loaded_model:
        return jsonify({'error': 'Model not found.'})
    data = request.get_json()
    input_text = data.get('inputs')
    predicted_num = int(data.get('num'))
    predicted_words = predict_next_words(input_text, predicted_num)
    return jsonify(predicted_words)
