import os

import pytest
from MemSys import MemSys, Node, Directory, BinaryFile, LogFile, Buffer


def test_get_index(client):
    #  Read directory file
    ms = MemSys()
    ms.create_directory('.', "Dir_1")
    ms.create_directory('.', "Dir_2")
    ms.create_directory('.', "Dir_3")
    ms.create_directory('./Dir_1', "Dir_11")
    ms.create_directory('./Dir_1', "Dir_12")
    ms.create_directory('./Dir_2', "Dir_21")
    ms.create_directory('./Dir_2', "Dir_22")

    list_response = client.get("/index?path=Dir_1")
    print(list_response.data)
    assert list_response.status_code == 200
    print('The Dir_1 directory should include two new files: ')

    list_response = client.get("/index?path=Dir_2")
    print('The Dir_2 directory should include two new files: ')
    print(list_response.data)
    assert "Dir_21" in str(list_response.data)
    assert "Dir_22" in str(list_response.data)


# create a file
def test_create_directory(client):
    print('\n')
    response = client.get("/directory")
    assert response.status_code == 200
    print(response.data)
    assert response.data == b'<DIR | Path: /[ ~ ]>'


# Create binaries
def test_create_binaryfile(client):
    res = client.post("/binaryfile", data={"path": ".", "name": "file.bin", "info": "Dummy info"})
    print()
    assert res.status_code == 200
    print('The path of binary file:')
    assert res.data == b'./file.bin:Dummy info'
    response = client.get("/binaryfile?info=Dummy info")
    print('Confirm the file type created: \n')
    print(response.data)
    assert response.data == b'Dummy info'


#  Create Log file
def test_create_logtextfile(client):
    res = client.get("/logtextfile?info=Log info")
    client.post("/logtextfile", data={"path": ".", "name": "file.log", "info": "Log info"})
    print('Confirm the file type created: \n')
    response = res.data
    assert response == b'Log info'


# create buffer file
def test_create_bufferfile(client):
    assert client.get("/bufferfile?item=file.buf").status_code == 200
    res = client.post("/bufferfile", data={"name": "file.buf", "path": "."})
    print(res.data)
    response = res.data
    assert response == b'./file.buf'


def test_move(client):
    # File move
    # create file called 'Filedummy.buf'
    re = client.post("/bufferfile", data={"name": "Filedummy.buf", "path": "."})
    print(re.data)
    # move 'Filedummy.buf' to 'Dir_1'
    response = client.put("/index", data={"src": "Filedummy.buf", "dest": "Dir_1"})
    print(response.data)
    index_response = os.listdir('Dir_1')
    print(index_response)
    assert response.status_code == 200
    assert response.data == b'Dir_1andFiledummy.buf'
    print('Confirm that there is the object file in "Dir_1"')
    assert "Filedummy.buf" in index_response


def test_delete(client):
    # File delete
    client.post("/bufferfile", data={"name": "Dummy.buf", "path": "."})

    index_response = os.listdir('Dir_1')
    print('\n The directory in the current folder "Dir_1" is : ')
    print(index_response)
    assert "Filedummy.buf" in index_response
    response_delete = client.delete("/index?name=Dir_1/Filedummy.buf")
    index_response = os.listdir('Dir_1')
    print('After deletion:')
    assert "Filedummy.buf" not in index_response
    print(index_response)
    print(response_delete.data)
    assert response_delete.status_code == 200


def test_delete2(client):
    client.put("/index", data={"src": "Dummy.buf", "dest": "Dir_1"})
    client.delete("/index?name=Dir_1/Dummy.buf")
    index_response = os.listdir('Dir_1')
    assert "Dummy.buf" not in index_response


def test_binaryfile_read(client):
    #  Binary file read file
    client.post("/binaryfile", data={"path": ".", "name": "dummy.bin", "info": "some info"})
    response = client.get("/binaryfile?info=some info")
    print(response.data)
    assert response.status_code == 200
    assert response.data == b'some info'


def test_buffer_pop(client):
    print('Storage of test data')
    test1 = client.put("/bufferfile", data={"path": "Dir_2", "item": "test1"})
    test2 = client.put("/bufferfile", data={"path": "Dir_2", "item": "test2"})
    test3 = client.put("/bufferfile", data={"path": "Dir_2", "item": "test3"})
    print('Testing')
    assert test1.data == b"test1"
    assert test2.data == b"test2"
    assert test3.data == b"test3"


def test_buffer_push(client):
    print('Storage of test data: ')
    client.post("/bufferfile", data={"name": "DUMMY.buf", "path": "."})
    client.put("/bufferfile", data={"path": "dummy.buf", "item": "one"})
    client.put("/bufferfile",  data={"path": "dummy.buf", "item": "two"})

    response = client.get("/bufferfile?item=two")
    print(response.data)
    print('Storage succeeded !')
    assert len(response.data) == 3






