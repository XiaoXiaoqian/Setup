#!/usr/bin/env python2
"""
@author: Xiaoqian Xiao
use 2 because of dcmstack
Created on Mon Nov 27 16:14:44 2017
"""
#%reset
import os, sys, tarfile, json
from collections import namedtuple

SeqInfo = namedtuple(
    'SeqInfo',
    ['total_files_till_now',  # 0
     'example_dcm_file',      # 1
     'series_id',             # 2
     'unspecified1',          # 3
     'unspecified2',          # 4
     'unspecified3',          # 5
     'dim1', 'dim2', 'dim3', 'dim4', # 6, 7, 8, 9
     'TR', 'TE',              # 10, 11
     'protocol_name',         # 12
     'is_motion_corrected',   # 13
     'is_derived',            # 14
     'patient_id',            # 15
     'study_description',     # 16
     'referring_physician_name', # 17
     'series_description',    # 18
     'sequence_name',         # 19
     'image_type',            # 20
     'accession_number',      # 21
     'patient_age',           # 22
     'patient_sex',           # 23
     'date'                   # 24
     ]
)

DatasetDescription = namedtuple(
    'DatasetDescription',
    ['ProjectName',  # 0 name of the dataset
     'BIDSVersion',      # 1
     'License',             # 2
     'Authors',          # 3 List of individuals who contributed to the creation/curation of the dataset
     'Acknowledgements',          # 4 who should be acknowledge in helping to collect the data
     'HowToAcknowledge',          # 5 Instructions how researchers using this dataset should acknowledge the original authors. This field can also be used to define a publication that should be cited in publications that use the dataset
     'Funding', # 6 sources of funding (grant numbers)
     'ReferencesAndLinks',              # 7 a list of references to publication that contain information on the dataset, or links.
     'DatasetDOI',         # 8 the Document Object Identifier of the dataset
     'ManufacturersModelName', # 9 Manufacturer`s model name of the equipment that produced the composite instances. Corresponds to DICOM Tag 0008, 1090
     'StudyTime', # 10
     'PatientID',   # 11
     'PatientAge',  # 12
     'PatientSex'  # 13
     ]
)

TaskInfo = namedtuple(
    'TaskInfo',
    ['RepetitionTime', # 0 TR The time in seconds between the beginning of an acquisition of one volume and the beginning of acquisition of the volume following it (TR). Please note that this definition includes time between scans (when no data has been acquired) in case of sparse acquisition schemes. This value needs to be consistent with the ‘ pixdim[4] ’ field (after accounting for units stored in ‘ xyzt_units ’ field) in the NIfTI header.
     'EchoTime',  # 1 The echo time (TE) for the acquisition, specified in seconds. This parameter is required if a corresponding fieldmap data is present or the data comes from a multi echo sequence. Corresponds to DICOM Tag 0018, 0081 “Echo Time”.
     'FlipAngle', # 2 Flip angle for the acquisition, specified in degrees. Corresponds to: DICOM Tag 0018, 1314 “Flip Angle”.
     'SliceTiming', # 3 The time at which each slice was acquired during the acquisition. Slice timing is not slice order - it describes the time (sec) of each slice acquisition in relation to the beginning of volume acquisition. It is described using a list of times (in JSON format) referring to the acquisition time for each slice. The list goes through slices along the slice axis in the slice encoding dimension (see below). This parameter is required for sparse sequences. In addition without this parameter slice time correction will not be possible.
     'MultibandAccellerationFactor', # 4 The multiband factor, for multiband acquisitions
     'ParallelReductionFactorInPlane', # 5 The parallel imaging (e.g, GRAPPA) factor. Use the denominator of the fraction of k-space encoded for each slice. For example, 2 means half of k-space is encoded. Corresponds to DICOM Tag 0018, 9069 “Parallel Reduction Factor In-plane”.
     'PhaseEncodingDirection', # 6 Possible values: “i”, “j”, “k”, “i-”, “j-”, “k-”. The letters “i”, “j”, “k” correspond to the first, second and third axis of the data in the NIFTI file. The polarity of the phase encoding is assumed to go from zero index to maximum index unless ‘-’ sign is present (then the order is reversed - starting from the highest index instead of zero)
     'EffectiveEchoSpacing', # 7 The sampling interval also known as the dwell time; required for unwarping distortions using field maps; expressed in seconds. See here how to calculate it. This parameter is required if a corresponding fieldmap data is present
     'TotalReadoutTime', # 8 defined as the time ( in seconds ) from the center of the first echo to the center of the last echo (aka “FSL definition” - see here and here how to calculate it). This parameter is required if a corresponding multiple phase encoding directions fieldmap (see 8.9.4) data is present.
     'InstitutionName', # 9 The name of the institution in charge of the equipment that produced the composite instances. Corresponds to DICOM Tag 0008, 0080 ”InstitutionName”.
     'InstitutionAddress', # 10 The address of the institution in charge of the equipment that produced the composite instances. Corresponds to DICOM Tag 0008, 0081 ”InstitutionAddress”.
     'DeviceSerialNumber' # 11 The serial number of the equipment that produced the composite instances. Corresponds to DICOM Tag 0018, 1000 ”DeviceSerialNumber”. A pseudonym can also be used to prevent the equipment from being identifiable, so long as each pseudonym is unique within the dataset. 
     ]
)

AnatomyInfo = namedtuple(
    'AnatomyInfo',
    ['RepetitionTime',  # 0 TR The time in seconds between the beginning of an acquisition of one volume and the beginning of acquisition of the volume following it (TR). Please note that this definition includes time between scans (when no data has been acquired) in case of sparse acquisition schemes. This value needs to be consistent with the ‘ pixdim[4] ’ field (after accounting for units stored in ‘ xyzt_units ’ field) in the NIfTI header.
     'EchoTime',  # 1 The echo time (TE) for the acquisition, specified in seconds. This parameter is required if a corresponding fieldmap data is present or the data comes from a multi echo sequence. Corresponds to DICOM Tag 0018, 0081 “Echo Time”.
     'FlipAngle', # 2 Flip angle for the acquisition, specified in degrees. Corresponds to: DICOM Tag 0018, 1314 “Flip Angle”.
     'SliceTiming', # 3 The time at which each slice was acquired during the acquisition. Slice timing is not slice order - it describes the time (sec) of each slice acquisition in relation to the beginning of volume acquisition. It is described using a list of times (in JSON format) referring to the acquisition time for each slice. The list goes through slices along the slice axis in the slice encoding dimension (see below). This parameter is required for sparse sequences. In addition without this parameter slice time correction will not be possible.
     'MultibandAccellerationFactor', # 4 The multiband factor, for multiband acquisitions
     'ParallelReductionFactorInPlane', # 5 The parallel imaging (e.g, GRAPPA) factor. Use the denominator of the fraction of k-space encoded for each slice. For example, 2 means half of k-space is encoded. Corresponds to DICOM Tag 0018, 9069 “Parallel Reduction Factor In-plane”.
     'PhaseEncodingDirection', # 6 Possible values: “i”, “j”, “k”, “i-”, “j-”, “k-”. The letters “i”, “j”, “k” correspond to the first, second and third axis of the data in the NIFTI file. The polarity of the phase encoding is assumed to go from zero index to maximum index unless ‘-’ sign is present (then the order is reversed - starting from the highest index instead of zero)
     'EffectiveEchoSpacing', # 7 The sampling interval also known as the dwell time; required for unwarping distortions using field maps; expressed in seconds. See here how to calculate it. This parameter is required if a corresponding fieldmap data is present
     'TotalReadoutTime', # 8 defined as the time ( in seconds ) from the center of the first echo to the center of the last echo (aka “FSL definition” - see here and here how to calculate it). This parameter is required if a corresponding multiple phase encoding directions fieldmap (see 8.9.4) data is present.
     'InstitutionName', # 9 The name of the institution in charge of the equipment that produced the composite instances. Corresponds to DICOM Tag 0008, 0080 ”InstitutionName”.
     'InstitutionAddress', # 10 The address of the institution in charge of the equipment that produced the composite instances. Corresponds to DICOM Tag 0008, 0081 ”InstitutionAddress”.
     'DeviceSerialNumber', # 11 The serial number of the equipment that produced the composite instances. Corresponds to DICOM Tag 0018, 1000 ”DeviceSerialNumber”. A pseudonym can also be used to prevent the equipment from being identifiable, so long as each pseudonym is unique within the dataset.
     'ContrastBolusIngredient' # 12 Active ingredient of agent. Allowed values: IODINE, GADOLINIUM, CARBON DIOXIDE, BARIUM. Corresponds to DICOM Tag 0018,1048.
     ]
)    

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

def write_json(data, resultfile):
    with open(resultfile, 'w') as outfile:
        json.dump(data, outfile)
