baseDir='/Users/xiaoqian/Projects/aTBS'
dataDir=${baseDir}/source
outputDir=${baseDir}/derivatives
workDir=${baseDir}/work
#freesurferDir='/Users/xiaoqian/tools/freesurfer'
freesurferDir=$FREESURFER_HOME
fmriprep $dataDir $outputDir participant --participant-label $subID --ignore fieldmaps --ignore slicetiming --longitudinal --use-aroma --fs-license-file ${freesurferDir}/license.txt --resource-monitor -w $workDir --low-mem --nthreads 24 --omp-nthreads 24



Docker

docker run -ti --rm \

-v $DataPath:/data:ro \

-v $OutputPath:/out \

-v $FreesuferLicsensePath:/opt/freesurfer/license.txt \

poldracklab/fmriprep:latest \

/data /out/out \

participant \

--ignore fieldmaps \

--ignore slicetiming \

--no-freesurfer \

--fs-license-file /opt/freesurfer/license.txt





#OutputPath='/Users/xiaoqian/Box/Xiaoqian_Externally_Shareable_Files/Project/aTBS/derivatives'

FreesuferLicsensePath='/Users/xiaoqian/Box/XiaoqianXiao/tools/freesurfer'

OutputPath='/Users/xiaoqian/Projects/aTBS/derivatives'

DataPath='/Users/xiaoqian/Projects/aTBS/source'

WorkPath='/Users/xiaoqian/Projects/aTBS/work'

NipVersion='latest'

subID='024'



Need to be done: 1 2 3 4 11 14 16 18 19 21 24 26 28

still there: 

In processing: 24

Done: 

1, 2, 3, 4, 11, 14, 16, 18, 19, 21, 26, 28

No freesurfer Nor a no working dir

docker run -ti --rm -v $DataPath:/data:ro -v $OutputPath:/out -v $WorkPath:/work -v $FreesuferLicsensePath/license.txt:/opt/freesurfer/license.txt poldracklab/fmriprep:$NipVersion /data /out/out participant --ignore fieldmaps --ignore slicetiming --longitudinal --participant_label sub-$subID --fs-license-file /opt/freesurfer/license.txt --low-mem --no-freesurfer --nthreads 4 --omp-nthreads 12 --resource-monitor

No freesurfer Nor a

docker run -ti --rm -v $DataPath:/data:ro -v $OutputPath:/out -v $WorkPath:/work -v $FreesuferLicsensePath/license.txt:/opt/freesurfer/license.txt poldracklab/fmriprep:$NipVersion /data /out/out participant --ignore fieldmaps --ignore slicetiming --longitudinal --participant_label sub-$subID --fs-license-file /opt/freesurfer/license.txt -w /work --low-mem --no-freesurfer --nthreads 1 --omp-nthreads 20 --resource-monitor



No freesurfer

docker run -ti --rm -v $DataPath:/data:ro -v $OutputPath:/out -v $WorkPath:/work -v $FreesuferLicsensePath/license.txt:/opt/freesurfer/license.txt poldracklab/fmriprep:$NipVersion /data /out/out participant --ignore fieldmaps --ignore slicetiming --longitudinal --participant_label sub-$subID --use-aroma --fs-license-file /opt/freesurfer/license.txt -w /work --low-mem --no-freesurfer --nthreads 1 --omp-nthreads 20 --resource-monitor

With freesurfer

docker run -ti --rm -v $DataPath:/data:ro -v $OutputPath:/out -v $WorkPath:/work -v $FreesuferLicsensePath/license.txt:/opt/freesurfer/license.txt poldracklab/fmriprep:$NipVersion /data /out/out participant --ignore fieldmaps --ignore slicetiming --longitudinal --participant_label sub-$subID --use-aroma --fs-license-file /opt/freesurfer/license.txt --resource-monitor -w /work --low-mem --nthreads 24 --omp-nthreads 24



FreesuferLicsensePath='/Users/xiaoqian-test/Box/XiaoqianXiao/tools/freesurfer'

OutputPath='/Users/xiaoqian-test/Projects/aTBS/derivatives'

DataPath='/Users/xiaoqian-test/Box/Xiaoqian_Externally_Shareable_Files/Project/aTBS/source'







docker-machine ssh myvm1 



ls -lah ~/Library/Containers/com.docker.docker/Data/com.docker.driver.amd64-linux/Docker.qcow2

killall Docker && open /Applications/Docker.app

cd /Applications/Docker.app/Contents/MacOS

./qemu-img resize ~/Library/Containers/com.docker.docker/Data/com.docker.driver.amd64-linux/Docker.qcow2 +100G







best off running one instance per subject and requesting 8 cores with 8 threads max and 10+safety G of memory



ICA-AROMA is calculated in the MNI template space
