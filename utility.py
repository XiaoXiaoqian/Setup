#!/usr/bin/env python2
"""
@author: Xiaoqian Xiao

Created on Mon Nov 27 16:14:44 2017
"""

import os, sys, tarfile

def extract(tar_url, extract_path='.'):
    print tar_url
    #tar = tarfile.open(tar_url, 'r')
    for item in tar:
        #tar.extract(item, extract_path)
        if item.name.find(".tgz") != -1 or item.name.find(".tar") != -1:
            tar.extract(item, extract_path + "/" + item.name[:item.name.rfind('/')])