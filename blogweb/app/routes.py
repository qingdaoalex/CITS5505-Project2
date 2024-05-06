from flask import render_template, flash, redirect, url_for, request, session, jsonify
from urllib.parse import urlsplit
from app import app, db, mail
from app.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm, PostForm, EditProfileForm, EmptyForm
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from app.models import User, Post
from datetime import datetime, timezone
import pytz
from app.email import send_password_reset_email
import os
import imghdr
from werkzeug.utils import secure_filename
from flask import send_from_directory

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(body=form.post.data, author=current_user)
		current_user.timestamp = datetime.now()
		db.session.add(post)
		db.session.commit()
		return redirect(url_for('index'))
	
	page = request.args.get('page', 1, type=int)
	posts = db.paginate(
        		current_user.following_posts(), 
            page=page,
						per_page=app.config['POSTS_PER_PAGE'], 
            error_out=False
          )
	next_url = url_for('index', page=posts.next_num) \
		if posts.has_next else None
	prev_url = url_for('index', page=posts.prev_num) \
		if posts.has_prev else None
	return render_template('index.html', title='Home', form=form,
													posts=posts, next_url=next_url,
													prev_url=prev_url)

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

@app.route('/delete', methods=['POST'])
@login_required
def delete_account():
	user_id = current_user.id
	user = User.query.get(user_id)
	if user:
		db.session.delete(user)
		db.session.commit()
		logout_user()  # Logout the user after deletion
		flash('Your account has been deleted successfully.')
		return redirect(url_for('index'))
	else:
		flash('User not found.')
		return redirect(url_for('index'))
    
@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	
	form = RegistrationForm()
	if form.validate_on_submit():
		# Check if username or email already exists
		existing_user = User.query.filter((User.username == form.username.data) | (User.email == form.email.data)).first()
		if existing_user:
			flash('Username or email already exists.', 'error')
			return redirect(url_for('register'))
		# Create new user
		user = User(username=form.username.data, email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Congratulations, you are now a registered user!')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)

@app.route('/check_availability', methods=['POST'])
def check_availability():
	username = request.json.get('username')
	email = request.json.get('email')
	existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
	if existing_user:
		if existing_user.username == username:
			return jsonify({'available': False, 'field': 'username'})
		else:
			return jsonify({'available': False, 'field': 'email'})
	else:
		return jsonify({'available': True})

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = ResetPasswordRequestForm()
	if form.validate_on_submit():
		user = db.session.scalar(
			sa.select(User).where(User.email == form.email.data))
		if user:
			send_password_reset_email(user)
		flash('Check your email for the instructions to reset your password')
		return redirect(url_for('login'))
	return render_template('reset-request.html',
													title='Reset Password', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	user = User.verify_reset_password_token(token)
	if not user:
		return redirect(url_for('index'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		user.set_password(form.password.data)
		db.session.commit()
		flash('Your password has been reset.')
		return redirect(url_for('login'))
	return render_template('reset.html',title='Reset Password', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    page = request.args.get('page', 1, type=int)
    # query = user.posts.select().order_by(Post.timestamp.desc())
    posts = db.paginate(current_user.following_posts(), page=page, per_page=app.config['POSTS_PER_PAGE'], error_out=False)
    next_url = url_for('user', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('user', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None
    form = EmptyForm()
    return render_template('user.html', user=user, posts=posts, next_url=next_url, prev_url=prev_url, form=form)

@app.before_request
def before_request():
	if current_user.is_authenticated:
		current_user.last_seen = datetime.now()
		db.session.commit()
        
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
	form = EditProfileForm(current_user.username, current_user.email)
	if form.validate_on_submit():
		current_user.username = form.username.data
		current_user.about_me = form.about_me.data
		current_user.email = form.email.data
		db.session.commit()
		return redirect(url_for('edit_profile'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.about_me.data = current_user.about_me
		form.email.data = current_user.email
	return render_template('edit_profile.html', title='Edit Profile', user=current_user, email=current_user.email,form=form)


@app.route('/upload_avatar', methods=['POST'])
def upload_avatar():
    user = current_user
    if 'avatar-upload' in request.files:
      file = request.files['avatar-upload']
      if file.filename != '':
        if file.content_length > app.config['MAX_FILE_SIZE_BYTES']:
          flash('File size exceeds the limit.', 'error')
          return redirect(url_for('edit_profile'))

        # Validate file type using imghdr
        allowed_image_types = {'jpg', 'jpeg', 'png', 'gif'}
        file_type = imghdr.what(file)
        if file_type not in allowed_image_types:
          flash('Invalid image file format.', 'error')
          return redirect(url_for('edit_profile'))

        # Delete the old avatar file if it exists
        if user.avatar_path:
          old_avatar_path = os.path.join(app.config['UPLOAD_PATH'], user.avatar_path)
          if os.path.exists(old_avatar_path):
            os.remove(old_avatar_path)

        filename = secure_filename(file.filename)
        avatar_directory = app.config['UPLOAD_PATH']
        if not os.path.exists(avatar_directory):
          os.makedirs(avatar_directory)  # Create the directory if it doesn't exist
        try:
          file.save(os.path.join(avatar_directory, filename))
          user.avatar_path = filename
          db.session.commit()
          flash('Avatar uploaded successfully.', 'success')
        except Exception as e:
          # Log the error
          app.logger.error("Error uploading avatar: %s", str(e))
          flash('Internal Server Error.', 'error')
    return redirect(url_for('edit_profile'))


@app.route('/set_default_avatar', methods=['POST'])
def set_default_avatar():
    user = current_user
    
    # Delete the existing avatar file if it exists
    if user.avatar_path:
        avatar_path = os.path.join(app.config['UPLOAD_PATH'], user.avatar_path)
        if os.path.exists(avatar_path):
            os.remove(avatar_path)

    # Set avatar path to NULL
    user.avatar_path = None
    db.session.commit()

    # Redirect to edit_profile page
    return redirect(url_for('edit_profile'))

@app.route('/uploaded_avatars/<filename>')
def uploaded_avatars(filename):
	return send_from_directory(app.config['UPLOAD_PATH'], filename)

@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
	form = EmptyForm()
	if form.validate_on_submit():
		user = db.session.scalar(
			sa.select(User).where(User.username == username))
		if user is None:
			flash(f'User {username} not found.')
			return redirect(url_for('index'))
		if user == current_user:
			flash('You cannot follow yourself!')
			return redirect(url_for('user', username=username))
		current_user.follow(user)
		db.session.commit()
		flash(f'You are following {username}!')
		return redirect(url_for('user', username=username))
	else:
		return redirect(url_for('index'))


@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
	form = EmptyForm()
	if form.validate_on_submit():
		user = db.session.scalar(
			sa.select(User).where(User.username == username))
		if user is None:
			flash(f'User {username} not found.')
			return redirect(url_for('index'))
		if user == current_user:
			flash('You cannot unfollow yourself!')
			return redirect(url_for('user', username=username))
		current_user.unfollow(user)
		db.session.commit()
		flash(f'You are not following {username}.')
		return redirect(url_for('user', username=username))
	else:
		return redirect(url_for('index'))
