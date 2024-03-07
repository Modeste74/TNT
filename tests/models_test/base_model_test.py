#!/usr/bin/python3
"""defines the test for base_model class"""
import unittest
from models.base_model import BaseModel, Base
from datetime import datetime
from models import storage

class TestBaseModel(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Reload the storage to set up the session
        storage.reload()

    @classmethod
    def tearDownClass(cls):
        # Close the session after all tests in the class
        storage.close()

    def setUp(self):
        # Create an instance of BaseModel
        self.model = BaseModel()

    def tearDown(self):
        # Clean up the session after each test
        storage.close()

    def test_instance_creation(self):
        self.assertIsInstance(self.model, BaseModel)

    # Add other test methods...

    def test_instance_creation(self):
        self.assertIsInstance(self.model, BaseModel)

    def test_id_generation(self):
        self.assertIsNotNone(self.model.id)
        self.assertIsInstance(self.model.id, str)

    def test_created_at_type(self):
        self.assertIsInstance(self.model.created_at, datetime)

    def test_to_dict_method(self):
        model_dict = self.model.to_dict()
        self.assertIsInstance(model_dict, dict)
        self.assertIn('id', model_dict)
        self.assertIn('created_at', model_dict)
        self.assertIn('updated_at', model_dict)
        self.assertIn('__class__', model_dict)


if __name__ == '__main__':
    unittest.main()
