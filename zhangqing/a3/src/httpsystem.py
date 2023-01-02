'''
  name:Zhang Qing
  ID:ass2
  Date:2023/1/1
  Task: Assignment_2
'''

import functools
import os
import shutil

from flask import Blueprint, flash, g, redirect, render_template, request, make_response
from flask import flash, url_for
from MemSys import MemSys, Node, Directory, BinaryFile, LogFile, Buffer

flasksys = Blueprint(' ', __name__)


@flasksys.route("/index", methods=["GET", "PUT", "DELETE"])
def index():  # root directory
    ms = MemSys()

    if request.method == "GET":
        #  Get the file list
        print('\n')
        path = request.args.get("path")
        index_response = os.listdir(path)
        indexlist = []
        for dir in index_response:
            temp = dir.split('\\')
            indexlist.append(temp[-1])
        #  Return to the target directory
        return indexlist

    elif request.method == "PUT":
        # Move command
        src = request.form.get("src")
        dest = request.form.get("dest")

        node = ms.get_node(src)

        de = Directory(ms, node, dest)

        if not src or not dest:
            return make_response({"status": "error", "message": "You need to specify src and dest to move elements!"},
                                 400)

        try:
            # de.move(src, dest)
            shutil.move(src, dest)
            return dest + 'and' + src
        except:
            shutil.move(src, dest)
            return dest + ' and ' + src

    elif request.method == "DELETE":
        # Delete Instruction
        name = request.args.get("name")

        try:
            ms.delete(name)
            return name

        except ValueError as e:
            return make_response({"status": "error", "message": str(e)}, 400)


@flasksys.route("/directory", methods=["GET", "POST"])
def directory():
    ms = MemSys()
    if request.method == "GET":
        #  Catalogue
        return ms.root.__str__()

    elif request.method == "POST":
        print()
        # Create the new folder
        path = request.form["path"]
        name = request.form["name"]
        error = None

        if not path:
            error = "Path is required."

        if not name:
            error = "Name is required."

        if error is not None:
            flash(error)

        try:
            ms.create_directory(path, name)

        except ValueError as e:
            return make_response({"status": "erorr", "message": str(e)}, 444)

        return path + '/' + name


@flasksys.route("/binaryfile", methods=["GET", "POST"])
def binary():
    ms = MemSys()
    if request.method == "GET":
        #  Read a binary file
        print()
        info = request.args.get("info")
        return info

    elif request.method == "POST":
        #  Create some binaries files
        path = request.form.get("path")
        name = request.form.get("name")
        info = request.form.get("info")

        if not path or not name:
            return make_response({"status": "error", "message": "Arguments path and name are required"}, 400)

        if not info:
            return make_response({"status": "error", "message": "Argument information is required"}, 400)

        try:

            ms.create_binary_file(path, name, info)

        except ValueError as e:
            return make_response({"status": "erorr", "message": str(e)}, 400)

        return path + '/' + name + ':' + info


@flasksys.route("/logtextfile", methods=["GET", "POST"])
def logfile():
    ms = MemSys()
    if request.method == "GET":
        info = request.args.get("info")
        #  Catalogue
        print()
        bin_file = ms.get_node(info)
        print(info)
        return info

    elif request.method == "POST":
        #  Create the log file
        path = request.form["path"]
        name = request.form["name"]
        info = request.form.get("info")
        error = None

        if not path:
            error = "Path is required."

        if not name:
            error = "Name is required."

        if not info:
            return make_response({"status": "error", "message": "Argument information is required"}, 400)

        if error is not None:
            flash(error)

        try:
            ms.create_log_file(path, name, info)
        except ValueError as e:
            return make_response({"status": "erorr", "message": str(e)}, 400)
        print()
        return path + '/' + name + ':' + info


@flasksys.route("/bufferfile", methods=["GET", "POST", "PUT"])
def bufferfile():
    ms = MemSys()
    if request.method == "GET":
        #  Read the binary file
        item = request.args.get("item")
        #  Catalogue
        print()
        return item

    elif request.method == "POST":
        #  Create binary file
        path = request.form["path"]
        name = request.form["name"]
        error = None

        if not path:
            error = "Path is required."

        if not name:
            error = "Name is required."

        if error is not None:
            flash(error)

        try:
            ms.create_buffer(path, name)
            ms.create_directory(path, name)

        except ValueError as e:
            return make_response({"status": "erorr", "message": str(e)}, 400)

        print()
        return path + '/' + name
    if request.method == "PUT":
        #  Storing information to binary files
        path = request.form.get("path")
        item = request.form.get("item")

        if not path or not item:
            return make_response({"status": "error", "message": "Arguments path and information is required"}, 400)

        return item


def login_required(view):

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("main_system.login"))

        return view(**kwargs)

    return wrapped_view
