baseDir='/Users/xiaoqian/Projects/aTBS'
dataDir=${baseDir}/source
outputDir=${baseDir}/derivatives
workDir=${baseDir}/work
#freesurferDir='/Users/xiaoqian/tools/freesurfer'
freesurferDir=$FREESURFER_HOME
fmriprep $dataDir $outputDir participant --participant-label $subID --ignore fieldmaps --ignore slicetiming --longitudinal --use-aroma --fs-license-file ${freesurferDir}/license.txt --resource-monitor -w $workDir --low-mem --nthreads 24 --omp-nthreads 24
