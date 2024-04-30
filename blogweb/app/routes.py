from flask import render_template, flash, redirect, url_for, request, session
from urllib.parse import urlsplit
from app import app, db
from app.forms import LoginForm, RegistrationForm, PostForm
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from app.models import User, Post
from datetime import datetime
import pytz
import logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('index'))
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template("index.html", title='Home Page', form=form,
                           posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = session.get('next_page')
            session.pop('next_page', None)  # Clear next_page from session
            if not next_page:
                next_page = url_for('index')
        return redirect(next_page)
    # Store the next_page in session before rendering login template
    session['next_page'] = request.args.get('next')
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            logging.info('User registered successfully.')
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('login'))
        except Exception as e:
            logging.error(f'Error registering user: {str(e)}')
            db.session.rollback()
            flash('An error occurred while registering. Please try again later.', 'error')
    
    # Log if form validation fails or if the request method is not POST
    if form.errors:
        logging.error(f'Form validation failed: {form.errors}')
    elif request.method != 'POST':
        logging.info('Register page loaded (GET request).')
    else:
        logging.warning('Unknown error occurred during registration.')
    
    return render_template('register.html', title='Register', form=form)

@app.route('/reset', methods=['GET', 'POST'])
def reset():
    return render_template('reset.html', title="Reset Password")

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.route('/user/<username>')
@login_required
def user(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)