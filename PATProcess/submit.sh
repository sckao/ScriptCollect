#! /bin/bash

cd /home/cms/sckao/Top/CMSSW_2_1_10/src/PhysicsTools/PatAlgos/test/RUNDIR/
source /home/cms/sckao/.bashrc
eval `scramv1 runtime -sh`
cmsRun RUNSCRIPT
