# -*- coding: utf-8 -*-
# @Author : PuYang
# @Time   : 2022/5/5
# @File   : utils.py

import os

def deletehiddenfile_recursive(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.startswith('._'):
                os.remove(os.path.join(root, file))
                print(os.path.join(root, file))

if __name__ == '__main__':
    deletehiddenfile_recursive('.')