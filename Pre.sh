FreesuferLicsensePath='/Users/xiaoqian/Box/XiaoqianXiao/tools/freesurfer'
OutputPath='/Users/xiaoqian/Projects/aTBS/derivatives'
DataPath='/Users/xiaoqian/Projects/aTBS/source'
WorkPath='/Users/xiaoqian/Projects/aTBS/work'
NipVersion='latest'

for sub in 1 2 3 4 11 14 16 18 19 21 26 28
do 
  if [ ${sub} -lt 10];
  then
    subID=00${sub}
  else
    subID=0${sub}
  fi
    #with results in T1 space (specitally for ICA-AROMA in T1 space)
    #docker run -ti --rm -v $DataPath:/data:ro -v $OutputPath:/out  -v $WorkPath:/work -v $FreesuferLicsensePath/license.txt:/opt/freesurfer/license.txt poldracklab/fmriprep:$NipVersion /data /out/out participant --ignore fieldmaps --ignore slicetiming --longitudinal --participant_label sub-$subID --use-aroma --fs-license-file /opt/freesurfer/license.txt --resource-monitor -w /work --low-mem —nthreads 8 --omp-nthreads 8 --output-space T1w template
    #without results in T1 space (will need non-aggressive ICA-AROMA in T1 space mannually latter)
    docker run -ti --rm -v $DataPath:/data:ro -v $OutputPath:/out  -v $WorkPath:/work -v $FreesuferLicsensePath/license.txt:/opt/freesurfer/license.txt poldracklab/fmriprep:$NipVersion /data /out/out participant --ignore fieldmaps --ignore slicetiming --longitudinal --participant_label sub-$subID --use-aroma --fs-license-file /opt/freesurfer/license.txt --resource-monitor -w /work --low-mem —nthreads 8 --omp-nthreads 8 --output-space T1w template
done
