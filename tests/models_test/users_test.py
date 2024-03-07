#!/usr/bin/python3
"""Defines tests for the Users class"""

import unittest
from models.users import Users
from models.messages import Message
from models.hub import HubLearners, Hub
from models.base_model import BaseModel, Base
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from models import storage

class TestUsersModel(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Reload the storage to set up the session
        storage.reload()

    @classmethod
    def tearDownClass(cls):
        # Close the session after all tests in the class
        storage.close()

    def tearDown(self):
        # Clean up the session after each test
        storage.close()

    def setUp(self):
        # Create a test user
        self.test_user = Users(username="test_user",
                               password="test_password", user_type="tutor")

    def test_user_creation(self):
        self.assertIsInstance(self.test_user, Users)
        self.assertIsInstance(self.test_user, BaseModel)
        self.assertIsInstance(self.test_user, Base)

    def test_set_password(self):
        # Ensure the password is hashed properly
        original_password = "test_password"
        hashed_password = generate_password_hash(original_password)
        self.assertNotEqual(self.test_user.password, original_password)
        self.assertTrue(self.test_user.check_password(original_password))
        self.assertTrue(check_password_hash(self.test_user.password, original_password))

    def test_check_password(self):
        # Ensure the check_password method works correctly
        correct_password = "test_password"
        incorrect_password = "wrong_password"
        self.assertTrue(self.test_user.check_password(correct_password))
        self.assertFalse(self.test_user.check_password(incorrect_password))


if __name__ == '__main__':
    unittest.main()
