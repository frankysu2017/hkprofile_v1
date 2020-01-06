#!/usr/bin/env python3
# coding=utf-8

import cv2
import os
import base64
from db_conn import get_db
from flask import g
import sqlite3


def type_convert(filename):
    pngname = '/'.join(filename.split('/')[0:-1]) + '/' + filename.split('/')[-1].split('.')[0] + '_c.png'
    img = cv2.imread(filename)
    cv2.imwrite(pngname, img)


def insert_img(filename):
    person_id = filename.split('/')[-1].split('.')[0].split('_')[0]
    pic_ext = filename.split('.')[-1]
    print(person_id)
    db = sqlite3.connect('./data.db')
    #db.execute('UPDATE person SET picture=""')
    if pic_ext in ['png', 'PNG']:
        with open(filename, 'rb') as f:
            base64_data = base64.b64encode(f.read())
            s = base64_data.decode()
            db.execute("UPDATE person SET picture=?||'\n'||picture WHERE id=?", ('data:image/png;base64,%s'%s, person_id))
        db.commit()


if __name__ == "__main__":
    path = r'./testimg'
    files = [path+'/'+x for x in os.listdir(r'./testimg')]
    for file in files:
        print(file)
        id = int(file.split('/')[-1].split('.')[0].split('_')[0])
        type = file.split('.')[-1].lower()
        if type != 'png':
            newfile = ''.join(file.split('.')[0:-1]) + '_c.png'
        else:
            newfile = file
        print("id = {};\t type = {};\t filename = {}".format(id, type, newfile))