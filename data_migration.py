#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from microface import microface


def uploadAllModelToDb():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'm1cr0face.settings'
                          )
    known_faces_path = 'known_faces_import/'
    for f in os.listdir(known_faces_path):
        if os.path.isfile(known_faces_path + f):
            data = f.split('_')
            print ('For user: ', data[1])
            microface.insertBlobToDb(emp_code=data[1],
                    face_model=known_faces_path + f)


if __name__ == '__main__':
    uploadAllModelToDb()
