from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, DateTimeField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
import sqlalchemy as sa
from app import db
from app.models import User
import re

class LoginForm(FlaskForm):
  username = StringField('User name', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired()])
  remember_me = BooleanField('Remember Me')
  submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
  username = StringField('User name', validators=[DataRequired()])
  email = StringField('Email', validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired()])
  password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
  submit = SubmitField('Register')

  def validate_username(self, username):
    # Check if username already exists in the database
    user = db.session.scalar(sa.select(User).where(User.username == username.data))
    if user is not None:
      raise ValidationError('Please use a different username.')
    
    # Check if username length is between 3 and 20 characters
    if len(username.data) < 3 or len(username.data) > 20:
      raise ValidationError('Username must be between 3 and 20 characters long.')

    # Check if username contains only letters and numbers
    if not re.match("^[a-zA-Z0-9]+$", username.data):
      raise ValidationError('Username can only contain letters and numbers.')

  def validate_email(self, email):
    user = db.session.scalar(sa.select(User).where(
      User.email == email.data))
    if user is not None:
      raise ValidationError('Please use a different email address.')
  
  def validate_password(self, password):
    # Validate password length and complexity
    min_length = 6
    max_length = 20
    if len(password.data) < min_length or len(password.data) > max_length:
      raise ValidationError('Password must be between 6 and 20 characters long.')
    if not any(char.isdigit() for char in password.data):
      raise ValidationError('Password must contain at least one number.')
    if not any(char.isalpha() for char in password.data):
      raise ValidationError('Password must contain at least one letter.')

  def validate_password2(self, password2):
    # Check if passwords match
    if self.password.data != password2.data:
      raise ValidationError('Passwords do not match.')

class ResetPasswordRequestForm(FlaskForm):
  email = StringField('Email', validators=[DataRequired(), Email()])
  submit = SubmitField('Send')

class ResetPasswordForm(FlaskForm):
  password = PasswordField('Password', validators=[DataRequired()])
  password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
  submit = SubmitField('Reset')

  def validate_password(self, password):
    # Validate password length and complexity
    min_length = 6
    max_length = 20
    if len(password.data) < min_length or len(password.data) > max_length:
      raise ValidationError('Password must be between 6 and 20 characters long.')
    if not any(char.isdigit() for char in password.data):
      raise ValidationError('Password must contain at least one number.')
    if not any(char.isalpha() for char in password.data):
      raise ValidationError('Password must contain at least one letter.')

  def validate_password2(self, password2):
    # Check if passwords match
    if self.password.data != password2.data:
      raise ValidationError('Passwords do not match.')

class PostForm(FlaskForm):
    title = TextAreaField('Question Title', validators=[
        DataRequired(), Length(min=1, max=140)])
    content = CKEditorField('Question Content', validators=[
        DataRequired(), Length(min=1, max=500)])
    submit = SubmitField('Post Question')
    
class EditProfileForm(FlaskForm):
  username = StringField('Username(3 to 20 characters, number or letter)', validators=[DataRequired()])
  about_me = TextAreaField('About me(140 maximum length)', validators=[Length(min=0, max=140)])
  email = StringField('Email', validators=[DataRequired(), Email()])
  submit = SubmitField('Submit')

  def __init__(self, original_username, original_email, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.original_username = original_username
    self.original_email = original_email

  def validate_username(self, username):
    if username.data != self.original_username:
      user = db.session.scalar(sa.select(User).where(User.username == self.username.data))
      if user is not None:
        raise ValidationError('Please use a different username.')

    # Check if username length is between 3 and 20 characters
    if len(username.data) < 3 or len(username.data) > 20:
      raise ValidationError('Username must be between 3 and 20 characters long.')

    # Check if username contains only letters and numbers
    if not re.match("^[a-zA-Z0-9]+$", username.data):
      raise ValidationError('Username can only contain letters and numbers.')

  def validate_email(self, email):
      if email.data != self.original_email:
        user = db.session.scalar(sa.select(User).where(User.email == email.data))
        if user is not None:
            raise ValidationError('Please use a different email.')
            
class ReplyForm(FlaskForm):
    content = CKEditorField('Reply', validators=[DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('Submit')

class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')
    
class MessageForm(FlaskForm):
    message = CKEditorField(('Message'), validators=[
        DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('Submit')

class SearchForm(FlaskForm):
    query = StringField('Search', validators=[DataRequired()])
    type = SelectField('Type', choices=[('user', 'User'), ('post', 'Post'), ('reply', 'Reply')])
    submit = SubmitField('Search')

