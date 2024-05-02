from flask_wtf import FlaskForm
from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5
from app import db, login

class User(UserMixin, db.Model):
    # For a AddressAndPhone model class, the table would be named address_and_phone. If you prefer to choose your own table names, you can add an attribute named __tablename__ to the model class, set to the desired name as a string.
    # __tablename__ = 'my_custom_table_name'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    posts: so.WriteOnlyMapped['Post'] = so.relationship(back_populates='author')
    # The User class has a new posts field, that is initialized with so.relationship(). 
    # This is not an actual database field, but a high-level view of the relationship between 
    # users and posts, and for that reason it isn't in the database diagram. 
    # Likewise, the Post class has an author field that is also initialized as a relationship. 
    # These two attributes allow the application to access the connected user and post entries.

    about_me: so.Mapped[Optional[str]] = so.mapped_column(sa.String(140))
    last_seen: so.Mapped[Optional[datetime]] = so.mapped_column(default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return '<User {}>'.format(self.username)
#     >>> from app.models import User
# >>> u = User(username='susan', email='susan@example.com')
# >>> u
# <User susan>

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

class Post(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    body: so.Mapped[str] = so.mapped_column(sa.String(140))
    timestamp: so.Mapped[datetime] = so.mapped_column( index=True, default=lambda: datetime.now(timezone.utc))
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    # The user_id field was initialized as a foreign key to User.id, which means that it references values from the id column in the users table.

    author: so.Mapped[User] = so.relationship(back_populates='posts')
    

    def __repr__(self):
        return '<Post {}>'.format(self.body)