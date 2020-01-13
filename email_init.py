#!/usr/bin/env python3
# coding=utf-8
# email_init.py

import email
import re
from bs4 import BeautifulSoup
from datetime import datetime, tzinfo, timedelta, timezone
from dateutil.parser import parse


def decode_str(s):
    value, charset = email.header.decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value


def get_subject(msg):
    '''
    get the email subject decoded
    :param msg:
    :return: subject in plain text
    '''
    s = msg.get('subject')
    if s:
        s_decoded = email.header.decode_header(s)
        return s_decoded[0][0].decode(s_decoded[0][1], 'ignore')
    else:
        return None


def get_sendtime(msg):
    if 'date' in msg:
        return parse(msg.get('date'))
    else:
        return None


def get_mainbody(msg):
    m = msg.get_payload(decode=True).strip()
    return m


def email_init(emlfile):
    with open(emlfile, 'r') as eml:
        msg = email.message_from_file(eml)
        print([x for x in msg])
        subject = get_subject(msg)
        sendtime = get_sendtime(msg)
        print(sendtime)
        f = email.utils.parseaddr(msg.get('from'))
        t = email.utils.parseaddr(msg.get('to'))
        maintype = msg.get_content_maintype()
        if maintype == 'text':
            print(msg.get_payload())
        elif maintype == 'multipart':
            for part in msg.get_payload():
                print(part.get_content_maintype())
                if part.get_content_maintype() == 'text':
                    mail_content = part.get_payload(decode=True).strip().decode('gbk','ignore')
        s = BeautifulSoup(mail_content, features="html.parser").get_text()
        s = re.sub('[\t*\n]+', '\n', s)


        s = '{}, {}, {}, "{}"'.format(subject, f, t, s)
        with open(r'test.txt', 'w', encoding='utf8') as f:
            f.writelines(s)


if __name__ == '__main__':
    email_init(r'./email/01.eml')