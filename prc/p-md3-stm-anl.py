#!/usr/bin/env python

from sBT import *

#import pandas as pd
#import numpy as np

def getStmSumVars(sps,olist1,olist2,oopt=None,minDev=0.0,min9X=0.0,verb=0):
    
    (yyyy,stm,livestatus,tctype,sname,ovmax,tclife,stmlife,latb,lonb,bdtg,edtg,
     latmn,latmx,lonmn,lonmx,
     stcd,oACE,
     nRI,nED,nRW,
     RIstatus,timeGen,stm9x,ogendtg)=sps

    stmid="%s.%s"%(stm,yyyy)
    if(verb):
        print 'VVV: ',stmid,sps
    
    if(oopt == 'time2dev'):
        (devType,stmid9x)=stm9x.split(":")
        time2gen=timeGen.split(":")[1].strip()
        if(IsNN(stmid)):
            time2gen=timeGen.split(":")[1].strip()
            time2gen=float(time2gen)/24.0
            olist1.append(time2gen)
            if(time2gen <= minDev):
                print 'WWW small 9X-NN for stmid: ',stmid,' time2gen: ',time2gen
        else:
            if(stmlife >= min9X):
                print 'sss',stcd
                olist2.append(stmlife)
            
    else:
        print 'EEE in getStmSumVars...must set oopt='
        sys.exit()
            
    
    
    
    


#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# command line setup
#

class TmtrkCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv
        self.argopts={
            #1:['yearopt',    'yearopt YYYY or BYYYY.EYYYY'],
        }


        self.options={
            'override':         ['O',0,1,'override'],
            'verb':             ['V',0,1,'verb=1 is verbose'],
            'ropt':             ['N','','norun',' norun is norun'],
            'yearOpt':          ['Y:',None,'a','yearOpt'],
            'stmopt':           ['S:',None,'a',' stmid target'],
            'sumonly':          ['s',0,1,'list stmids only'],
            'dofilt9x':         ['9',0,1,'only do 9X'],
            'dobt':             ['b',0,1,'dobt for both get stmid and trk'],
            'doshow':           ['x',1,0,'do NOT show in pltHist'],
            'filtopt':          ['f:',None,'a',"""
            
FF.TT.NN
FF: all|season|dev
TT: latb|latmn|stmlife|time2gen|9xlife
NN: 0 - counts; 1 - donorm=1; 2 donorm=1,docum=1          
"""],
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

oyearOpt=yearOpt
if(yearOpt != None):
    tt=yearOpt.split('.')

    if(len(tt) == 2):
        byear=tt[0]
        eyear=tt[1]
        years=mf.yyyyrange(byear, eyear)
        oyearOpt="%s-%s"%(byear,eyear)
    
    elif(len(tt) == 1):
        years=[yearOpt]
        oyearOpt=yearOpt
    else:
        print 'EEE -- invalid yearopt: ',yearopt

if(filtopt == None):
    print 'EEE you must set filtopt in FF.TT.NN format'
    sys.exit()

MF.sTimer('ALL')
MF.sTimer('md3-load')
md3=Mdeck3(oyearOpt=oyearOpt,verb=verb,doSumOnly=1)
MF.dTimer('md3-load')

stmids=[]
stmopts=getStmopts(stmopt)
for stmopt in stmopts:
    stmids=stmids+md3.getMd3Stmids(stmopt,dobt=dobt,dofilt9x=dofilt9x,verb=verb)

slists=[]
olistDev=[]
olistNon=[]

for stmid in stmids:
    (sps,scard)=md3.getMd3StmMeta(stmid)
    rc=getStmSumVars(sps,olistDev,olistNon,oopt='time2dev')
    
print 'ddd',olistDev
print 'nnn',olistNon

if(find(stmopt.lower(),'l')): basin='LANT'
if(find(stmopt.lower(),'w')): basin='WPAC'
if(find(stmopt.lower(),'e')): basin='EPAC'
if(find(stmopt.lower(),'h')): basin='SHEM'

(filtBySeason,filtByDev,filtByCC,tlist,donorm,docum,
 ymax,yint,xmax,xmin,xint,binint,ptitle2)=setFilter(filtopt,stmopt)


statAll=olistDev
statDev=olistDev
statNonDev=olistNon
year=stmopt

pngpath="/ptmp/%s.%s.png"%(filtopt,stmopt)
pngpath=pngpath.replace(',','-')
print 'PPP(pngpath): ',pngpath
        
        
ptype='bar'
if(docum): ptype='step'

pltHist(statAll,statDev,statNonDev,stmopt,basin=basin,year=year,
        filttype='dev',
        tlist=tlist,
        ptitle2=ptitle2,
        donorm=donorm,
        docum=docum,
        ymax=ymax,yint=yint,
        binint=binint,
        dostacked=0,
        ptype=ptype,
        var1='Dev',
        var2='NonDev',
        pngpath=pngpath,
        xmax=xmax,xmin=xmin,xint=xint,tag=tlist,doshow=doshow)

sys.exit()
        
if(sumonly):
    
    sNN={}
    s9X={}
    nNN=0
    n9Xd=0
    n9Xn=0
    for sl in slists:
        stmid="%s.%s"%(sl[1],sl[0])
        if(IsNN(stmid)):
            stmid9x="%s.%s"%(sl[-2],sl[0])
            nNN=nNN+1
            sNN[stmid]=stmid9x
            if(verb): print 'NN:',nNN,stmid,stmid9x
        else:
            tt=sl[-2].split(':')
            dtype=tt[0].strip()
            d9x=tt[1].strip()
            if(dtype == 'NN'):
                stmidNN="%s.%s"%(d9x,sl[0])
                stmid9x="%s.%s"%(sl[1],sl[0])
                n9Xd=n9Xd+1
                s9X[stmidNN]=stmid9x
            else:
                n9Xn=n9Xn+1
                
    print 'NNN nNN: ',nNN,'n9Xd: ',n9Xd,'n9Xn: ',n9Xn
    kksNN=sNN.keys()
    kks9X=s9X.keys()
    print 'nnn-keys: len(sNN): ',len(kksNN),' len(s9X): ',len(kks9X)
    
    if(verb):
        kksNN.sort()
        for k in kksNN:
            print 'kN:',k,sNN[k]
            
        kks9X.sort()
        for k in kks9X:
            print 'k9:',k,s9X[k]

MF.dTimer('ALL')



sys.exit()


