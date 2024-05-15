from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import app, db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from hashlib import md5
import pytz
from time import time
import jwt
from flask import url_for
import json
from time import time


followers = sa.Table(
  'followers',
  db.metadata,
  sa.Column('follower_id', sa.Integer, sa.ForeignKey('user.id'),
            primary_key=True),
  sa.Column('followed_id', sa.Integer, sa.ForeignKey('user.id'),
            primary_key=True)
)
class User(UserMixin, db.Model):
  id: so.Mapped[int] = so.mapped_column(primary_key=True)
  username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,unique=True)
  email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
  password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
  avatar_path: so.Mapped[str] = so.mapped_column(sa.String(256), nullable = True)
  notifications: so.WriteOnlyMapped['Notification'] = so.relationship(
        back_populates='user', passive_deletes=True)

  posts: so.WriteOnlyMapped['Post'] = so.relationship("Post",
    back_populates='author', lazy='dynamic', passive_deletes=True,cascade='all, delete-orphan')
   ###replies
  replies: so.Mapped[list['Reply']] = so.relationship("Reply", back_populates="user",lazy='dynamic', cascade='all, delete-orphan', passive_deletes=True)
    ##
  about_me: so.Mapped[Optional[str]] = so.mapped_column(sa.String(140))
  last_seen: so.Mapped[Optional[datetime]] = so.mapped_column(
    default=lambda: datetime.now())
  last_message_read_time: so.Mapped[Optional[datetime]]
  
  following: so.WriteOnlyMapped['User'] = so.relationship(
    secondary=followers, primaryjoin=(followers.c.follower_id == id),
    secondaryjoin=(followers.c.followed_id == id),
    back_populates='followers', passive_deletes=True, cascade='all')
  followers: so.WriteOnlyMapped['User'] = so.relationship(
    secondary=followers, primaryjoin=(followers.c.followed_id == id),
    secondaryjoin=(followers.c.follower_id == id),
    back_populates='following', passive_deletes=True, cascade='all')
  messages_sent: so.WriteOnlyMapped['Message'] = so.relationship( foreign_keys='Message.sender_id', back_populates='author', passive_deletes=True)
  messages_received: so.WriteOnlyMapped['Message'] = so.relationship( foreign_keys='Message.recipient_id', back_populates='recipient', passive_deletes=True)

  def __repr__(self):
    return '<User {}>'.format(self.username)
  
  def set_password(self, password):
    self.password_hash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password_hash, password)
  
  def get_reset_password_token(self, expires_in=600):
    return jwt.encode(
      {'reset_password': self.id, 'exp': time() + expires_in},
      app.config['SECRET_KEY'], algorithm='HS256')

  def unread_message_count(self):
    last_read_time = self.last_message_read_time or datetime(1900, 1, 1)
    query = sa.select(Message).where(Message.recipient == self, Message.timestamp > last_read_time)
    return db.session.scalar(sa.select(sa.func.count()).select_from(query.subquery()))
  
  @staticmethod
  def verify_reset_password_token(token):
    try:
        id = jwt.decode(token, app.config['SECRET_KEY'],
                        algorithms=['HS256'])['reset_password']
    except:
        return
    return db.session.get(User, id)
  
  def avatar(self, size):
    if self.avatar_path:
        return url_for('uploaded_avatars', filename=self.avatar_path)
    else:
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'
  
  def follow(self, user):
    if not self.is_following(user):
        self.following.add(user)

  def unfollow(self, user):
    if self.is_following(user):
        self.following.remove(user)

  def is_following(self, user):
    query = self.following.select().where(User.id == user.id)
    return db.session.scalar(query) is not None

  def followers_count(self):
    query = sa.select(sa.func.count()).select_from(
      self.followers.select().subquery())
    return db.session.scalar(query)

  def following_count(self):
    query = sa.select(sa.func.count()).select_from(
      self.following.select().subquery())
    return db.session.scalar(query)
  
# Only followed user posts without current user's posts
  def following_posts_only(self):
    Author = so.aliased(User)
    Follower = so.aliased(User)
    return (
      sa.select(Post)
      .join(Post.author.of_type(Author))
      .join(Author.followers.of_type(Follower), isouter=True)
      .where(sa.or_(
        Follower.id == self.id,
      ))
      .group_by(Post)
      .order_by(Post.timestamp.desc())
    )
  
# User's own posts with followed user posts.
  def following_posts(self):
    Author = so.aliased(User)
    Follower = so.aliased(User)
    return (
      sa.select(Post)
      .join(Post.author.of_type(Author))
      .join(Author.followers.of_type(Follower), isouter=True)
      .where(sa.or_(
        Follower.id == self.id,
        Author.id == self.id,
      ))
      .group_by(Post)
      .order_by(Post.timestamp.desc())
    )
    
  def add_notification(self, name, data):
        db.session.execute(self.notifications.delete().where(Notification.name == name))
        n = Notification(name=name, payload_json=json.dumps(data), user=self)
        db.session.add(n)
        return n
  


class Post(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(140))
    content: so.Mapped[str] = so.mapped_column(sa.Text, nullable=False)
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now())
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    author: so.Mapped[User] = so.relationship(back_populates='posts')
    replies: so.WriteOnlyMapped['Reply'] = so.relationship('Reply', back_populates='post', cascade='all, delete-orphan')
    def __repr__(self):
        return '<Post {}>'.format(self.tktle)
    ###function to count number of replies
    def replies_count(self):
        return db.session.query(sa.func.count(Reply.id)).filter(Reply.post_id == self.id).scalar()
    
################### changes for reply function
class Reply(db.Model):
    __tablename__ = 'reply'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    content: so.Mapped[str] = so.mapped_column(sa.Text, nullable=False)
    timestamp: so.Mapped[datetime] = so.mapped_column(sa.DateTime, default=lambda: datetime.now())
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user.id', ondelete='CASCADE'))
    post_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('post.id', ondelete='CASCADE'))

    user: so.Mapped['User'] = so.relationship('User', back_populates='replies')
    post: so.Mapped['Post'] = so.relationship('Post', back_populates='replies')

    def __repr__(self):
        return f'<Reply {self.id}>'
#########################
    
    
    
@login.user_loader
def load_user(id):
  return db.session.get(User, int(id))

class Message(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    sender_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    recipient_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    body: so.Mapped[str] = so.mapped_column(sa.String(140))
    timestamp: so.Mapped[datetime] = so.mapped_column( index=True, default=lambda: datetime.now())
    author: so.Mapped[User] = so.relationship( foreign_keys='Message.sender_id', back_populates='messages_sent')
    recipient: so.Mapped[User] = so.relationship( foreign_keys='Message.recipient_id', back_populates='messages_received')

    def __repr__(self):
        return '<Message {}>'.format(self.body)
      
class Notification(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(128), index=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    timestamp: so.Mapped[float] = so.mapped_column(index=True, default=time)
    payload_json: so.Mapped[str] = so.mapped_column(sa.Text)

    user: so.Mapped[User] = so.relationship(back_populates='notifications')

    def get_data(self):
        return json.loads(str(self.payload_json))
