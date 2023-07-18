#!/usr/bin/env python

from sBT import *

#import pandas as pd
#import numpy as np

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# command line setup
#

class TmtrkCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.defaults={
            #'version':'v01',
            }

        self.argv=argv
        self.argopts={
            #1:['yearopt',    'yearopt YYYY or BYYYY.EYYYY'],
        }


        self.options={
            'override':         ['O',0,1,'override'],
            'verb':             ['V',0,1,'verb=1 is verbose'],
            'ropt':             ['N','','norun',' norun is norun'],
            'stmopt':           ['S:',None,'a',' stmid target'],
            'dofilt9x':         ['9',0,1,'only do 9X'],
            'dtgopt':           ['d:',None,'a',' dtgopt'],
            'doLs':             ['l:',None,'a',' only list a var'],
            'dobt':             ['b',0,1,'dobt for both get stmid and trk'],
        }

        self.purpose="""
reconstruct stm-sum cards using mdeck3.trk data in src directories in dat/tc/sbt by year and basin"""

        self.examples='''
%s -S 01w.07 -l epre6'''

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#

argv=sys.argv
CL=TmtrkCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr


MF.sTimer('ALL')

# -- make sbt object
#

MF.sTimer('sbt')
sbt=superBT(version,verb=verb)
MF.dTimer('sbt')

# -- make xaxis (dtg) n=0,maxTimes=100
#
rc=sbt.makeSbtVarTaxis()

# -- internal processing verb
#
overb=0

stmids=None
if(stmopt != None):
    
    stmids=[]
    stmopts=getStmopts(stmopt)
    for stmopt in stmopts:
        stmids=stmids+sbt.getMd3Stmids(stmopt,dobt=dobt,dofilt9x=dofilt9x,verb=overb)

    sbtVarAll={}
    
    nNN=0
    sbt.stmopt=stmopt

    ovars=['bvmax','bspd','br34m',
           'mvmax',
           'shrspd',
           'tpw','rh700',
           'oprc3','oprg3','opri3',
           'eprc3','eprg3','epri3',
           'epre3','eprr3',
           'ssta']

    #ovars=['mvmax','bvmax','stmspd']
    #ovars=['bvmax','br34m']
    ovars=['oprc3','oprg3','opri3',
           'eprc3','eprg3','epri3',
           'epre3','eprr3',
           ]

    ovars=['bvmax','bspd','br34m',
           'mvmax',
           ]
    ovars=[
           'shrspd',
           'tpw','rh700',
           'ssta']

    ovars=['bvmax','bspd','br34m',
           'mvmax','btccode',
           'shrspd',
           'tpw','rh700',
           'roci1','roci0',
           'oprc3','oprg3','opri3',
           'eprc3','eprg3','epri3','epre3','eprr3',
           'oprc5','oprg5','opri5',
           'eprc5','eprg5','epri5','epre5','eprr5',
           'ssta']

    #ovars=['opri3','epre3','eprr3']
    

    # -- get the sBt for the stmids
    #
    sbtvarAll={}
    overb=verb
    for stmid in stmids:
        (sbtType,sbtVar)=sbt.getSbtVar(stmid,doDtgKey=1,verb=overb)
        sbtvarAll[stmid]=sbtVar
    
    # -- ls only
    
    if(doLs != None):
        ovars=[doLs]
        rc=sbt.lsGaVarAllDict(sbtvarAll,ovars)
        sys.exit()
        
    
    tovars=[]
    for ovar in ovars:
        tovars.append("%s"%(ovar))
        
    ovars=tovars

    # -- make the grads .dat .ctl
    #
    rc=sbt.makeGaVarAllDict(sbtvarAll,ovars,verb=overb)
    print sbt.gactlPath

MF.dTimer('ALL')



sys.exit()


