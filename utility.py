#!/usr/bin/env python2
"""
@author: Xiaoqian Xiao
use 2 because of dcmstack
Created on Mon Nov 27 16:14:44 2017
"""
#%reset
import os, sys, tarfile, json, shutil
def untar_tgz(root, extract_path='.'):   
    for path, subdirs, files in os.walk(root):
        for filename in files:
            filepath = os.path.join(path, filename)
            if filepath is root:
                resultpath = extract_path
            else:
                resultpath = os.path.join(extract_path, path[path.rfind(root)+len(root)+1:])
            print resultpath
            mkdir(resultpath)
            if tarfile.is_tarfile(filepath):
                tar = tarfile.open(filepath, 'r:*')
                for member in tar:
                    tar.extract(member, resultpath)                    
def mkdir(targetdir):
    while not os.path.isdir(targetdir):
        os.makedirs(targetdir)        
def write_json(fname, meta_dict, overwrite=False):
    """
    Write a dictionary to a JSON file. Account for overwrite flag
    :param fname: string
        JSON filename
    :param meta_dict: dictionary
        Dictionary
    :param overwrite: bool
        Overwrite flag
    :return:
    """
    if os.path.isfile(fname):
        if overwrite:
            print('    Overwriting previous %s' % os.path.basename(fname))
            create_file = True
        else:
            print('    Preserving previous %s' % fname)
            create_file = False
    else:
        print('    Creating new %s' % os.path.basename(fname))
        create_file = True
    if create_file:
        with open(fname, 'w') as fd:
            json.dump(meta_dict, fd, indent=4, separators=(',', ':'))        
def read_json(fname):
    """
    Safely read JSON sidecar file into a dictionary
    :param fname: string
        JSON filename
    :return: dictionary structure
    """
    try:
        fd = open(fname, 'r')
        json_dict = json.load(fd)
        fd.close()
    except:
        print('*** JSON sidecar not found - returning empty dictionary')
        json_dict = dict()
    return json_dict

def copy(file1, file2, overwrite=False):
    """
    Copy file accounting for overwrite flag
    :param file1: str
    :param file2: str
    :param overwrite: bool
    :return:
    """
    if os.path.isfile(file2):
        if overwrite:
            print('    Overwriting previous %s' % os.path.basename(file2))
            create_file = True
        else:
            print('    Preserving previous %s' % os.path.basename(file2))
            create_file = False
    else:
        print('    Copying %s to %s' % (os.path.basename(file1), os.path.basename(file2)))
        create_file = True

    if create_file:
        shutil.copy(file1, file2)

dict_subID = dict()
dict_subID['20170414'] = 'sub-001_ses-baseline'
dict_subID['20170425'] = 'sub-001_ses-1w'
dict_subID['20170601'] = 'sub-002_ses-baseline'
dict_subID['20170612'] = 'sub-002_ses-1w'
dict_subID['20170710'] = 'sub-002_ses-1m'
dict_subID['20170914'] = 'sub-003_ses-baseline'
dict_subID['20170925'] = 'sub-003_ses-1w'
#subID['20170528'] = '004'
#subID['20170605'] = '004'
#subID['20170706'] = '004'
dict_subID['20170717'] = 'sub-004_ses-baseline'
dict_subID['20170724'] = 'sub-004_ses-1w'
dict_subID['20170821'] = 'sub-004_ses-1m'
#subID['20170724'] = '011'
#subID['20170731'] = '011'
#subID['20170724'] = '011'
dict_subID['20170811'] = 'sub-011_ses-baseline'
dict_subID['20170819'] = 'sub-011_ses-1w'
dict_subID['20170918'] = 'sub-011_ses-1m'
#subID['20170805'] = '013'
#subID['20170811'] = '014'
#subID['20170819'] = '014'
dict_subID['20170923'] = 'sub-014_ses-baseline'
dict_subID['20170930'] = 'sub-014_ses-1w'
dict_subID['20170820'] = 'sub-016_ses-baseline'
dict_subID['20170827'] = 'sub-016_ses-1w'
dict_subID['20170909'] = 'sub-018_ses-baseline'
dict_subID['20170916'] = 'sub-018_ses-1w'
dict_subID['20170828'] = 'sub-019_ses-baseline'
dict_subID['20170905'] = 'sub-019_ses-1w'
dict_subID['20171002'] = 'sub-019_ses-1m'
#subID['20170908'] = '021_sec-pre'
#dict_subID['20170910'] = 'sub-021_ses-baseline'
#dict_subID['20170917'] = 'sub-021_ses-1w'
dict_subID['20170929'] = 'sub-024_ses-baseline'
dict_subID['20171007'] = 'sub-024_ses-1w'
dict_subID['20171104'] = 'sub-024_ses-1m'
dict_subID['20171208'] = 'sub-026_ses-baseline'
dict_subID['20171218'] = 'sub-026_ses-1w'
#dict_subID['20171013'] = 'sub-021_ses_1m' 
#dict_subID['20171021'] = 'sub-021_ses_1w'
#20171111	021 Scan
#20171111	021 Scan
#20171020	blind p001 GK Pre scan
#20171031	blind p001 GK post scan
#20171125	blind p001 One month scan


#def gen_config():
    

###still working on
#def clear_dicoms(item_dicoms):
 #   """Ensures DICOM directories are safely cleared after reading the header info"""
 #   try:
 #       tmp = Path(op.commonprefix(item_dicoms)).parents[1]
 #   except IndexError:
 #       return
 #   if (str(tmp.parent) == tempfile.gettempdir()
 #       and str(tmp.stem).startswith('heudiconvDCM')
 #       and op.exists(str(tmp))):
        # clean up directory holding dicoms
 #       shutil.rmtree(str(tmp))
##note        
#20170717_0651_15493 no dicom
#20170909_0831_15984 only T1
