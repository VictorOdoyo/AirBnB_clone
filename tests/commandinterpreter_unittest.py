#!/usr/bin/python3
"""Unit test for the command interpreter."""

import unittest
import re
import json
from models.base_model import BaseModel
from models import storage
from hbnb import HBNBCommand

class TestHBNBCommand(unittest.TestCase):
    def setUp(self):
        self.hbnb = HBNBCommand()

    def test_default(self):
        # Test when the line does not match the pattern for class.syntax()
        line = "not_valid_command"
        self.assertEqual(self.hbnb._precmd(line), line)

        # Test when the line matches the pattern for class.syntax()
        line = "BaseModel.create()"
        self.assertEqual(self.hbnb._precmd(line), "create BaseModel ")

    def test_update_dict(self):
        classname = "BaseModel"
        uid = "1234-5678-9012-3456"
        s_dict = '{"name": "John", "age": 30}'

        # Test when class name doesn't exist
        classname = "InvalidClass"
        self.hbnb.update_dict(classname, uid, s_dict)
        self.assertEqual(self.hbnb.prompt_output.getvalue().strip(),
                         "** class doesn't exist **")

        # Test when instance id is missing
        classname = "BaseModel"
        uid = None
        self.hbnb.update_dict(classname, uid, s_dict)
        self.assertEqual(self.hbnb.prompt_output.getvalue().strip(),
                         "** instance id missing **")

        # Test when instance is not found
        classname = "BaseModel"
        uid = "invalid_id"
        self.hbnb.update_dict(classname, uid, s_dict)
        self.assertEqual(self.hbnb.prompt_output.getvalue().strip(),
                         "** no instance found **")

        # Test when the update is successful
        b = BaseModel()
        b.id = uid
        b.save()
        self.hbnb.update_dict(classname, uid, s_dict)
        key = "{}.{}".format(classname, uid)
        self.assertEqual(getattr(storage.all()[key], "name"), "John")
        self.assertEqual(getattr(storage.all()[key], "age"), 30)

    def test_do_EOF(self):
        self.assertEqual(self.hbnb.do_EOF(""), True)
        self.assertEqual(self.hbnb.prompt_output.getvalue().strip(), "")

    def test_do_quit(self):
        self.assertEqual(self.hbnb.do_quit(""), True)

    def test_emptyline(self):
        self.assertEqual(self.hbnb.emptyline(), None)

    # More tests for other methods in the class can be added
