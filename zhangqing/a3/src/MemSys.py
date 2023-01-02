from __future__ import annotations

import os
from typing import Any
import string

DIR_MAX_ELEMS = 10
MAX_BUF_FILE_SIZE = 15

class MemSys():
    def __init__(self):
        self.root = Directory(self, path=[], name="~")
        self.cwd = self.root

    def path_to_string(self, path: list[Node]) -> str:
        return '/'.join(path)

    def alter_directory(self, path):
        d = self.get_node(path)
        self.cwd = d

    def create_directory(self, path: str, name: str) -> Directory:
        dest_dir = self.get_node(path)
        os.mkdir(path + '/' + name)
        return dest_dir.create_directory(name)

    def create_binary_file(self, path: str, name: str, information: str) -> BinaryFile:
        dest_dir = self.get_node(path)
        return dest_dir.create_binary_file(name, information)

    def create_log_file(self, path: str, name: str, information: str = None) -> LogFile:
        dest_dir = self.get_node(path)
        return dest_dir.create_log_file(name, information)

    def create_buffer(self, path: str, name: str) -> Buffer:
        dest_dir = self.get_node(path)
        return dest_dir.create_buffer(name)

    def get_node(self, path) -> Node:
        return self.cwd.find_node(path)

    def print_ele(self) -> None:
        print(self.cwd.name)
        self.cwd.print_ele(lvl=0)

    def delete(self, name):
        try:
            os.rmdir(name)
            print("Successfully delete such directory")
        except:
            print("Fail to delete")

class Node():
    def __init__(self, path: list[Node], name: str):
        self.path = path
        self.name = name

    def delete(self):
        parent = self.path[-1]
        parent.childs.pop(parent.childs.index(self))


class Directory(Node):
    def __init__(self, fs: MemSys, path: list[Node], name: str):
        if '/' in name:
            raise ValueError(f"Directory name contains {'/'}")

        super().__init__(path, name)
        self.childs = []
        self.fs = fs

    def __repr__(self):
        return f"<DIR | Path: {'/'.join([d.name for d in self.path]) if self.path else ''}/[ {self.name} ]>"

    def move(self, filename: str, destination: str):
        dest_dir = self.fs.get_node(destination)

        target = None

        for c in self.childs:
            if c.name == filename:
                target = c

        if not dest_dir or not isinstance(dest_dir, Directory):
            raise ValueError("Wrong destination path")

        self.childs.remove(target)
        dest_dir.childs.append(target)

    def is_create_file(self, new_file_name: str) -> bool:
        if len(self.childs) == DIR_MAX_ELEMS:
            print(f"Directory can't contain more than {DIR_MAX_ELEMS} nodes")

        for child in self.childs:
            if child.name == new_file_name:
                print("File with that name already exists!")

        return True

    def create_directory(self, name: str) -> Directory:
        self.is_create_file(name)
        self.childs.append(Directory(self.fs, self.path + [self], name))

    def create_binary_file(self, name: str, information: str) -> BinaryFile:
        self.is_create_file(name)

        file = BinaryFile(self.path + [self], name, information)
        self.childs.append(file)

        return file


    def create_log_file(self, name: str, information: str = None) -> LogFile:
        self.is_create_file(name)

        file = LogFile(self.path + [self], name, information)
        self.childs.append(file)

        return file

    def create_buffer(self, name: str) -> Buffer:
        self.is_create_file(name)

        file = Buffer(self.path + [self], name)
        self.childs.append(file)

        return file

    def print_ele(self, lvl=0) -> None:
        for child in self.childs:
            print("   "*(lvl+1) + child.name)

            if isinstance(child, Directory):
                child.print_ele(lvl+1)

    def find_node(self, path):
        expect_dir_name = path.split('/')[0]
        result = None

        if expect_dir_name == '.':
            result = self
        elif expect_dir_name == '..':
            result = self.path[-1]
        elif expect_dir_name == '~':
            result = self.fs.root

        for c in self.childs:
            if c.name == expect_dir_name:
                result = c

        if '/' in path:
            return result.find_node('/'.join(path.split('/')[1:]))
        else:
            return result


class BinaryFile(Node):
    def __init__(self, path: list[Node], name: str, information: str):
        super().__init__(path, name)
        self.information = information

    def read(self) -> None:
        return self.information


class LogFile(Node):
    def __init__(self, path: list[Node], name: str, information: str = ""):
            
        super().__init__(path, name)
        self.information = information

    def read(self) -> str:
        return self.information

    def append(self, information: str) -> str:
        self.information += information


class Buffer(Node):
    def __init__(self, path: list[Node], name: str):
        super().__init__(path, name)
        self.items = []

    def push(self, element: Any) -> bool:
        if len(self.items) == MAX_BUF_FILE_SIZE:
            raise ValueError("BufferFile is full")

        self.items.append(element)

    def pop(self) -> bool:
        if len(self.items) == 0:
            raise ValueError("the BufferFile is empty")

        return self.items.pop()
