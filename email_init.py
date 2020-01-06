#!/usr/bin/env python3
# coding=utf-8
# email_init.py

import email
import re
import nltk
from bs4 import BeautifulSoup


def decode_str(s):
    value, charset = email.header.decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value


def email_init(emlfile):
    with open(emlfile, 'r') as eml:
        msg = email.message_from_file(eml)
        subject = msg.get('subject')
        subject = email.header.decode_header(subject)[0][0].decode('gbk','ignore')
        f = email.utils.parseaddr(msg.get('From'))
        t = email.utils.parseaddr(msg.get('to'))
        maintype = msg.get_content_maintype()
        if maintype == 'multipart':
            for part in msg.get_payload():
                if part.get_content_maintype() == 'text':
                    mail_content = part.get_payload(decode=True).strip().decode('gbk','ignore')
        s = BeautifulSoup(mail_content, features="html.parser").get_text()
        print(s)


        s = "{}, {}, {}".format(subject, f, t)
        with open(r'test.re', 'w') as f:
            f.writelines(s)


if __name__ == '__main__':
    email_init(r'test.eml')