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
            'dobt':             ['b',0,1,'dobt for both get stmid and trk'],
        }

        self.purpose="""
reconstruct stm-sum cards using mdeck3.trk data in src directories in dat/tc/sbt by year and basin"""

        self.examples='''
%s 2019'''

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#

argv=sys.argv
CL=TmtrkCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr


MF.sTimer('ALL')

MF.sTimer('sbt')
sbt=superBT(version,verb=verb)
MF.dTimer('sbt')

# -- internal processing verb
#
overb=0

stmids=None
if(stmopt != None):
    
    stmids=[]
    stmopts=getStmopts(stmopt)
    for stmopt in stmopts:
        stmids=stmids+sbt.getMd3Stmids(stmopt,dobt=dobt,dofilt9x=dofilt9x,verb=overb)

    sbtTSDev={}
    sbtTSNonDev={}
    
    nNN=0

    sbt.stmopt=stmopt

    #kkk 'bdir' 270.0
    #kkk 'blat' 2.7
    #kkk 'blon' 141.9
    #kkk 'bpmin' 1006.0
    #kkk 'br34m' -999.0
    #kkk 'bspd' 10.0
    #kkk 'btccode' DB
    #kkk 'bvmax' 15.0
    #kkk 'cpsb' -2.0
    #kkk 'cpshi' -5.0
    #kkk 'cpslo' 15.0
    #kkk 'dvrg200' 24.0
    #kkk 'eprc3' 19.5
    #kkk 'eprc5' 13.3
    #kkk 'eprc8' 7.7
    #kkk 'epre3' 12.2
    #kkk 'epre5' 10.9
    #kkk 'epre8' 8.6
    #kkk 'eprg3' 25.7
    #kkk 'eprg5' 17.3
    #kkk 'eprg8' 9.5
    #kkk 'epri3' 19.3
    #kkk 'epri5' 12.2
    #kkk 'epri8' 7.2
    #kkk 'eprr3' 81.0
    #kkk 'eprr5' 83.0
    #kkk 'eprr8' 84.0
    #kkk 'land' 556.0
    #kkk 'mvmax' 11.0
    #kkk 'oprc3' 21.3
    #kkk 'oprc5' 12.9
    #kkk 'oprc8' 7.3
    #kkk 'oprg3' 29.3
    #kkk 'oprg5' 17.0
    #kkk 'oprg8' 9.1
    #kkk 'opri3' 20.0
    #kkk 'opri5' 11.6
    #kkk 'opri8' 6.5
    #kkk 'poci0' -999.0
    #kkk 'poci1' -999.0
    #kkk 'r34m' -999.0
    #kkk 'rh500' 80.0
    #kkk 'rh700' 71.0
    #kkk 'rh850' 73.0
    #kkk 'roci0' -999.0
    #kkk 'roci1' -999.0
    #kkk 'shrdir' 291.0
    #kkk 'shrspd' 20.0
    #kkk 'sst' 29.4
    #kkk 'ssta' 0.4
    #kkk 'stmdir' 284.0
    #kkk 'stmspd' 17.0
    #kkk 'tpw' 59.0
    #kkk 'u500' -162.0
    #kkk 'u700' -110.0
    #kkk 'u850' -58.0
    #kkk 'v500' -29.0
    #kkk 'v700' 10.0
    #kkk 'v850' -17.0
    #kkk 'vort850' 56.0


    ovars=['bvmax','bspd','br34m','stmspd',
           'mvmax',
           'shrspd',
           'tpw','rh700',
           'oprc3','oprg3','opri3',
           'eprc3','eprg3','epri3',
           'epre3','eprr3',
           'ssta']

    #ovars=['mvmax','bvmax','stmspd']
    #ovars=['bspd','stmspd']
    
    tovars=[]
    for ovar in ovars:
        tovars.append("%s"%(ovar))
        
    ovars=tovars

    tsNon={}
    tsDev={}
    overb=verb

    for stmid in stmids:
        (sbtType,sbtTS)=sbt.getSbtTS(stmid,verb=overb)
        print 'sss',stmid,sbtType
        if(sbtType == 'NONdev'):
            sbtTSNonDev[stmid]=sbtTS
        elif(sbtType == 'DEV'):
            sbtTSDev[stmid]=sbtTS
        else:
            nNN=nNN+1
        
            
    nstmids=sbtTSNonDev.keys()
    nstmids.sort()

    dstmids=sbtTSDev.keys()
    dstmids.sort()

    if(verb == 2):
        
        for nstmid in nstmids:
            print 'NNNN',nstmid
            nsbtts=sbtTSNonDev[nstmid]
            ntimes=nsbtts.keys()
            ntimes.sort()
            for ntime in ntimes:
                print 'nn',ntime,nsbtts[ntime]
            
            for dstmid in dstmids:
                print 'DDDD',dstmid
                dsbtts=sbtTSDev[dstmid]
                dtimes=dsbtts.keys()
                dtimes.sort()
                for dtime in dtimes:
                    print 'dd',dtime,dsbtts[dtime]
                    
    nDev=len(dstmids)
    nNon=len(nstmids)
    
    if(nDev != nNN):
        print 'hhhmmmmmm nDev != nNN ',nDev,nNN
    
    if(nNon != 0 and nNN != 0 and nDev != 0):
        rDev=nDev*1.0/float(nNon+nDev)
        rDev=rDev*100.0
        rDevN=nNN*1.0/float(nNon+nNN)
        rDevN=rDevN*100.0
        pMissN=rDevN-rDev
        print 'NNN for stmopt: ',stmopt,'nNN: ',nNN,'nDev',nDev,'nNon',nNon
        print 'DDD rFormDev: %3.0f%%  NNM rFormN: %3.0f%%  %4.1f%%'%(rDev,rDevN,pMissN)

    #rc=sbt.makeGaNonVDevTS(sbtTSNonDev,'non',nvars)
    #rc=sbt.makeGaNonVDevTS(sbtTSDev,'dev',nvars)
    rc=sbt.makeGaNonVDevTSDict(sbtTSNonDev,'non',ovars,verb=overb)
    print sbt.gactlPath
    rc=sbt.makeGaNonVDevTSDict(sbtTSDev,'dev',ovars,verb=overb)
    print sbt.gactlPath

MF.dTimer('ALL')



sys.exit()


