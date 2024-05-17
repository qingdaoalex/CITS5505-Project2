import os
import unittest
from flask import current_app, session
from app import create_app, db
from app.models import User, Post, Reply
from config import TestConfig
from flask_login import login_user

class SearchFunctionalityTestCase(unittest.TestCase):
    def setUp(self):
        # Set up the application and database
        self.app = create_app(TestConfig)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['TESTING'] = True
        self.app.config['LOGIN_DISABLED'] = True  # Disable login for testing
        self.app.logger.disabled = True
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Create test user, post, and reply
        user = User.query.filter_by(username='testuser').first()
        if not user:
            user = User(username='testuser', email='test@example.com')
            user.set_password('password')
            db.session.add(user)
            db.session.commit()

        post = Post(title='Test Post', content='This is a test post', author=user)
        db.session.add(post)
        db.session.commit()

        reply = Reply(content='Test reply', post=post, user=user)
        db.session.add(reply)
        db.session.commit()

        self.client = self.app.test_client(use_cookies=True)
        with self.app.test_request_context():
            login_user(user)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_search_route_get(self):
        response = self.client.get('/search')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.data.decode())

    def test_search_route_post(self):
        response = self.client.post('/search', data={
            'query': 'test',
            'type': 'post'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Post', response.data.decode())

    def test_search_results_user(self):
        response = self.client.get('/search_results?query=testuser&type=user')
        self.assertEqual(response.status_code, 200)
        self.assertIn('testuser', response.data.decode())

    def test_search_results_post(self):
        response = self.client.get('/search_results?query=Test&type=post')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Post', response.data.decode())

    def test_search_results_reply(self):
        response = self.client.get('/search_results?query=Test&type=reply')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test reply', response.data.decode())

    def test_search_results_no_results(self):
        response = self.client.get('/search_results?query=xyz&type=post')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('No results found' in response.data.decode())  # Adjust based on actual no-results handling

if __name__ == '__main__':
    unittest.main()
