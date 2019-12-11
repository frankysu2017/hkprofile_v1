#!/usr/bin/env python3
# coding=utf-8


import sqlite3
from flask import g


def get_db():
    if 'db' not in g:
        print
        g.db = sqlite3.connect('./data.db')
    return g.db
 
 
def close_db(e=None):
    db = g.pop('db', None)
 
    if db is not None:
        db.close()


if __name__ == "__main__":
    db = sqlite3.connect('./data.db')
    cur = db.cursor()
    for i in range(100):
        cur.execute(
            'INSERT INTO person (cn_name, en_name, picture, gender, birthdate, id_num, permit_num, passort, home_address, post_address, company_address, party, occupation, private_phone, company_phone, fax, email, internet_account, homepage, bank_account, other_number, family, hobby, experience, event, stain) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (i, i, i, i, i, i, i, i, i, i, i, i, i, i, i, i, i, i, i, i, i, i, i, i, i, i)
        )
    db.commit()