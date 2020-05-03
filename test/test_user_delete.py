from create_application import create_application
from src.model.user import User
from src.model.secured_password import SecuredPassword
import unittest
import json

class TestUserRegistration(unittest.TestCase):
    def setUp(self) -> None:
        self.app, self.controller = create_application(return_controller=True)
        admin_user = User(email="admin@admin.com", fullname="Admin",
                          phone_number="11 1111-1111", photo="",
                          secured_password=SecuredPassword.from_raw_password("admin"),
                          admin=True)
        self.controller.database.save_user(admin_user)
        self.app.testing = True

    def test_user_delete_for_missing_fields_error(self):
        with self.app.test_client() as c:
            response = c.delete('/user', query_string={"fullname": "Carolina"})
            self.assertEqual(response.status_code, 400)

    def test_user_delete_for_non_existing_user_error(self):
        with self.app.test_client() as c:
            response = c.delete('/user', query_string={"email": "caropistillo@gmail.com"})
            self.assertEqual(response.status_code, 404)

    def test_user_delete_success(self):
        with self.app.test_client() as c:
            response = c.post('/user', data='{"email":"caropistillo@gmail.com", "password": "carolina15", "fullname":'
                                 '"Carolina Rocio", "phone_number":"11 1111-1111", "photo":""}',
                                                        headers={"Content-Type": "application/json"})
            self.assertEqual(response.status_code, 200)
            response = c.delete('/user', query_string={"email": "caropistillo@gmail.com"})
            self.assertEqual(response.status_code, 200)

    def test_user_delete_and_login_non_existing_user_error(self):
        with self.app.test_client() as c:
            response = c.post('/user', data='{"email":"caropistillo@gmail.com", "password": "carolina15", "fullname":'
                                 '"Carolina Rocio", "phone_number":"11 1111-1111", "photo":""}',
                                                        headers={"Content-Type": "application/json"})
            self.assertEqual(response.status_code, 200)
            response = c.delete('/user', query_string={"email": "caropistillo@gmail.com"})
            self.assertEqual(response.status_code, 200)
            response = c.post('/user/login', data='{"email":"caropistillo@gmail.com", "password": "carolina15" }',
                              headers={"Content-Type": "application/json"})
            self.assertEqual(response.status_code, 404)

    def test_user_delete_and_query_non_existing_user_error(self):
        with self.app.test_client() as c:
            response = c.post('/user', data='{"email":"caropistillo@gmail.com", "password": "carolina15", "fullname":'
                                 '"Carolina Rocio", "phone_number":"11 1111-1111", "photo":""}',
                                                        headers={"Content-Type": "application/json"})
            self.assertEqual(response.status_code, 200)
            response = c.delete('/user', query_string={"email": "caropistillo@gmail.com"})
            self.assertEqual(response.status_code, 200)

            response = c.post('/user/login', data='{"email":"admin@admin.com", "password":"admin"}',
                              headers={"Content-Type": "application/json"})
            token = json.loads(response.data)["login_token"]

            response = c.get('/user', query_string={"email": "caropistillo@gmail.com"},
                             headers={"Authorization": "Bearer %s" % token})
            self.assertEqual(response.status_code, 404)

    def test_user_delete_and_update_non_existing_user_error(self):
        with self.app.test_client() as c:
            response = c.post('/user', data='{"email":"caropistillo@gmail.com", "password": "carolina15", "fullname":'
                                 '"Carolina Rocio", "phone_number":"11 1111-1111", "photo":""}',
                                                        headers={"Content-Type": "application/json"})
            self.assertEqual(response.status_code, 200)
            response = c.delete('/user', query_string={"email": "caropistillo@gmail.com"})
            self.assertEqual(response.status_code, 200)
            response = c.put('/user', query_string={"email": "caropistillo@gmail.com"},
                             data='{"fullname":"Carolina Pistillo", "phone_number":"11 3263-7625", "photo":"caro.jpg", '
                                  '"password":"carolina"}', headers={"Content-Type": "application/json"})
            self.assertEqual(response.status_code, 404)

