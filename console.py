#!/usr/bin/python3
"""This is a console Module for HBNB project."""
import cmd
import sys
import re
import os
from datetime import datetime
import uuid
from models.base_model import BaseModel
from models import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
import shlex
import MySQLdb


class HBNBCommand(cmd.Cmd):
    """Contains functionality for the HBNB console."""

    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''  # Determine prompt

    # Mapping of class names to their corresponding classes
    classes = {
        'BaseModel': BaseModel, 'User': User, 'Place': Place,
        'State': State, 'City': City, 'Amenity': Amenity,
        'Review': Review
    }

    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']

    # Dictionary to map attribute types for casting
    types = {
        'number_rooms': int, 'number_bathrooms': int,
        'max_guest': int, 'price_by_night': int,
        'latitude': float, 'longitude': float
    }

    # Define ignored_attributes
    ignored_attributes = ('id', 'created_at', 'updated_at', '__class__')

    def preloop(self):
        """Print prompt if isatty is False."""
        if not sys.__stdin__.isatty():
            print('(hbnb)')

    def precmd(self, line):
        """Reformat command line for advanced command syntax."""
        _cmd = _cls = _id = _args = ''

        # Check for general formatting - i.e., '.', '(', ')'
        if not ('.' in line and '(' in line and ')' in line):
            return line

        try:
            pline = line[:]  # Parsed line

            # Isolate <class name>
            _cls = pline[:pline.find('.')]

            # Isolate and validate <command>
            _cmd = pline[pline.find('.') + 1:pline.find('(')]
            if _cmd not in HBNBCommand.dot_cmds:
                raise Exception

            # If parentheses contain arguments, parse them
            pline = pline[pline.find('(') + 1:pline.find(')')]
            if pline:
                # Partition args: (<id>, [<delim>], [<*args>])
                pline = pline.partition(', ')

                # Isolate _id, stripping quotes
                _id = pline[0].replace('\"', '')

                # If arguments exist beyond _id
                pline = pline[2].strip()  # pline is now str
                if pline:
                    # Check for *args or **kwargs
                    if pline[0] == '{' and pline[-1] == '}' and type(eval(pline)) is dict:
                        _args = pline
                    else:
                        _args = pline.replace(',', '')

            line = ' '.join([_cmd, _cls, _id, _args])

        except Exception as mess:
            pass
        finally:
            return line

    def postcmd(self, stop, line):
        """Print prompt if isatty is False."""
        if not sys.__stdin__.isatty():
            print('(hbnb) ', end='')
        return stop

    def do_quit(self, command):
        """Exit the HBNB console."""
        exit(0)

    def help_quit(self):
        """Print help documentation for quit."""
        print("Exits the program with formatting\n")

    def do_EOF(self, arg):
        """Handle EOF to exit program."""
        print()
        exit(0)

    def help_EOF(self):
        """Print help documentation for EOF."""
        print("Exits the program without formatting\n")

    def emptyline(self):
        """Overrides the emptyline method of CMD."""
        pass

    def do_create(self, arg):
        """Creates a new instance of a specified class"""
        if not arg:
            print("** class name missing **")
            return

        class_name, *attributes = arg.split()
        if class_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        # Create an instance of the specified class
        new_instance = HBNBCommand.classes[class_name]()

        # Parse the attributes and their values
        for attribute in attributes:
            key, value = attribute.split("=")
            # Remove double quotes around the value if present
            value = value.strip('\"')
            # Set the attribute of the instance
            setattr(new_instance, key, value)

        # Save the instance to the storage
        new_instance.save()
        print(new_instance.id)

    # def do_create(self, args):
    #     # """
    #     # Create an instance of a specified class.

    #     # Usage: create <class_name> [<attribute_name>="<attribute_value>" ...]
    #     # """
    #     if not args:
    #         print("** class name missing **")
    #         return

    #     try:
    #         class_name, *attributes = shlex.split(args)
    #         class_name = class_name.strip()

    #         if class_name not in HBNBCommand.classes:
    #             print("** class doesn't exist **")
    #             return

    #         attribute_dict = {}
    #         for attribute in attributes:
    #             name, _, value = attribute.partition("=")
    #             name = name.strip()
    #             value = value.strip()

    #             if name not in HBNBCommand.ignored_attributes:
    #                 if name in HBNBCommand.types:
    #                     try:
    #                         value = HBNBCommand.types[name](value)
    #                     except ValueError:
    #                         print(f"Invalid value for attribute '{name}'")
    #                         return

    #                 attribute_dict[name] = value

    #         new_instance = HBNBCommand.classes[class_name](**attribute_dict)

    #         if os.getenv('HBNB_TYPE_STORAGE') == 'db':
    #             new_instance.save()
    #             print(new_instance.id)
    #         else:
    #             storage.new(new_instance)
    #             storage.save()
    #             print(new_instance.id)

    #     except Exception as e:
    #         print(f"Error: {e}")
    #         import traceback
    #         traceback.print_exc()


    # def do_create(self, args):
    #     """
    #     Create an instance of a specified class.

    #     Usage: create <class_name> [<attribute_name>="<attribute_value>" ...]
    #     """
    #     ignored_attributes = ('id', 'created_at', 'updated_at', '__class__')
    #     class_name = ''
    #     class_match = re.match(r'(?P<name>[a-zA-Z_]\w*)', args)

    #     if class_match is not None:
    #         class_name = class_match.group('name')
    #     else:
    #         print("** class name missing **")
    #         return

    #     if class_name not in HBNBCommand.classes:
    #         print("** class doesn't exist **")
    #         return

    #     attribute_dict = {}
    #     attribute_pattern = r'(?P<name>[a-zA-Z_]\w*)=(?P<value>.+)'
    #     attribute_matches = re.finditer(attribute_pattern, args)

    #     for match in attribute_matches:
    #         attribute_name = match.group('name')
    #         attribute_value = match.group('value')

    #         if attribute_name not in ignored_attributes:
    #             if attribute_name in HBNBCommand.types:
    #                 attribute_value = HBNBCommand.types[attribute_name](attribute_value)

    #             attribute_dict[attribute_name] = attribute_value

    #     new_instance = HBNBCommand.classes[class_name](**attribute_dict)

    #     if os.getenv('HBNB_TYPE_STORAGE') == 'db':
    #         new_instance.save()
    #         print(new_instance.id)
    #     else:
    #         storage.new(new_instance)
    #         storage.save()
    #         print(new_instance.id)

    #         """Create an object of any class."""
    #         ignored_attrs = ('id', 'created_at', 'updated_at', '__class__')
    #         class_name = ''
    #         name_pattern = r'(?P<name>(?:[a-zA-Z]|_)(?:[a-zA-Z]|\d|_)*)'
    #         class_match = re.match(name_pattern, args)
    #         obj_kwargs = {}

    #         if class_match is not None:
    #             class_name = class_match.group('name')
    #             params_str = args[len(class_name):].strip()
    #             params = params_str.split(' ')
    #             str_pattern = r'(?P<t_str>"([^"]|\")*")'
    #             float_pattern = r'(?P<t_float>[-+]?\d+\.\d+)'
    #             int_pattern = r'(?P<t_int>[-+]?\d+)'
    #             param_pattern = '{}=({}|{}|{})'.format(
    #                 name_pattern,
    #                 str_pattern,
    #                 float_pattern,
    #                 int_pattern
    #             )

    #             for param in params:
    #                 param_match = re.fullmatch(param_pattern, param)

    #                 if param_match is not None:
    #                     key_name = param_match.group('name')
    #                     str_v = param_match.group('t_str')
    #                     float_v = param_match.group('t_float')
    #                     int_v = param_match.group('t_int')

    #                     if float_v is not None:
    #                         obj_kwargs[key_name] = float(float_v)

    #                     if int_v is not None:
    #                         obj_kwargs[key_name] = int(int_v)

    #                     if str_v is not None:
    #                         obj_kwargs[key_name] = str_v[1:-1].replace('_', ' ')
    #         else:
    #             class_name = args

    #         if not class_name:
    #             print("** class name missing **")
    #             return
    #         elif class_name not in HBNBCommand.classes:
    #             print("** class doesn't exist **")
    #             return

    #         if os.getenv('HBNB_TYPE_STORAGE') == 'db':
    #             if 'id' not in obj_kwargs:
    #                 obj_kwargs['id'] = str(uuid.uuid4())

    #             if 'created_at' not in obj_kwargs:
    #                 obj_kwargs['created_at'] = str(datetime.now())

    #             if 'updated_at' not in obj_kwargs:
    #                 obj_kwargs['updated_at'] = str(datetime.now())

    #             new_instance = HBNBCommand.classes[class_name](**obj_kwargs)
    #             new_instance.save()
    #             print(new_instance.id)
    #         else:
    #             new_instance = HBNBCommand.classes[class_name]()
    #             for key, value in obj_kwargs.items():
    #                 if key not in ignored_attrs:
    #                     setattr(new_instance, key, value)

    #             new_instance.save()
    #             print(new_instance.id)
    """
    def do_create(self, args):

        ignored_attributes = ('id', 'created_at', 'updated_at', '__class__')
        class_name = ''
        class_match = re.match(r'(?P<name>[a-zA-Z_]\w*)', args)

        if class_match is not None:
            class_name = class_match.group('name')
        else:
            print("** class name missing **")
            return

        if class_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        attribute_dict = {}
        attribute_pattern = r'(?P<name>[a-zA-Z_]\w*)=(?P<value>.+)'
        attribute_matches = re.finditer(attribute_pattern, args)

        for match in attribute_matches:
            attribute_name = match.group('name')
            attribute_value = match.group('value')

            if attribute_name not in ignored_attributes:
                if attribute_name in HBNBCommand.types:
                    attribute_value = HBNBCommand.types[attribute_name](attribute_value)

                attribute_dict[attribute_name] = attribute_value

        new_instance = HBNBCommand.classes[class_name](**attribute_dict)

        if os.getenv('HBNB_TYPE_STORAGE') == 'db':
            new_instance.save()
            print(new_instance.id)
        else:
            storage.new(new_instance)
            storage.save()
            print(new_instance.id)


            ignored_attrs = ('id', 'created_at', 'updated_at', '__class__')
            class_name = ''
            name_pattern = r'(?P<name>(?:[a-zA-Z]|_)(?:[a-zA-Z]|\d|_)*)'
            class_match = re.match(name_pattern, args)
            obj_kwargs = {}

            if class_match is not None:
                class_name = class_match.group('name')
                params_str = args[len(class_name):].strip()
                params = params_str.split(' ')
                str_pattern = r'(?P<t_str>"([^"]|\")*")'
                float_pattern = r'(?P<t_float>[-+]?\d+\.\d+)'
                int_pattern = r'(?P<t_int>[-+]?\d+)'
                param_pattern = '{}=({}|{}|{})'.format(
                    name_pattern,
                    str_pattern,
                    float_pattern,
                    int_pattern
                )

                for param in params:
                    param_match = re.fullmatch(param_pattern, param)

                    if param_match is not None:
                        key_name = param_match.group('name')
                        str_v = param_match.group('t_str')
                        float_v = param_match.group('t_float')
                        int_v = param_match.group('t_int')

                        if float_v is not None:
                            obj_kwargs[key_name] = float(float_v)

                        if int_v is not None:
                            obj_kwargs[key_name] = int(int_v)

                        if str_v is not None:
                            obj_kwargs[key_name] = str_v[1:-1].replace('_', ' ')
            else:
                class_name = args

            if not class_name:
                print("** class name missing **")
                return
            elif class_name not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return

            if os.getenv('HBNB_TYPE_STORAGE') == 'db':
                if 'id' not in obj_kwargs:
                    obj_kwargs['id'] = str(uuid.uuid4())

                if 'created_at' not in obj_kwargs:
                    obj_kwargs['created_at'] = str(datetime.now())

                if 'updated_at' not in obj_kwargs:
                    obj_kwargs['updated_at'] = str(datetime.now())

                new_instance = HBNBCommand.classes[class_name](**obj_kwargs)
                new_instance.save()
                print(new_instance.id)
            else:
                new_instance = HBNBCommand.classes[class_name]()
                for key, value in obj_kwargs.items():
                    if key not in ignored_attrs:
                        setattr(new_instance, key, value)

                new_instance.save()
                print(new_instance.id)
    """

    def help_create(self):
        """Help information for the create method."""
        print("Creates an instance of a class.")
        print("[Usage]: create <className> [<param1> <value1> <param2> <value2> ...]\n")

    def do_show(self, args):
        """Show information about an instance."""
        new = args.partition(" ")
        c_name = new[0]
        c_id = new[2]

        if c_id and ' ' in c_id:
            c_id = c_id.partition(' ')[0]

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id

        try:
            print(storage.all()[key])
        except KeyError:
            print("** no instance found **")

    def help_show(self):
        """Help information for the show command."""
        print("Shows information about an instance of a class.")
        print("[Usage]: show <className> <objectId>\n")

    def do_destroy(self, args):
        """Destroy an instance."""
        new = args.partition(" ")
        c_name = new[0]
        c_id = new[2]

        if c_id and ' ' in c_id:
            c_id = c_id.partition(' ')[0]

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id

        try:
            storage.delete(storage.all()[key])
            storage.save()
        except KeyError:
            print("** no instance found **")

    def help_destroy(self):
        """Help information for the destroy command."""
        print("Destroys an instance of a class.")
        print("[Usage]: destroy <className> <objectId>\n")

    def do_all(self, args):
        """ Shows all objects, or all objects of a class"""
        print_list = []

        if args:
            args = args.split(' ')[0]  # remove possible trailing args
            if args not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return
            for k, v in storage.all().items():
                if k.split('.')[0] == args:
                    print_list.append(str(v))
        else:
            for k, v in storage.all().items():
                print_list.append(str(v))

        print(print_list)

    def help_all(self):
        """Help information for the all command."""
        print("Shows information about all instances or instances of a class.")
        print("[Usage]: all [<className>]\n")

    def do_count(self, args):
        """Count current number of class instances."""
        count = 0

        for k, v in storage.all().items():
            if args == k.split('.')[0]:
                count += 1

        print(count)

    def help_count(self):
        """Help information for the count command."""
        print("Count current number of class instances.")
        print("[Usage]: count <className>\n")

    def do_update(self, args):
        """Update information of an instance."""
        c_name = c_id = att_name = att_val = kwargs = ''

        args = args.partition(" ")

        if args[0]:
            c_name = args[0]
        else:
            print("** class name missing **")
            return

        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        args = args[2].partition(" ")

        if args[0]:
            c_id = args[0]
        else:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id

        if key not in storage.all():
            print("** no instance found **")
            return

        if '{' in args[2] and '}' in args[2] and type(eval(args[2])) is dict:
            kwargs = eval(args[2])
            args = []

            for k, v in kwargs.items():
                args.append(k)
                args.append(v)
        else:
            args = args[2]

            if args and args[0] == '\"':
                second_quote = args.find('\"', 1)
                att_name = args[1:second_quote]
                args = args[second_quote + 1:]

            args = args.partition(' ')

            if not att_name and args[0] != ' ':
                att_name = args[0]

            if args[2] and args[2][0] == '\"':
                att_val = args[2][1:args[2].find('\"', 1)]

            if not att_val and args[2]:
                att_val = args[2].partition(' ')[0]

            args = [att_name, att_val]

        new_dict = storage.all()[key]

        for i, att_name in enumerate(args):
            if (i % 2 == 0):
                att_val = args[i + 1]

                if not att_name:
                    print("** attribute name missing **")
                    return

                if not att_val:
                    print("** value missing **")
                    return

                if att_name in HBNBCommand.types:
                    att_val = HBNBCommand.types[att_name](att_val)

                new_dict.__dict__.update({att_name: att_val})

        new_dict.save()

    def help_update(self):
        """Help information for the update command."""
        print("Updates information of an instance.")
        print("Usage: update <className> <id> <attName> <attVal>\n")


if __name__ == "__main__":
    HBNBCommand().cmdloop()

