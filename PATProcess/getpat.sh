#! /bin/sh

# reading a file from a file list for each run
r=9
for i in `cat flist3.log`
do
# Read the file name from file list
RUNFILE=$i 
r=$(($r+1))
echo $r
RUNFOLDER="WJ_$r"

# create python file
PATOUT="pWJets_PAT1_$r.root"
echo $PATOUT
RUNPY="WJets_$r.py" 
echo $RUNPY 
cat Summer08_WJets_PAT.py | sed s/FASTFILE/$RUNFILE/ | sed s/PATFILE/$PATOUT/ > $RUNPY

# create run script
RUNSH="wj_$r.sh" 
echo $RUNSH 
cat submit.sh | sed s/RUNSCRIPT/$RUNPY/ | sed s/RUNDIR/$RUNFOLDER/ > $RUNSH
chmod a+x $RUNSH

# create submit file
RUNSUB="wj_$r.sub" 
echo $RUNSUB 
cat condor_0.sub | sed s/CONDOR_SH/$RUNSH/ | sed s/RUNDIR1/$RUNFOLDER/ > $RUNSUB

# create run folder and move all stuff in this folder
mkdir $RUNFOLDER
mv $RUNSUB $RUNFOLDER
mv $RUNSH $RUNFOLDER
mv $RUNPY $RUNFOLDER
cd $RUNFOLDER
condor_submit $RUNSUB
sleep 1s
cd ../

done
