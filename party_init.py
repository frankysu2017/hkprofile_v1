#!/usr/bin/env python3
# coding=utf-8
# party_init.py


def party_process(filename):
    with open(filename, 'r', encoding='utf8') as f:
        for line in f:
            record = line.replace('\n', '').split(',')
            id = record[0]
            p_tag = record[1].split('-')
            for item in p_tag:
                if item == '':
                    item = '未录入'
                print('id = {}; party = {}'.format(id, item))


if __name__ == '__main__':
    party_process(r'partytag.csv')