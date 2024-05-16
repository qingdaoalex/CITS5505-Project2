from flask import render_template, flash, redirect, url_for, request, session, jsonify, current_app, send_from_directory
from urllib.parse import urlsplit
from app import db
from app.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm, PostForm, EditProfileForm, EmptyForm, MessageForm, ReplyForm, SearchForm
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from app.models import User, Post, Message, Notification, Reply
from datetime import datetime, timezone
import pytz
from app.email import send_password_reset_email
import os
import imghdr
from werkzeug.utils import secure_filename
import uuid
from sqlalchemy import or_

from app.blueprints import main
from config import DeploymentConfig
config = DeploymentConfig

@main.route('/', methods=['GET', 'POST'])
def welcome():
	return render_template('welcome.html')

@main.route('/references', methods=['GET'])
def references():
	return render_template('references.html')

@main.route('/index', methods=['GET', 'POST'])
@login_required
def index():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(title=form.title.data, content=form.content.data, author=current_user)
		current_user.timestamp = datetime.now()
		db.session.add(post)
		db.session.commit()
		return redirect(url_for('main.index'))
	search_form = SearchForm()
	page = request.args.get('page', 1, type=int)
	all_post_query = sa.select(Post).order_by(Post.timestamp.desc())
	all_posts = db.paginate(all_post_query, per_page=config['POSTS_PER_PAGE'], error_out=False)
	follow_posts = db.paginate(current_user.following_posts_only(),
													 per_page=config['POSTS_PER_PAGE'], error_out=False)
	next_url_all = url_for('main.index', page=all_posts.next_num) \
		if all_posts.has_next else None
	prev_url_all = url_for('main.index', page=all_posts.prev_num) \
		if all_posts.has_prev else None
	next_url_follow = url_for('main.index', page=follow_posts.next_num) \
		if all_posts.has_next else None
	prev_url_follow = url_for('main.index', page=follow_posts.prev_num) \
		if all_posts.has_prev else None
	
	return render_template('index.html', title='Home', form=form,
    all_posts=all_posts, follow_posts=follow_posts,
		next_url_all=next_url_all, prev_url_all=prev_url_all,
		prev_url_follow=prev_url_follow, next_url_follow=next_url_follow, 
		search_form=search_form)

@main.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('main.index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = db.session.scalar(
			sa.select(User).where(User.username == form.username.data))
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('main.login'))
		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or urlsplit(next_page).netloc != '':
			next_page = session.get('next_page')
			session.pop('next_page', None)  # Clear next_page from session
			if not next_page:
				next_page = url_for('main.index')
		return redirect(next_page)
	# Store the next_page in session before rendering login template
	session['next_page'] = request.args.get('next')
	return render_template('login.html', title='Sign In', form=form)

@main.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@main.route('/delete', methods=['POST'])
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
    
@main.route('/register', methods=['GET', 'POST'])
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

@main.route('/check_availability', methods=['POST'])
def check_availability():
	username = request.json.get('username')
	email = request.json.get('email')
	existing_user = User.query.filter((User.username == username) | (User.email == email)).first()

	if existing_user:
		# Check if the existing user's username matches the input username
		if existing_user.username == username:
			# If the input username matches the current user's username, return available
			if current_user.is_authenticated and current_user.username == username:
				username_available = True
			else:
				username_available = False
		else:
			username_available = True

		# Check if the existing user's email matches the input email
		if existing_user.email == email:
			# If the input email matches the current user's email, return available
			if current_user.is_authenticated and current_user.email == email:
				email_available = True
			else:
				email_available = False
		else:
			email_available = True

		return jsonify({'username_available': username_available, 'email_available': email_available})
	else:
		return jsonify({'username_available': True, 'email_available': True})

@main.route('/reset_password_request', methods=['GET', 'POST'])
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

@main.route('/reset_password/<token>', methods=['GET', 'POST'])
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

@main.route('/user/<username>')
@login_required
def user(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    page = request.args.get('page', 1, type=int)
    query = user.posts.select().order_by(Post.timestamp.desc())
    posts = db.paginate(query, page=page, per_page=config['POSTS_PER_PAGE'], error_out=False)
    next_url = url_for('user', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('user', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None
    form = EmptyForm()
    return render_template('user.html', user=user, posts=posts, next_url=next_url, prev_url=prev_url, form=form)

@main.route('/user/<username>/popup')
@login_required
def user_popup(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    form = EmptyForm()
    return render_template('user_popup.html', user=user, form=form)

@main.before_request
def before_request():
	if current_user.is_authenticated:
		current_user.last_seen = datetime.now()
		db.session.commit()
        
@main.route('/edit_profile', methods=['GET', 'POST'])
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


@main.route('/upload_avatar', methods=['POST'])
def upload_avatar():
    user = current_user
    if 'avatar-upload' in request.files:
      file = request.files['avatar-upload']
      if file.filename != '':
        if file.content_length > config['MAX_FILE_SIZE_BYTES']:
          flash('File size exceeds the limit.', 'error')
          return redirect(url_for('edit_profile'))

        # Validate file type using imghdr
        allowed_image_types = {'jpg', 'jpeg', 'png', 'gif'}
        file_type = imghdr.what(file)
        if file_type not in allowed_image_types:
          flash('Invalid image file format.', 'error')
          return redirect(url_for('edit_profile'))

        # Generate a unique filename
        unique_filename = str(uuid.uuid4()) + '_' + secure_filename(file.filename)

        # Delete the old avatar file if it exists
        if user.avatar_path:
          old_avatar_path = os.path.join(config['UPLOAD_PATH'], user.avatar_path)
          if os.path.exists(old_avatar_path):
            os.remove(old_avatar_path)

        avatar_directory = config['UPLOAD_PATH']
        if not os.path.exists(avatar_directory):
          os.makedirs(avatar_directory)  # Create the directory if it doesn't exist
        try:
          file.save(os.path.join(avatar_directory, unique_filename))
          user.avatar_path = unique_filename
          db.session.commit()
          flash('Avatar uploaded successfully.', 'success')
        except Exception as e:
          # Log the error
          logger.error("Error uploading avatar: %s", str(e))
          flash('Internal Server Error.', 'error')
    return redirect(url_for('edit_profile'))


@main.route('/set_default_avatar', methods=['POST'])
def set_default_avatar():
    user = current_user
    
    # Delete the existing avatar file if it exists
    if user.avatar_path:
        avatar_path = os.path.join(config['UPLOAD_PATH'], user.avatar_path)
        if os.path.exists(avatar_path):
            os.remove(avatar_path)

    # Set avatar path to NULL
    user.avatar_path = None
    db.session.commit()

    # Redirect to edit_profile page
    return redirect(url_for('edit_profile'))

@main.route('/uploaded_avatars/<filename>')
def uploaded_avatars(filename):
	return send_from_directory(config['UPLOAD_PATH'], filename)

@main.route('/follow/<username>', methods=['POST'])
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


@main.route('/unfollow/<username>', methods=['POST'])
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

@main.route('/send_message/<recipient>', methods=['GET', 'POST'])
@login_required
def send_message(recipient):
    user = db.first_or_404(sa.select(User).where(User.username == recipient))
    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(author=current_user, recipient=user,body=form.message.data)
        db.session.add(msg)
        user.add_notification('unread_message_count',user.unread_message_count())
        db.session.commit()
        return redirect(url_for('user', username=recipient))
    return render_template('send_message.html', title=('Send Message'),form=form, recipient=recipient)
  
@main.route('/messages')
@login_required
def messages():
    current_user.last_message_read_time = datetime.now()
    current_user.add_notification('unread_message_count', 0)
    db.session.commit()
    page = request.args.get('page', 1, type=int)
    query = current_user.messages_received.select().order_by(Message.timestamp.desc())
    messages = db.paginate(query, page=page,per_page=current_config['POSTS_PER_PAGE'],error_out=False)
    next_url = url_for('messages', page=messages.next_num) \
        if messages.has_next else None
    prev_url = url_for('messages', page=messages.prev_num) \
        if messages.has_prev else None
    return render_template('messages.html',messages=messages,next_url=next_url, prev_url=prev_url)
  
@main.route('/notifications')
@login_required
def notifications():
    since = request.args.get('since', 0.0, type=float)
    query = current_user.notifications.select().where(
        Notification.timestamp > since).order_by(Notification.timestamp.asc())
    notifications = db.session.scalars(query)
    return [{
        'name': n.name,
        'data': n.get_data(),
        'timestamp': n.timestamp
    } for n in notifications]

@main.route('/post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    replies_query = Reply.query.filter_by(post_id=post.id).order_by(Reply.timestamp.desc())
    replies = replies_query.all()  # Execute the query to fetch replies
    reply_form = ReplyForm()
    print("******replies*******", replies)
    print("******replies_query*******", replies_query)

    page = request.args.get('page', 1, type=int)
    reply_post = db.paginate(replies_query, per_page=config['POSTS_PER_PAGE'], error_out=False)
    next_url_reply = url_for('/post/<int:post_id>', page=reply_post.next_num) \
      if reply_post.has_next else None
    prev_url_reply = url_for('/post/<int:post_id>', page=reply_post.prev_num) \
		if reply_post.has_prev else None

    if reply_form.validate_on_submit():
        reply = Reply(content=reply_form.content.data, user=current_user, post=post)
        db.session.add(reply)
        db.session.commit()
        return redirect(url_for('post_detail', post_id=post.id))

    return render_template('post_detail.html', title=post.title, post=post, replies=replies, reply_post=reply_post,
				reply_form=reply_form,	next_url_reply=next_url_reply, prev_url_reply=prev_url_reply,)

@main.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(url_for('search_results', query=form.query.data, type=form.type.data))
    return render_template('index.html', form=form)

@main.route('/search_results')
def search_results():
    query = request.args.get('query', '', type=str)
    search_type = request.args.get('type', 'post', type=str)

    if search_type == 'user':
        results = db.session.scalars(sa.select(User).where(User.username.contains(query))).all()
    elif search_type == 'post':
        results = db.session.scalars(sa.select(Post).where(
            or_(Post.title.contains(query), Post.content.contains(query))
        )).all()
    elif search_type == 'reply':
        results = db.session.execute(
            sa.select(Reply, Post.title, Post.id)
            .join(Post, Post.id == Reply.post_id)
            .where(Reply.content.contains(query))
        ).all()
    else:
        results = []

    return render_template('search_results.html', results=results, search_type=search_type)


@main.route('/delete_reply/<int:reply_id>', methods=['POST'])
@login_required
def delete_reply(reply_id):
    reply = Reply.query.get_or_404(reply_id)
    db.session.delete(reply)
    db.session.commit()
    return redirect(url_for('post_detail', post_id=reply.post_id))

