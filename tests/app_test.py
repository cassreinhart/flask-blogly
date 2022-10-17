from unittest import TestCase
from app import app
from flask import session
from models import User


class FlaskTests(TestCase):

    def test_users(self):
        with app.text_client() as client:
            res = client.get('/users')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h2>Users</h2>')
    
    def test_user_info_page(self):
        with app.test_client() as client:
            res = client.get('/users/1')

            self.assertEqual(res.status_code, 200)
            self.assertIn('<button formaction="/users/1/edit" formmethod="get" id="edit">Edit</button>')

    def test_user_edit_page(self):
        with app.test_client() as client:
            res = client.get('/users/1/edit')
            
            self.assertEqual(res.status_code, 200)
            self.assertIn('<label for="first_name">First Name </label> <input type="text" name="first_name">')

        def test_user_delete(self):
            with app.test_client() as client:
                res = client.get('/users/1/delete')
                
                self.assertNotIn('<a href="users/1">')