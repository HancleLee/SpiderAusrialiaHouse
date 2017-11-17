#!/usr/bin/env python
# -*- coding:utf-8 -*-
import datetime
import os

def saveDic(dic, file_name, encode_type):
    if type(dic)==dict:
        try:
            dic_num = dic.__len__()
            file_path = str(createFile()) + "\\" + file_name + '.txt'
            file_path = file_path.replace("\\", "/")
            fp = open(file_path, "w+", encoding=encode_type)
            fp.write(str(dic))
            fp.close()
            return True

        except (IOError, ZeroDivisionError, FileNotFoundError) as e:
            print(e)
            return False
    else:
        return False


def saveLists(lists, file_name, encode_type):
    # print(lists.__len__())
    if type(lists)==list:
        try:
            # 保存到文件
            file_path = str(createFile()) + "\\" + file_name + '.txt'
            file_path = file_path.replace("\\", "/")
            fp = open(file_path , "w+", encoding=encode_type)
            fp.write(str(lists))
            fp.close()
            return True
        except (IOError ,ZeroDivisionError, FileNotFoundError) as e:
            print(e)
            return False

    else:
        return False


def createFile():
    date = datetime.datetime.now().strftime('%Y%m%d')
    path = os.getcwd() + "\\" + date
    path = path.replace("\\", "/")
    print(path)
    if os.path.exists(path):
        return path
    else:
        os.mkdir(path)
        return path



def saveStr(data, file_name, encode_type):
    if type(data)==str:
        try:
            file_path = str(createFile()) + "\\" + file_name + '.txt'
            file_path = file_path.replace("\\", "/")
            fp = open(file_path, "w+", encoding=encode_type)
            fp.write(data)
            fp.close()
            return True

        except (IOError, ZeroDivisionError, FileNotFoundError) as e:
            print(e)
            return False
    else:
        print("not str")
        return False

def saveFile(data, file_name, encode_type):
    print(type(data))
    if type(data) == str:
        return saveStr(data, file_name, encode_type)
    elif type(data) == dict:
        return saveDic(data, file_name, encode_type)
    elif type(data) == list:
        return saveLists(data, file_name, encode_type)
    else:
        try:
            dataStr = str(data)
            return saveStr(dataStr, file_name, encode_type)
        except (IOError, ZeroDivisionError, FileNotFoundError) as e:
            print(e)
            return False

def readFile(file_name):
    file_path = str(createFile()) + "/" + file_name + '.txt'
    try:
        file_object = open(file_path)
        all_the_text = file_object.read()
        return all_the_text
    except (IOError, ZeroDivisionError, FileNotFoundError) as e:
        print(e)
        return False

    finally:
        pass
        # print("file read erro")
        # return False
        # file_object.close()
