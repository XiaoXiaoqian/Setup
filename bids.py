#!/usr/bin/env python2
"""
@author: Xiaoqian Xiao
Deal with transferring to BIDS
**refer heudiconv
Created on Mon Nov 27 13:33:34 2017
"""
from dicom_xxq import *
from utility import *
basedir = '/Users/xiaoqian/Projects'

#basedir = '/Users/xiaoqian/Box/Xiaoqian_Externally_Shareable_Files/Projects'
ProjectName = 'aTBS'
rawdir = os.path.join(basedir, ProjectName, 'raw')
untardir = os.path.join(basedir, ProjectName, 'untar')

#untardir1 = os.path.join(basedir, ProjectName,'untar/20171218_0653_16703')
untar_tgz(rawdir, untardir)
get_scan_info(untardir, basedir)
