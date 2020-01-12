#!/usr/bin/env python3
# coding=utf-8
# email_init.py

import email
import re
from bs4 import BeautifulSoup


def get_ctype(msg):
    ct = msg.get('Content-Type')
    print(ct)
    plain_flag = re.findall('text/(.*?);', ct)
    print(plain_flag)
    content_charset = re.findall('charset=(.*);?', ct)
    print(content_charset)
    if plain_flag:
        plain_flag = plain_flag[0]
    else:
        plain_flag = None
    if content_charset:
        content_charset = content_charset[0]
        if 'gb2312' in content_charset.lower():
            content_charset = 'gbk'
    else:
        content_charset = None
    return plain_flag, content_charset


def email_init(emlfile):
    with open(emlfile, 'r') as eml:
        msg = email.message_from_file(eml)
        subject = msg.get('subject')
        subject, charset = email.header.decode_header(subject)[0]
        if isinstance(subject, bytes):
            subject = subject.decode(charset, 'ignore')
        f = email.utils.parseaddr(msg.get('From'))
        t = email.utils.parseaddr(msg.get('to'))
        sender_name, f_charset = email.header.decode_header(f[0])[0]
        sender_box = f[1]
        if isinstance(sender_name, bytes):
            sender_name = sender_name.decode(f_charset, 'ignore')
        receiver_name, t_charset = email.header.decode_header(t[0])[0]
        receiver_box = t[1]
        if isinstance(receiver_name, bytes):
            receiver_name = receiver_name.decode(t_charset, 'ignore')
        maintype = msg.get_content_maintype()
        if maintype == 'text':
            plain_flag, content_charset = get_ctype(msg)
            mail_content = msg.get_payload(decode=True).strip().decode(content_charset)
            if plain_flag == 'html':
                mail_content = BeautifulSoup(mail_content, features='html.parser').body.get_text()
        elif maintype == 'multipart':
            print('it is multipart email')
            mail_content = ''
            for part in msg.get_payload():
                plain_flag, content_charset = get_ctype(part)
                if part.get_content_maintype() == 'text':
                    temp_content = part.get_payload(decode=True).strip().decode(content_charset)
                    if plain_flag == 'html':
                        pattern = re.compile('(.*)(<HTML>.*</HTML>)(.*)', flags=re.IGNORECASE)
                        pref, html, suf = re.search(pattern, temp_content).groups()
                        temp_content = pref + '\n' + BeautifulSoup(html, features='html.parser').body.get_text() + '\n' + suf
                mail_content += temp_content
                temp_content = ''
        #mail_content = re.sub('^[ ]*\n$', '', mail_content)
        mail_content = re.sub('\s*\n', '\n', mail_content)
    '''
    for k in msg.keys():
        print('{}: {}'.format(k, msg.get(k)))
        print('------------------------------------------------------')
    '''
    return sender_name, sender_box, receiver_name, receiver_box, subject, mail_content


if __name__ == '__main__':
    sn, sb, rn, rb, sub, mc = email_init(r'08.eml')
    with open(r'08.re', 'w', encoding='utf8') as f:
        f.writelines('"{}","{}","{}","{}","{}","{}"'.format(sn, sb, rn, rb, sub, mc))