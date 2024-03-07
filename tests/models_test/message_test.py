#!usr/bin/python3
"""defines tests for message class"""
import unittest
from models.users import Users
from models.messages import Message
from models.base_model import BaseModel, Base
from werkzeug.security import generate_password_hash
from models import storage

class TestMessageModel(unittest.TestCase):

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
        # Create two test users
        self.sender_user = Users(username="sender_user",
                                  password="sender_password", user_type="tutor")
        self.receiver_user = Users(username="receiver_user",
                                    password="receiver_password", user_type="learner")

        # Create a test message
        self.test_message = Message(sender_id=self.sender_user.id,
                                    receiver_id=self.receiver_user.id,
                                    content="Test message content")

    def test_message_creation(self):
        self.assertIsInstance(self.test_message, Message)
        self.assertIsInstance(self.test_message, BaseModel)
        self.assertIsInstance(self.test_message, Base)

    def test_message_relationships(self):
    	# Create sender and receiver users
   		sender_user = Users(username="sender_user",
   			password="sender_password", user_type="tutor")
   		receiver_user = Users(username="receiver_user",
    		password="receiver_password", user_type="learner")

   		storage.new(sender_user)
   		storage.new(receiver_user)
   		storage.save()
   		self.test_message = Message(sender_id=sender_user.id,
   			receiver_id=receiver_user.id,
   			message="Test message content")

   		storage.new(self.test_message)
   		storage.save()

   		self.assertEqual(self.test_message.sender, sender_user)
   		self.assertEqual(self.test_message.receiver, receiver_user)
   		self.assertIn(self.test_message, sender_user.sent_messages)
   		self.assertIn(self.test_message, receiver_user.received_messages)


if __name__ == '__main__':
    unittest.main()