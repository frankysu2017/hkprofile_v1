#!/usr/bin/env python3
# coding=utf-8
# email_init.py

import email
import re
from bs4 import BeautifulSoup
from dateutil.parser import parse


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
    mainbody = msg.get_payload(decode=True).strip().decode(msg.get_content_charset(), 'ignore')
    html_flag = re.search('text/(.*)', msg.get_content_type()).group(1).lower()
    if html_flag == 'html':
        prefix, html_text, suffix = re.search('(.*)(<html>.*</html>)(.*)', mainbody)

    mainbody = re.sub('[\n]+', '\n', mainbody)
    return mainbody


def get_sender(msg):
    sname, send_box = email.utils.parseaddr(msg.get('from'))
    if sname:
        sname = email.header.decode_header(sname)
        if isinstance(sname[0][0], bytes):
            send_name = sname[0][0].decode(sname[0][1], 'ignore')
        else:
            send_name = sname[0][0]
    else:
        send_name = None
    return send_name, send_box


def get_receiver(msg):
    rname, receive_box = email.utils.parseaddr(msg.get('to'))
    if rname:
        rname = email.header.decode_header(rname)
        if isinstance(rname[0][0], bytes):
            receive_name = rname[0][0].decode(rname[0][1], 'ignore')
        else:
            receive_name = rname[0][0]
    else:
        receive_name = rname
    return receive_name, receive_box


def email_init(emlfile):
    with open(emlfile, 'r') as eml:
        msg = email.message_from_file(eml)
        subject = get_subject(msg)
        send_time = get_sendtime(msg)
        send_name, send_box = get_sender(msg)
        receive_name, receive_box = get_receiver(msg)
        print('{}, {}, {}, {}, {}, {}'.format(send_name, send_box, receive_name, receive_box, send_time, subject))
        maintype = msg.get_content_maintype()
        if maintype == 'text':
            print('it is text')
            mail_content = get_mainbody(msg)
        elif maintype == 'multipart':
            print('it is multipart')
            mail_content = ''
            for part in msg.get_payload():
                if part.get_content_maintype() == 'text':
                    part_content = get_mainbody(part)
                else:
                    part_content = ''
                mail_content += part_content
            #print(mail_content)
        s = BeautifulSoup(mail_content, features="html.parser").get_text()
        s = re.sub('[\t*\n]+', '\n', s)


        with open(r'test.txt', 'w', encoding='utf8') as f:
            pass


if __name__ == '__main__':
    print('send_name, send_box, receive_name, receive_box, send_time, subject')
    #email_init(r'./email/01.eml')
    #email_init(r'./email/02.eml')
    email_init(r'./email/03.eml')
    #email_init(r'./email/04.eml')