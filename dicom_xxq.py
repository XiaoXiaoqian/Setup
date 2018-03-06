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
from utility import *
#from .parser import find_files
#from .utils import (load_json, save_json, create_file_if_missing,
 #                  json_dumps_pretty, set_readonly, is_readonly)
           

BIDSVersion = '1.0.2'
License = 'test by XXQ'
Authors = ['test by XXQ']
Acknowledgements = 'test by XXQ'
HowToAcknowledge = 'test by XXQ'
Funding = 'test by XXQ'
def get_scan_info(root, basedir):
    """
    Parameters:
    item
    ---------------------------------------------------------------------------
    Returns:
    row: list
        [ISO acquisition time, performing physician name, random string]
    """
    for path, subdirs, files in os.walk(root):
        if path.split('_')[-1] == 'dicoms' and "Save" not in re.split(r'[_|@|/]', path) \
        and "calibration" not in re.split(r'[_|@|/]', path) \
        and "Loc" not in re.split(r'[_|@|/]', path) \
        and "Processed" not in re.split(r'[_|@|/]', path):
            if files:
                niiDir = path.replace(path.split('/')[-1], "").replace('untar', 'raw')
                niifiles = glob(os.path.join(niiDir, '*.nii.gz'))
                dcm_files = glob(op.join(path,'*.dcm'))
                dcm_fn = dcm_files[0]
                dcm_filepath = os.path.join(path, dcm_fn)
                mw = ds.wrapper_from_data(dcm.read_file(dcm_filepath,
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

                projectName = re.split(r'[_|@|/]', dcminfo.PatientID)[-1]
                projectPath = os.path.join(basedir, projectName)
                mkdir(projectPath)
                targetPath = os.path.join(projectPath, 'source')
                mkdir(targetPath)
                date = dcminfo.ContentDate
                time = dcminfo.ContentTime.split('.')[0]
                time2 = dcminfo.StudyTime.split('.')[0]
                td = time + date
                acq_time = datetime.strptime(td, '%H%M%S%Y%m%d').isoformat()            
                key_subID = date
                key_subID2 = date+'_'+time2[0:4]
                if key_subID in dict_subID.keys():
                    info_subID = dict_subID[key_subID]
                    subPrefix = info_subID
                    subID = re.split(r'[_]', info_subID)[0].split('-')[1]
                    subDir = os.path.join(targetPath, 'sub-'+subID)
                    mkdir(subDir)
                    phase = re.split(r'[_]', info_subID)[1].split('-')[1]
                    secDir = os.path.join(subDir, 'ses-'+phase)
                    mkdir(secDir)
                    print(secDir)
                elif key_subID2 in dict_subID.keys():
                    info_subID = dict_subID[key_subID2]
                    subPrefix = info_subID
                    subID = re.split(r'[_]', info_subID)[0].split('-')[1]
                    subDir = os.path.join(targetPath, 'sub-'+subID)
                    mkdir(subDir)
                    phase = re.split(r'[_]', info_subID)[1].split('-')[1]
                    secDir = os.path.join(subDir, 'ses-'+phase)
                    mkdir(secDir)
                    print(secDir)
                else: 
                    print('no such key')
                    subID = re.split(r'[_|@|/]', dcminfo.PatientID)[0].split('s')[-1]
                    subDir = os.path.join(targetPath, subID)
                    mkdir(subDir)
                    phase = re.split(r'[_|@|/]', dcminfo.PatientID)[1]
                    secDir = os.path.join(subDir, subID)
                    mkdir(secDir)
                    print(secDir)
                    subPrefix = 'sub-'+subID+'_ses-'+phase


                subAge = int(dcminfo.PatientAge.split('Y')[0])
                subSex = dcminfo.PatientSex

                #scanType = re.split(r'[\s]', dcminfo.SeriesDescription)[0] 
                scanType = dcminfo[0x19109e].value
                # Fieldmap; EffectiveEchoSpacing and TotalReadoutTime
                ETL = dcminfo.EchoTrainLength
                PEbandwidth = float(dcminfo.PixelBandwidth)
                ACCFactor = 3#have not figure out how to read directlly from dcm. right now read from nii header
                #EffectiveEchoSpacing = 1 / (PEbandwidth * (ETL - 1) * ACCFactor)
                #TotalReadoutTime = 1/PEbandwidth 
                taskName = dcminfo.SeriesDescription.split(' ')[0]

                #Build the info dics and save them
                Dataset_Description = dict()
                Dataset_Description['Name'] = projectName
                Dataset_Description['BIDSVersion'] = BIDSVersion
                Dataset_Description['License'] = License
                Dataset_Description['Authors'] = Authors
                Dataset_Description['Acknowledgements'] = Acknowledgements
                Dataset_Description['HowToAcknowledge'] = HowToAcknowledge
                Dataset_Description['Funding'] = Funding
                Dataset_Description['InstitutionName'] = dcminfo.InstitutionName
                Dataset_Description['Manufacturer'] = dcminfo.Manufacturer
                Dataset_Description['ManufacturersModelName'] = dcminfo.ManufacturersModelName
                fname = os.path.join(targetPath, 'dataset_description.json') 
                write_json(fname, Dataset_Description, 'TRUE')
                #Dataset_Description['Session'] = phase
                Dataset_Description['SubID'] = subID
                Dataset_Description['SubAge'] = subAge
                Dataset_Description['SubSex'] = subSex
                fname = os.path.join(subDir, 'dataset_description.json') 
                write_json(fname, Dataset_Description, 'TRUE')            
                if scanType == 'EFGRE3D': 
                    Anatomy_Info = dict()
                    Anatomy_Info['ScanType'] = 'T1'
                    Anatomy_Info['SeriesDescription'] = dcminfo.SeriesDescription
                    Anatomy_Info['AcquisitionMatrix'] = dcminfo.AcquisitionMatrix
                    Anatomy_Info['RepetitionTime'] = TR
                    Anatomy_Info['TE'] = TE
                    Anatomy_Info['FlipAngle'] = int(dcminfo.FlipAngle)
                    Anatomy_Info['InstitutionName'] = dcminfo.InstitutionName
                    Anatomy_Info['Manufacturer'] = dcminfo.Manufacturer
                    Anatomy_Info['ManufacturersModelName'] = dcminfo.ManufacturersModelName
                    Anatomy_Info['AcqTime'] = acq_time
                    anatdir = os.path.join(secDir, 'anat')
                    mkdir(anatdir)
                    for i in niifiles:
                        copy(i, os.path.join(anatdir, subPrefix+'_T1w.nii.gz'))
                    fname = os.path.join(anatdir, subPrefix+'_T1w.json') 
                    write_json(fname, Anatomy_Info, 'TRUE')
                elif scanType == '3DFSE': 
                    Anatomy_Info = dict()
                    Anatomy_Info['ScanType'] = 'T2'
                    Anatomy_Info['SeriesDescription'] = dcminfo.SeriesDescription
                    Anatomy_Info['AcquisitionMatrix'] = dcminfo.AcquisitionMatrix
                    Anatomy_Info['RepetitionTime'] = TR
                    Anatomy_Info['TE'] = TE
                    Anatomy_Info['FlipAngle'] = int(dcminfo.FlipAngle)
                    Anatomy_Info['InstitutionName'] = dcminfo.InstitutionName
                    Anatomy_Info['Manufacturer'] = dcminfo.Manufacturer
                    Anatomy_Info['ManufacturersModelName'] = dcminfo.ManufacturersModelName
                    Anatomy_Info['AcqTime'] = acq_time
                    anatdir = os.path.join(secDir, 'anat')
                    mkdir(anatdir)
                    for i in niifiles:
                        copy(i, os.path.join(anatdir, subPrefix+'_T2w.nii.gz'))
                    fname = os.path.join(anatdir, subPrefix+'_T2w.json') 
                    write_json(fname, Anatomy_Info, 'TRUE')    
                elif scanType == 'EPI':
                    slice_times = get_slice_timing(root)
                    Func_Info = dict()
                    Func_Info['ScanType'] = 'Func'
                    Func_Info['SeriesDescription'] = dcminfo.SeriesDescription
                    Func_Info['AcquisitionMatrix'] = dcminfo.AcquisitionMatrix
                    Func_Info['RepetitionTime'] = TR
                    Func_Info['TE'] = TE
                    Func_Info['FlipAngle'] = int(dcminfo.FlipAngle)
                    Func_Info['SliceTiming'] = slice_times
                    Func_Info['ACCFactor'] = ACCFactor
                    Func_Info['InstitutionName'] = dcminfo.InstitutionName
                    Func_Info['Manufacturer'] = dcminfo.Manufacturer
                    Func_Info['ManufacturersModelName'] = dcminfo.ManufacturersModelName
                    Func_Info['AcqTime'] = acq_time
                    Func_Info['TaskName'] = taskName
                    funcdir = os.path.join(secDir, 'func')
                    mkdir(funcdir)
                    for i in niifiles:
                        copy(i, os.path.join(funcdir, subPrefix+'_task-'+taskName+'_bold.nii.gz'))
                    fname = os.path.join(funcdir, subPrefix+'_task-'+taskName+'_bold.json') 
                    write_json(fname, Func_Info, 'TRUE')
                elif scanType == 'Fieldmap':
                    Fieldmap_Info = dict()
                    Fieldmap_Info['ScanType'] = 'Fieldmap'
                    Fieldmap_Info['SeriesDescription'] = dcminfo.SeriesDescription
                    Fieldmap_Info['AcquisitionMatrix'] = dcminfo.AcquisitionMatrix
                    Fieldmap_Info['RepetitionTime'] = TR
                    Fieldmap_Info['TE'] = TE
                    Fieldmap_Info['FlipAngle'] = int(dcminfo.FlipAngle)
                    Fieldmap_Info['ACCFactor'] = ACCFactor
                    Fieldmap_Info['EffectiveEchoSpacing'] = EffectiveEchoSpacing
                    Fieldmap_Info['phaseEncodeDirection'] = phaseEncodeDirection                
                    Fieldmap_Info['InstitutionName'] = dcminfo.InstitutionName
                    Fieldmap_Info['Manufacturer'] = dcminfo.Manufacturer
                    Fieldmap_Info['ManufacturersModelName'] = dcminfo.ManufacturersModelName
                    Fieldmap_Info['AcqTime'] = acq_time
                    fpdir = os.path.join(secDir, 'fmap')
                    mkdir(fpdir)
                    for i in niifiles:
                        copy(i, os.path.join(fpdir, subPrefix+'_fmap.nii.gz'))
                    fname = os.path.join(fpdir, subPrefix+'_fmap.json') 
                    write_json(fname, Fieldmap_Info, 'TRUE') 
def get_slice_timing(root):
    for path, subdirs, files in os.walk(root):
        if files:
            dcm_files = glob(op.join(path,'*.dcm'))
            num_files = len(dcm_files)
            slice_time = [None]*num_files
            for i in range(num_files):
                dcm_fn = dcm_files[i]
                dcm_filepath = os.path.join(path, dcm_fn)
                mw = ds.wrapper_from_data(dcm.read_file(dcm_filepath,
                                                stop_before_pixels=True,
                                                force=True))
                dcminfo = mw.dcm_data   
                aquision_time = float(dcminfo.TriggerTime)/1000
                slice_time[i] = aquision_time
            return (slice_time)
        else:
            print('Nan file path')
