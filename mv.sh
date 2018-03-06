#/bin/sh
basedir=/Users/xiaoqian/Projects/aTBS/raw
cd $basedir
  for fdir in 20*
  do 
    echo ${fdir}
    cd ${fdir}
    sudo rm -rf *Save *Shim *calibration *fgre
    for ffdir in 1*
    do
      sudo rm -rf *physio* *pfile* *pyrdb
    done
  done
