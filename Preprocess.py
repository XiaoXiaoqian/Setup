#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 20:02:44 2017
@author: xiaoqian
"""
#from NIMS to BSL
from utility import *
#scp -r xiaoqian@cnic22.stanford.edu:/home/xiaoqian/Documents/nimsfs/raw/nolanw/atbs/$filename
#/Users/xiaoqian/Projects/atbs/raw
import os

remotehost = 'xiaoqian@cnic22.stanford.edu'
remotedir = '/home/xiaoqian/Documents/nimsfs/raw/nolanw/atbs'
localdir = '/Users/xiaoqian/Projects/aTBS/raw'

for i in dict_subID:
    print (dict_subID[i])
    filename = i
    os.system('scp -r "%s:%s/%s" "%s"' % (remotehost, remotedir, filename, localdir))
