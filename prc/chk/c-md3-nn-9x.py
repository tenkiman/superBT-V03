#!/usr/bin/env python

from sBT import *


#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# command line setup
#

class TmtrkCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv
        self.argopts={
            1:['yearopt', 'bYYYY.eYYYY'],
        }


        self.options={
            'override':         ['O',0,1,'override'],
            'basinOpt':         ['B:',None,'a','basin opt'],
            'verb':             ['V',0,1,'verb=1 is verbose'],
            'doTrk':            ['T',1,0,'do NOT make the track files'],
            'ropt':             ['N','','norun',' norun is norun'],
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

tt=yearopt.split('.')

if(len(tt) == 2):
    byear=tt[0]
    eyear=tt[1]
    years=yyyyrange(byear, eyear)
    
elif(len(tt) == 1):
    years=[yearopt]
    
else:
    print 'EEE -- invalid yearopt: ',yearopt

md3=Mdeck3(verb=verb)

# -- work in the current version
#
sbtSrcDir=sbtSrcDir

if(basinOpt != None):
    basins=[basinOpt]
else:
    basins=['w','l','e','i','h','c']

MF.sTimer('sum-md3-ALL')

for year in years:
    
    for basin in basins:
    
        stmopt="%s.%s"%(basin,year)
        stmids=[]
        stmids=stmids+md3.getMd3Stmids(stmopt,verb=verb)
    
        slists=[]
        for stmid in stmids:
            (rc,scard)=md3.getMd3StmMeta(stmid)
            slists.append(rc)
            
        sNN={}
        s9X={}
        nNN=0
        n9Xd=0
        n9Xn=0
        nCNN=0
        nC9X=0
        for sl in slists:
            stmid="%s.%s"%(sl[1],sl[0])
            if(IsNN(stmid)):
                b1NN=sl[1][-1]
                stmid9x="%s.%s"%(sl[-2],sl[0])
                b19X=sl[-2][-1]
                nNN=nNN+1
                sNN[stmid]=stmid9x
                if(verb): print 'NN:',nNN,stmid,stmid9x,'BB',b1NN,b19X
                if(b1NN != b19X):
                    nCNN=nCNN+1
                    
            else:
                tt=sl[-2].split(':')
                dtype=tt[0].strip()
                d9x=tt[1].strip()
                
                if(dtype == 'NN'):
                    b1NN=d9x[-1]
                    b19X=sl[1][-1]
                    stmidNN="%s.%s"%(d9x,sl[0])
                    stmid9x="%s.%s"%(sl[1],sl[0])
                    n9Xd=n9Xd+1
                    if(verb): print '99: ',n9Xd,stmid9x,stmidNN,'BB',b1NN,b19X
                    if(b1NN != b19X):
                        nC9X=nC9X+1
                    s9X[stmidNN]=stmid9x
                else:
                    n9Xn=n9Xn+1
                    
        nNNA=nNN-nCNN
        n9XdA=n9Xd-nC9X
        if(nNN != n9Xd):
            stmopt=stmopt.replace('.20','.')
            card='%s  WWW nNN: %2d != %2d :n9Xd  nCNN: %2d nC9X: %2d'%(stmopt,nNN,n9Xd,nCNN,nC9X)
            print card

            if(nNNA != n9XdA):
                print
                card='%s  EEE diff nNN: %2d != %2d :n9Xd  nCNN: %2d nC9X: %2d'%(stmopt,nNN,n9Xd,nCNN,nC9X)
                print card
                print
        
        if(verb):
            kksNN=sNN.keys()
            kks9X=s9X.keys()
            print 'nnn-keys: len(sNN): ',len(kksNN),' len(s9X): ',len(kks9X)
        
            kksNN.sort()
            for k in kksNN:
                print 'kN:',k,sNN[k]
            
            kks9X.sort()
            for k in kks9X:
                print 'k9:',k,s9X[k]

            
        
MF.dTimer('sum-md3-ALL')
                         
sys.exit()
    