#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 20:02:44 2017
@author: xiaoqian
"""
#from NIMS to BSL
from utility import *
from pexpect import *

import os
import os.path as op
from glob import glob

remotehost = 'xiaoqian@cnic22.stanford.edu'
remotedir = '/home/xiaoqian/Documents/nimsfs/raw/nolanw/atbs'
localdir = '/Users/xiaoqian/Projects/aTBS/raw'

for i in dict_subID:
    print (dict_subID[i])
    filename = os.path.join(remotedir, i+'*')
    #os.system('scp -r "%s:%s" "%s"' % (remotehost, filename, localdir))
    child=spawn('scp -r "%s:%s" "%s"' % (remotehost,filename, localdir), timeout=21600)
    
    child.expect ("password")
    child.sendline ("!ddlswcg1H")
    child.read()
