#!/usr/bin/env python3
# coding=utf-8
# avatar_init.py

import os
import cv2
import base64

from hkprofile.models import db, Avatar, PersonInfo
from hkprofile import create_app


def image_to_base64(filename):
    image_type = filename.split('.')[:-1].lower()
    # convert the image type to png
    if image_type != 'png':
        pngname = ''.join(filename.split('.')[0:-1]) + '_c.png'
        img = cv2.imread(filename)
        cv2.imwrite(pngname, img)
    with open(pngname, 'rb') as f:
        base64_data = base64.b64encode(f.read())
        return base64_data.decode()


if __name__ == '__main__':
    app = create_app('hkprofile.config.ProdConfig')
    app.app_context().push()
    path = r'./testimg/'
    new_path = r'./testimg/png/'
    file_list = os.listdir(path)
    for filename in file_list:
        if os.path.isfile(path+filename):
            person_id = int(filename.split('.')[0].split('_')[0])
            print(person_id)
            filetype = filename.split('.')[-1].lower()
            if filetype != 'png':
                pngname = new_path + filename.split('.')[0] + '_c.png'
                img = cv2.imread(path + filename)
                cv2.imwrite(pngname, img)
            else:
                pngname = path + filename
            with open(pngname, 'rb') as f:
                base64_data = base64.b64encode(f.read())
            person_avatar = 'data:image/png;base64,%s' % base64_data.decode()

        p = PersonInfo.query.get(person_id)
        a = Avatar(person_avatar)
        p.avatar.append(a)
        db.session.commit()
