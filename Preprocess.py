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
import os.path as op
from glob import glob

remotehost = 'xiaoqian@cnic22.stanford.edu'
#remotedir = '/home/xiaoqian/Documents/nimsfs/raw/nolanw/atbs'
localdir = '/Users/xiaoqian/Projects/aTBS/raw'

for i in dict_subID:
    print (dict_subID[i])
    filename = os.path.join(remotedir, i+'*')
    os.system('scp -r "%s:%s" "%s"' % (remotehost, filename, localdir))

#two data sets were putting into open_atbs:20171208_0637_16657  20171209_0700_16665
#remotedir = '/home/xiaoqian/Documents/nimsfs/raw/nolanw/open_atbs'
#sfile = '20171208_0637_16657'
#filename = os.path.join(remotedir, sfile)
#os.system('scp -r "%s:%s" "%s"' % (remotehost, filename, localdir))
