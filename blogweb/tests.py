import os
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
import sys
from microblog import app
from datetime import datetime, timezone, timedelta
import unittest
from app import db
from app.models import User, Post, Reply, Message, Notification
from app.routes import check_availability
import hashlib
import sqlalchemy as sa

class BaseModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()  # Set up the test client
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()
        self.populate_dummy_data()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def populate_dummy_data(self):
        self.user1 = User(username='john', email='john@example.com')
        self.user2 = User(username='susan', email='susan@example.com')
        self.user3 = User(username='mary', email='mary@example.com')
        self.user4 = User(username='david', email='david@example.com')
        db.session.add_all([self.user1, self.user2, self.user3, self.user4])
        db.session.commit()


class UserModelCase(BaseModelTestCase):
    def test_check_no_user_availability(self):
        data = {'username': 'john', 'email': 'john@example.com'}
        print(data, "data*******************")
        # Make a POST request to the check_availability route
        response = self.app.post('/check_availability', json=data)
        expected_result = {'username_available': False, 'email_available': False}
        self.assertEqual(response.get_json(), expected_result)

    def test_check_user_availability(self):
        data = {'username': 'test', 'email': 'test@example.com'}
        # Make a POST request to the check_availability route
        response = self.app.post('/check_availability', json=data)
        expected_result = {'username_available': True, 'email_available': True}
        self.assertEqual(response.get_json(), expected_result)



    def test_password_hashing(self):
        u = User(username='susan', email='susan@example.com')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))
        


    def test_avatar(self):
        u = User(username='john', email='john@example.com')
        digest = hashlib.md5(u.email.lower().encode('utf-8')).hexdigest()
        self.assertEqual(u.avatar(128), f'https://www.gravatar.com/avatar/{digest}?d=identicon&s=128')
        


    def test_follow(self):
        u1 = self.user1
        u2 = self.user2
        self.assertEqual(u1.following_count(), 0)
        self.assertEqual(u2.followers_count(), 0)

        u1.follow(u2)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.following_count(), 1)
        self.assertEqual(u2.followers_count(), 1)

        u1.unfollow(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.following_count(), 0)
        self.assertEqual(u2.followers_count(), 0)

    def test_follow_posts(self):
        u1 = self.user1
        u2 = self.user2
        u3 = self.user3
        u4 = self.user4

        now = datetime.now(timezone.utc)
        p1 = Post(title="Post from john", content="Content", author=u1, timestamp=now + timedelta(seconds=1))
        p2 = Post(title="Post from susan", content="Content", author=u2, timestamp=now + timedelta(seconds=4))
        p3 = Post(title="Post from mary", content="Content", author=u3, timestamp=now + timedelta(seconds=3))
        p4 = Post(title="Post from david", content="Content", author=u4, timestamp=now + timedelta(seconds=2))
        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()

        u1.follow(u2)
        u1.follow(u4)
        u2.follow(u3)
        u3.follow(u4)
        db.session.commit()

        f1 = db.session.scalars(u1.following_posts()).all()
        f2 = db.session.scalars(u2.following_posts()).all()
        f3 = db.session.scalars(u3.following_posts()).all()
        f4 = db.session.scalars(u4.following_posts()).all()
        self.assertEqual(f1, [p2, p4, p1])
        self.assertEqual(f2, [p2, p3])
        self.assertEqual(f3, [p3, p4])
        self.assertEqual(f4, [p4])

   #test Only followed user posts without current user's own posts
    def test_following_posts_only(self):
        u1 = self.user1
        u2 = self.user2
        u3 = self.user3
        u4 = self.user4
        now = datetime.now(timezone.utc)
        p1 = Post(title="Post from john", content="Contentfrom john", author=u1, timestamp=now + timedelta(seconds=1))
        p2 = Post(title="Post from susan", content="Content from susan", author=u2, timestamp=now + timedelta(seconds=4))
        p3 = Post(title="Post from mary", content="Content from mary", author=u3, timestamp=now + timedelta(seconds=3))
        p4 = Post(title="Post from david", content="Content from david", author=u4, timestamp=now + timedelta(seconds=2))
        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()
        u1.follow(u2)
        u1.follow(u3)
        u1.follow(u4)
        u2.follow(u3)
        u3.follow(u4)
        u4.follow(u2)
        db.session.commit()
        f1 = db.session.scalars(u1.following_posts_only()).all()
        f2 = db.session.scalars(u2.following_posts_only()).all()
        f3 = db.session.scalars(u3.following_posts_only()).all()
        f4 = db.session.scalars(u4.following_posts_only()).all()
        self.assertEqual(f1, [p2, p3, p4])
        self.assertEqual(f2, [p3])
        self.assertEqual(f3, [p4])
        self.assertEqual(f4, [p2])

   # test Only followed user posts without current user's own posts, User not follow anyone
    def test_following_posts_only_no_follow(self):
        u1 = self.user1
        u2 = self.user2
        now = datetime.now(timezone.utc)
        p1 = Post(title="Post from john", content="Contentfrom john", author=u1, timestamp=now + timedelta(seconds=1))
        p2 = Post(title="Post from susan", content="Content from susan", author=u2, timestamp=now + timedelta(seconds=4))
        db.session.add_all([p1, p2])
        db.session.commit()
        f1 = db.session.scalars(u1.following_posts_only()).all()
        f2 = db.session.scalars(u2.following_posts_only()).all()
        self.assertEqual(f1, [])
        self.assertEqual(f2, [])
     

    def test_post(self):
        u = self.user1
        p = Post(title='Test Post', content='Test content', author=u)
        db.session.add(p)
        db.session.commit()
        self.assertEqual(p.title, 'Test Post')
        self.assertEqual(p.content, 'Test content')
        self.assertEqual(p.author, u)

    def test_upload_avatar(self):
        u = self.user1
        u.avatar_path = 'path/to/avatar.jpg'
        db.session.commit()
        
        with app.test_request_context():
            self.assertEqual(u.avatar(128), '/uploaded_avatars/path/to/avatar.jpg')

    def test_edit_profile(self):
        u = self.user1
        u.about_me = 'Hello, this is John!'
        db.session.commit()
        self.assertEqual(u.about_me, 'Hello, this is John!')


class PostModelCase(BaseModelTestCase):
    def test_post_replies_count(self):
        u = self.user1
        p = Post(title='Test Post', content='Test content', author=u)
        db.session.add(p)
        db.session.commit()

        r1 = Reply(content='Reply 1', user=u, post=p)
        r2 = Reply(content='Reply 2', user=u, post=p)
        db.session.add_all([r1, r2])
        db.session.commit()

        self.assertEqual(p.replies_count(), 2)


class ReplyModelCase(BaseModelTestCase):
    def test_reply(self):
        u = self.user1
        p = Post(title='Test Post', content='Test content', author=u)
        db.session.add(p)
        db.session.commit()

        r = Reply(content='This is a reply', user=u, post=p)
        db.session.add(r)
        db.session.commit()

        self.assertEqual(r.content, 'This is a reply')
        self.assertEqual(r.user, u)
        self.assertEqual(r.post, p)


class MessageModelCase(BaseModelTestCase):
    def test_message_relationships(self):
        sender = self.user1
        recipient = self.user2
        message = Message(body='Test message', author=sender, recipient=recipient)
        db.session.add(message)
        db.session.commit()

        self.assertEqual(message.author, sender)
        self.assertEqual(message.recipient, recipient)

    def test_send_message(self):
        sender = self.user1
        recipient = self.user2
        message = Message(body='Hello Susan!', author=sender, recipient=recipient)
        db.session.add(message)
        db.session.commit()

        self.assertEqual(message.body, 'Hello Susan!')
        self.assertEqual(message.author, sender)
        self.assertEqual(message.recipient, recipient)


class NotificationModelCase(BaseModelTestCase):
    def test_notification_payload(self):
        user = self.user1
        notification = Notification(name='test_notification', user=user, payload_json='{"key": "value"}')
        db.session.add(notification)
        db.session.commit()

        self.assertEqual(notification.user, user)
        self.assertEqual(notification.get_data(), {'key': 'value'})

if __name__ == '__main__':
    unittest.main(verbosity=2)
