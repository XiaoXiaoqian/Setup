#!/bin/sh
read_nii_header()
{
    nii_file=$1
    #fslhd $nii_file | grep -E 'phase_dim|descrip'
    fslhd $nii_file | grep -E 'descrip'
    EffectiveEchoSpacing=ec
}
#    '''
#https://cni.stanford.edu/wiki/GE_Processing
#results should be look like the following
#phase_dim      2
#descrip te=30.00;ti=0;fa=77;ec=0.4800;acq=[80,80];mt=0;rp=2.0;
#''']
