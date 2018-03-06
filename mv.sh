#/bin/sh
basedir=/Users/xiaoqian/Projects/aTBS/raw
cd $basedir
  for ffile in 20*
  do 
    fdir=${basedir}/${ffile}
    echo ${fdir}
    cd ${fdir}
    sudo rm -rf *Save *Shim *calibration *fgre
    for ffile in 1*
    do
      ffdir=${fdir}/${ffile}
      cd ${ffdir}
      sudo rm -rf *physio* *pfile* *pyrdb
    done
  done
