import unittest
from api.main import app, db, User, Task
from flask_testing import TestCase
import os

class MyTest(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_app_starts(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_register_login(self):
        # Register
        self.client.post('/register', data=dict(
            username='testuser',
            email='test@example.com',
            password='password'
        ), follow_redirects=True)
        user = User.query.filter_by(email='test@example.com').first()
        self.assertIsNotNone(user)

        # Login
        response = self.client.post('/login', data=dict(
            email='test@example.com',
            password='password'
        ), follow_redirects=True)
        self.assertIn(b'testuser', response.data)

    def test_add_todo(self):
        # Register and Login
        self.client.post('/register', data=dict(
            username='testuser',
            email='test@example.com',
            password='password'
        ), follow_redirects=True)
        
        # Add Task
        response = self.client.post('/add_task', data=dict(
            task='Test Task',
            due_date='2026-12-31'
        ), follow_redirects=True)
        self.assertIn(b'Test Task', response.data)
        
        task = Task.query.first()
        self.assertIsNotNone(task)
        self.assertEqual(task.task, 'Test Task')

if __name__ == '__main__':
    unittest.main()
