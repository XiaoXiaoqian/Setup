#!/usr/bin/env python2
"""
@author: Xiaoqian Xiao
Created on Mon Nov 27 16:14:44 2017
"""
%reset
import os, sys, tarfile
### fix the problem with subdir
def extract(root, extract_path='.'):   
    for path, subdirs, files in os.walk(root):
        for filename in files:
            filepath = os.path.join(path, filename)
            if filepath is root:
                resultpath = extract_path
            else:
                resultpath = os.path.join(extract_path, path[path.rfind(root)+len(root)+1:])
            print resultpath
            if not os.path.isdir(resultpath):
                os.makedirs(resultpath)
            if tarfile.is_tarfile(filepath):
                tar = tarfile.open(filepath, 'r:*')
                for member in tar:
                    tar.extract(member, resultpath)
            