#!/usr/bin/env python2
"""
@author: Xiaoqian Xiao
Dicom related
**refer heudiconv
"""
import os
import os.path as op
import logging
import re
from collections import OrderedDict
from datetime import datetime
import csv
from random import sample
from glob import glob

import dicom as dcm
import dcmstack as ds

#from .parser import find_files
#from .utils import (load_json, save_json, create_file_if_missing,
#                    json_dumps_pretty, set_readonly, is_readonly)
           
def get_scan_info(root):
    """
    Parameters:
    item
    ---------------------------------------------------------------------------
    Returns:
    row: list
        [ISO acquisition time, performing physician name, random string]
    """
    for path, subdirs, files in os.walk(root):
        dcm_fn = files[-1]
    mw = ds.wrapper_from_data(dcm.read_file(dcm_fn,
                                            stop_before_pixels=True,
                                            force=True))
    dcminfo = mw.dcm_data
    # MG
    try:
        TR = float(dcminfo.RepetitionTime) / 1000.
    except (AttributeError, ValueError):
        TR = -1
    try:
        TE = float(dcminfo.EchoTime)
    except (AttributeError, ValueError):
        TE = -1
    try:
        refphys = str(dcminfo.ReferringPhysicianName)
    except AttributeError:
        refphys = ''
    try:
        image_type = tuple(dcminfo.ImageType)
    except AttributeError:
        image_type = ''
    try:
        series_desc = dcminfo.SeriesDescription
    except AttributeError:
        series_desc = ''    

    motion_corrected = ('moco' in dcminfo.SeriesDescription.lower()
                           or 'MOCO' in image_type)
    
    if dcminfo.get([0x18,0x24], None):
            # GE and Philips scanners
            sequence_name = dcminfo[0x18,0x24].value
    elif dcminfo.get([0x19, 0x109c], None):
        # Siemens scanners
        sequence_name = dcminfo[0x19, 0x109c].value
    else:
        sequence_name = 'Not found'
    
    info = SeqInfo(
            total,
            op.split(series_files[0])[1],
            series_id,
            op.basename(op.dirname(series_files[0])),
            '-', '-',
            size[0], size[1], size[2], size[3],
            TR, TE,
            dcminfo.ProtocolName,
            motion_corrected,
            'derived' in [x.lower() for x in dcminfo.get('ImageType', [])],
            dcminfo.get('PatientID'),
            dcminfo.get('StudyDescription'),
            refphys,
            dcminfo.get('SeriesDescription'),
            sequence_name,
            image_type,
            accession_number,
            # For demographics to populate BIDS participants.tsv
            dcminfo.get('PatientAge'),
            dcminfo.get('PatientSex'),
            dcminfo.get('AcquisitionDate'),
        )
    
    subID = re.split(r'[_|@|/]', dcminfo.PatientName)[0].split('s')[-1]
    phase = re.split(r'[_|@|/]', dcminfo.PatientName)[1]
    projectName = re.split(r'[_|@|/]', dcminfo.PatientName)[-1]
    scanType = re.split(r'[\s]', dcminfo.SeriesDescription)[0]
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    date = dcmInfo.ContentDate
    time = dcmInfo.ContentTime.split('.')[0]
    td = time + date
    acq_time = datetime.strptime(td, '%H%M%S%Y%m%d').isoformat()





    row = [acq_time, PatientID]
    # empty entries should be 'n/a'
    # https://github.com/dartmouth-pbs/heudiconv/issues/32
    row = ['n/a' if not str(e) else e for e in row]
    return row