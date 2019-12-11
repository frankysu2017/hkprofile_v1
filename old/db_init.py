#!/usr/bin/env python3
# coding=utf-8


import sqlite3


conn = sqlite3.connect('data.db')
cur = conn.cursor()


with open('create_table.sql') as f:
    cur.executescript(f.read())

conn.close()


