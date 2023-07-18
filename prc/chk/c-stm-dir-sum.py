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


# -- work in the current version
#
sbtSrcDir=sbtSrcDir

if(basinOpt != None):
    basins=[basinOpt]
else:
    basins=['wpac','lant','epac','io','shem']

MF.sTimer('sum-md3-ALL')

for year in years:
    tdir="%s/%s"%(sbtSrcDir,year)
    MF.ChkDir(tdir,'mk')
    for basin in basins:

        btdir="%s/%s"%(tdir,basin)
        MF.ChkDir(btdir,'mk')

        bopt="%s.%s"%(basin[0],year)
        if(basin == 'epac'):
            bopt=bopt+',c.%s'%(year)
            
        if(basin == 'shem'):
            bopt='h.%s'%(year)
            
        smask="%s/%s/*"%(tdir,basin)
        spaths=glob.glob(smask)
        spaths.sort()

        MF.sTimer('sum-md3-%s-%s'%(basin,year))

        stmNNs={}
        stm9Xs={}
        
        for spath in spaths:
            ss=spath.split('/')
            ssum=ss[-1]
            ssum=ssum.split('-')
            stmid="%s.%s"%(ssum[0],ssum[1])
            if(IsNN(stmid)):
                stmid9x="%s.%s"%(ssum[-1],ssum[1])
                stmNNs[stmid]=stmid9x
                if(verb): print 'NNN',ssum,stmid,stmid9x
            elif(Is9X(stmid)):
                stmid9x=stmid
                if(find(ssum[-2],'DEV')):
                    if(verb): print '999',stmid9x,ssum[-2],ssum[-1]
                    stm9Xs[stmid9x]="%s.%s"%(ssum[-1],ssum[1])
                    
        nns=stmNNs.keys()
        nns.sort()
        n9s=stm9Xs.keys()
        n9s.sort()
        for nn in nns:
            
            stm9x=stmNNs[nn]
            
            if(not(stm9x in n9s)):
                print 'EEEE ',nn,' NOT with an associated 9X: ',stm9x
            if(verb): print 'nn',nn,stm9x,(stm9x in n9s)
        
            
        
MF.dTimer('sum-md3-ALL')
                         
sys.exit()
    