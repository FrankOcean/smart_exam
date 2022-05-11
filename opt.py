# -*- coding: utf-8 -*-
# @Author : PuYang
# @Time   : 2022/5/8
# @File   : opt.py
import os

host = '124.70.177.168'             # 设置图片返回的域名前缀
port = 5000                         # 填写端口
image_c = 1024                      # 图片上传大小限制
UPLOAD_FOLDER = 'static/image/'     # 设置上传文件的目录
RESULT_FOLDER = 'static/'     # 设置上传文件的目录
image_url = "http://{}:{}/image/".format(host, port) # 设置图片返回的域名
ALLOW_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'JPG', 'PNG', 'gif', 'GIF']) # 设置允许上传的文件格式

basedir = os.path.abspath(os.path.dirname(__file__))