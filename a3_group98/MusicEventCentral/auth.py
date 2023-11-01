from flask import Blueprint, render_template, redirect, url_for, flash
from .forms import LoginForm, RegisterForm
from flask_login import login_user, login_required, logout_user
from flask_bcrypt import generate_password_hash, check_password_hash
from .models import User
from . import db

authbp = Blueprint('auth', __name__)

@authbp.route('/register', methods=['GET', 'POST'])
def register():
    register = RegisterForm()

    if register.validate_on_submit():
        uname = register.user_name.data
        pwd = register.password.data
        email = register.email_id.data
        phone = register.phone_id.data

        user = db.session.scalar(db.select(User).where(User.name == uname))

        if user:
            flash('Username already exists, please try another', 'error')
            return redirect(url_for('auth.register'))

        try:
            pwd_hash = generate_password_hash(pwd)
            new_user = User(name=uname, password_hash=pwd_hash, emailid=email, phoneid=phone)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('main.index'))
        except Exception as e:
            flash('An error occurred during registration. Please try again later.', 'error')
            # Handle the error, e.g., log it and return an error response

    return render_template('user.html', form=register, heading='Register')

@authbp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        user_name = login_form.user_name.data
        password = login_form.password.data
        user = db.session.scalar(db.select(User).where(User.name == user_name))

        if user is None or not check_password_hash(user.password_hash, password):
            flash('Incorrect username or password', 'error')
        else:
            login_user(user)
            return redirect(url_for('main.index'))

    return render_template('user.html', form=login_form, heading='Login')

@authbp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
