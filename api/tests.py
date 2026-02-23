import unittest
from api import create_app
from api.models import db, User, Task, TaskList
import os

class MyTest(unittest.TestCase):
    def setUp(self):
        # Create a test app
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['WTF_CSRF_ENABLED'] = False
        
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_starts(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_register_login(self):
        # Register
        self.client.post('/register', data=dict(
            username='testuser',
            email='test@example.com',
            password='password123'
        ), follow_redirects=True)
        user = User.query.filter_by(email='test@example.com').first()
        self.assertIsNotNone(user)

        # Login
        response = self.client.post('/login', data=dict(
            email='test@example.com',
            password='password123'
        ), follow_redirects=True)
        self.assertIn(b'My Tasks', response.data)

    def test_add_todo_with_lists(self):
        # Register and Login (also automatically creates a default list now)
        self.client.post('/register', data=dict(
            username='testuser',
            email='test@example.com',
            password='password123'
        ), follow_redirects=True)
        
        # Get the automatically created list
        user = User.query.filter_by(email='test@example.com').first()
        task_list = TaskList.query.filter_by(user_id=user.id).first()
        self.assertIsNotNone(task_list, "A default task list should be created upon registration")
        
        # Add Task via TaskForm
        response = self.client.post('/task/add', data=dict(
            task='Test Task',
            due_date='2026-12-31',
            list_id=task_list.id
        ), follow_redirects=True)
        
        # Verify it rendered in the HTML
        self.assertIn(b'Test Task', response.data)
        
        # Verify it exists in DB
        task = Task.query.first()
        self.assertIsNotNone(task)
        self.assertEqual(task.task, 'Test Task')
        self.assertEqual(task.task_list_id, task_list.id)

if __name__ == '__main__':
    unittest.main()
