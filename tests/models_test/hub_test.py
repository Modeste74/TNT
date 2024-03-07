#!/usr/bin/python3
"""Defines tests for the Hub and HubLearners classes"""
import unittest
from models.hub import Hub, HubLearners
from models.base_model import BaseModel, Base
from models.users import Users
from models.resource import Resource
from models.chat import Chat
from models.group import Group
from models import storage

class TestHubModel(unittest.TestCase):

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
        # Create a test user (tutor)
        self.tutor_user = Users(username="tutor_user",
                                password="tutor_password", user_type="tutor")

        # Create a test hub
        self.test_hub = Hub(tutor_id=self.tutor_user.id,
                            name="Test Hub", participants=1)

        # Save the tutor user and hub
        storage.new(self.tutor_user)
        storage.new(self.test_hub)
        storage.save()

    def test_hub_creation(self):
        self.assertIsInstance(self.test_hub, Hub)
        self.assertIsInstance(self.test_hub, BaseModel)
        self.assertIsInstance(self.test_hub, Base)

    def test_hub_relationships(self):
        # Ensure relationships with tutor, resources, chats, and groups work
        resource = Resource(hub_id=self.test_hub.id, name="Test Resource")
        chat = Chat(hub_id=self.test_hub.id, name="Test Chat")
        group = Group(hub_id=self.test_hub.id, name="Test Group")

        storage.new(resource)
        storage.new(chat)
        storage.new(group)
        storage.save()

        self.assertEqual(self.test_hub.tutor, self.tutor_user)
        self.assertIn(resource, self.test_hub.resources)
        self.assertIn(chat, self.test_hub.chats)
        self.assertIn(group, self.test_hub.groups)

    def test_hub_learners_relationship(self):
        # Ensure relationships with learners in the hub work
        learner = Users(username="learner_user",
                        password="learner_password", user_type="learner")

        hub_learner = HubLearners(hub_id=self.test_hub.id, learner_id=learner.id)

        storage.new(learner)
        storage.new(hub_learner)
        storage.save()

        self.assertIn(hub_learner, self.test_hub.learners)
        self.assertIn(hub_learner, learner.hubs_association)

if __name__ == '__main__':
    unittest.main()