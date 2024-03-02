#!/usr/bin/python3
""" console """

import cmd
from datetime import datetime
import models
from models.base_model import BaseModel
from models.messages import Message
from models.users import Users
from models.hub import Hub, HubLearners
from models.resource import Resource
from models.chat import Chat
from models.group import Group
from models.group_members import GroupMember
import shlex  # for splitting the line along spaces except in double quotes

classes = {"Users": Users, "BaseModel": BaseModel, "Message": Message,
        "Hub": Hub, "Resource": Resource, "Chat": Chat, "Group": Group,
        "HubLearners": HubLearners, "GroupMember": GroupMember}


class DEPCommand(cmd.Cmd):
    """ DEP console """
    prompt = '(dentalEasepro) '

    def do_EOF(self, arg):
        """Exits console"""
        return True

    def emptyline(self):
        """ overwriting the emptyline method """
        return False

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def _key_value_parser(self, args):
        """creates a dictionary from a list of strings"""
        new_dict = {}
        for arg in args:
            if "=" in arg:
                kvp = arg.split('=', 1)
                key = kvp[0]
                value = kvp[1]
                if value[0] == value[-1] == '"':
                    value = shlex.split(value)[0].replace('_', ' ')
                else:
                    try:
                        value = int(value)
                    except Exception as e:
                        try:
                            value = float(value)
                        except Exception as f:
                            continue
                new_dict[key] = value
        return new_dict

    def do_create(self, arg):
        """Creates a new instance of a class"""
        args = arg.split()
        if len(args) == 0:
            print(" class name missing ")
            return False
        if args[0] in classes:
            new_dict = {}
            current_key = None
            for arg in args[1:]:
                if "=" in arg:
                    current_key, value = arg.split("=", 1)
                    value = value.strip('"')  # Remove leading double quote
                    new_dict[current_key] = value
                elif current_key:
                    new_dict[current_key] += " " + arg
                # Remove trailing double quotes for all values in new_dict
            for key in new_dict:
                new_dict[key] = new_dict[key].strip('"')
            instance = classes[args[0]](**new_dict)
            print(instance.id)
            instance.save()
        else:
            print(" class doesn't exist ")

    def do_show(self, arg):
        """Prints an instance as a string based on the class and id"""
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] in classes:
            if len(args) > 1:
                key = args[0] + "." + args[1]
                if key in models.storage.all():
                    print(models.storage.all()[key])
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

    def do_destroy(self, arg):
        args = shlex.split(arg)
        if len(args) != 2:
            print("** Missing class name or instance id **")
            return
        class_name, instance_id = args[0], args[1]
        if class_name in classes:
            obj = models.storage.get(classes[class_name], instance_id)
            if obj:
                models.storage.delete(obj)
                models.storage.save()
            else:
                print("** No instance found **")
        else:
            print("** Class doesn't exist **")


    def do_all(self, arg):
        """Prints string representations of instances"""
        args = shlex.split(arg)
        obj_list = []
        if len(args) == 0:
            obj_dict = models.storage.all()
        elif args[0] in classes:
            obj_dict = models.storage.all(classes[args[0]])
        else:
            print("** class doesn't exist **")
            return False
        for key in obj_dict:
            obj_list.append(str(obj_dict[key]))
        print("[", end="")
        print(", ".join(obj_list), end="")
        print("]")

    def do_update(self, arg):
        """Update an instance based on the class name, id, attribute & value"""
        args = shlex.split(arg)
        if len(args) < 4:
            print("** Missing arguments **")
            return
        class_name, instance_id, attribute, value = args[0], args[1], args[2], args[3]
        key = f"{class_name}.{instance_id}"

        if key not in models.storage.all():
            print("** No instance found **")
            return
        instance = models.storage.get(classes[class_name], instance_id)
        if not hasattr(instance, attribute):
            print("** Attribute not found in instance **")
            return
        setattr(instance, attribute, value)

    def do_count(self, args):
        """Count current number of class instances"""
        count = 0
        for k, v in models.storage.all().items():
            if args == k.split('.')[0]:
                count += 1
        print(count)


if __name__ == '__main__':
    DEPCommand().cmdloop()
