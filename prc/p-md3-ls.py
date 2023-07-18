#!/usr/bin/env python

from sBT import *

#import pandas as pd
#import numpy as np

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# command line setup
#

def anlDevNon(strk,stmid,s9xspd=15.0,verb=0):
    
    dtgs=strk.keys()
    dtgs.sort()
    dtgs.reverse()
    #(rlat,rlon,vmax,pmin,tdir,tspd,r34m,r50m,tcstate,warn,roci,poci,
    #  alf,depth,eyedia,tdo,ostmid,ostmname,r34,r50)
    vmaxs=[]
    posits=[]
    dirspds=[]
    sace9xs=[]
    
    sacefact=1.0/(s9xspd*s9xspd)
    for dtg in dtgs:
        trk=strk[dtg]
        rlat=trk[0]
        rlon=trk[1]
        vmax=trk[2]
        sdir=trk[4]
        sspd=trk[5]
        vmaxs.append(vmax)
        posits.append((rlat,rlon))
        dirspds.append((sdir,sspd))
        sace9x=(vmax*vmax)*sacefact
        sace9xs.append(sace9x)
        
    lastdtg=dtgs[0]
    np=len(posits)

    dtbase=12
    
    uvmot={}
    for n in range(2,np):
        (rlat1,rlon1)=posits[n-2]
        (rlat0,rlon0)=posits[n]
        (tdir,tspd)=dirspds[n-2]
        time=-(n-2)*dtbase*0.5 - dtbase*0.5
        time0=time+dtbase*0.5
        time1=time-dtbase*0.5
        #print n,time,'beg',rlat1,rlon1,'end',rlat0,rlon0,'tdir/spd',tdir,tspd
        (sdir,sspd,su,sv)=rumhdsp(rlat0,rlon0,rlat1,rlon1,dtbase)
        (ndir,nspd)=uv2dirspd(su, sv)
        if(verb): print 'dddmmm N: %2d time0: %4.0f time: %4.0f time1: %4.0f  idir/spd: %3.0f %4.1f u: %4.1f v: %4.1f odir/spd: %3.0f %4.1f'%\
          (n,time0,time,time1,sdir,sspd,su,sv,ndir,nspd)
        uvmot[time]=(su,sv)
        
    times=uvmot.keys()
    times.sort()
    
    for time in times:
        su=uvmot[time][0]
        sv=uvmot[time][1]
        
    sdir24=sdir48=sdir72=undef
    sspd24=sspd48=sspd72=undef
    sace9x24=sace9x48=sace9x72=undef
    n24=n48=n72=0
    
    have24=(-6. in times and -12. in times and -18. in times)
    have48=(-30. in times and -36. in times and -42. in times)
    have72=(-54. in times and -60. in times and -66. in times)

    if(have24):
        sace9x24=0.0
        nt=0
        ub=vb=0.0
        for time in [-6.,-12.,-18]:
            (u1,v1)=uvmot[time]
            ub=ub+u1
            vb=vb+v1
            nt=nt+1

        if(nt > 0):
            ub=ub/nt
            vb=vb/nt
            (sdir24,sspd24)=uv2dirspd(ub, vb)
            
        sace9x24=0.0
        nb=0
        ne=4
        if(np < 4):
            ne=np
        for n in range(nb,ne):
            sace9x24=sace9x24+sace9xs[n]
            n24=n24+1
        
        
    else:
        # -- only 0 - 12 at most
        #
        ub=vb=0.0
        nt=0
        for time in times:
            (u1,v1)=uvmot[time]
            ub=ub+u1
            vb=vb+v1
            nt=nt+1

        if(nt > 0):
            ub=ub/nt
            vb=vb/nt
        
        (sdir24,sspd24)=uv2dirspd(ub, vb)
            
        sace9x24=0.0
        for n in range(0,np):
            sace9x24=sace9x24+sace9xs[n]
            n24=n24+1
        
        
    if(have48):
        sace9x48=0.0

        ub=vb=0.0
        nt=0
        for time in [-24.,-30.,-36.,-42.]:
            (u1,v1)=uvmot[time]
            ub=ub+u1
            vb=vb+v1
            nt=nt+1

        if(nt > 0):
            ub=ub/nt
            vb=vb/nt
            (sdir48,sspd48)=uv2dirspd(ub, vb)

        nb=4
        ne=8
        if(np < 8): 
            print 'www48',stmid,np
            ne=np
        for n in range(nb,ne):
            sace9x48=sace9x48+sace9xs[n]
            n48=n48+1
        
    if(have72):

        ub=vb=0.0
        nt=0
        for time in [-48.,-54.,-60.,-66.]:
            (u1,v1)=uvmot[time]
            ub=ub+u1
            vb=vb+v1
            nt=nt+1

        if(nt > 0):
            ub=ub/nt
            vb=vb/nt
            (sdir72,sspd72)=uv2dirspd(ub, vb)

        sace9x72=0.0

        nb=8
        ne=12

        if(np < 12):
            print 'www72 ',stmid,np
            ne=np
        for n in range(nb,ne):
            sace9x72=sace9x72+sace9xs[n]
            n72=n72+1
        
    if(verb):
        print 'NNNNNNNNNNNNN np: ',np
        print '24h: %3.0f %4.1f  %5.1f n24: %2d'%(sdir24,sspd24,sace9x24,n24)
        print '48h: %3.0f %4.1f  %5.1f n48: %2d'%(sdir48,sspd48,sace9x48,n48)
        print '72h: %3.0f %4.1f  %5.1f n72: %2d'%(sdir72,sspd72,sace9x72,n72)
        
    lifetime=(np-1)*6.0
    avals=(stmid,lifetime,sdir24,sspd24,sace9x24,sdir48,sspd48,sace9x48,sdir72,sspd72,sace9x72)
    lastyyyymm=lastdtg[0:6]
    rc=(lastyyyymm,avals)
    return(rc)
    
    
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
            'basinOpt':         ['B:',None,'a','basinOpt'],
            'yearOpt':          ['Y:',None,'a','yearOpt'],
            'stmopt':           ['S:',None,'a',' stmid target'],
            'sumonly':          ['s',0,1,'list stmids only'],
            'dofilt9x':         ['9',0,1,'only do 9X'],
            'domiss':           ['m',0,1,'out stmids with missing dtg'],
            'dtgopt':           ['d:',None,'a',' dtgopt'],
            'dobt':             ['b',0,1,'dobt for both get stmid and trk'],
            'doVitals':         ['v',0,1,'make tcvitals for tracker'],
            'anlType':          ['a:',None,'a','anlType: time2gen|'],
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

if(yearOpt != None):
    tt=yearOpt.split('.')
    
    if(len(tt) == 2):
        byear=tt[0]
        eyear=tt[1]
        years=yyyyrange(byear, eyear)
        oyearOpt="%s-%s"%(byear,eyear)
    
    elif(len(tt) == 1):
    
        years=[yearOpt]
        oyearOpt=yearOpt
else:
    oyearOpt=yearOpt



MF.sTimer('ALL')
MF.sTimer('md3-load')
md3=Mdeck3(oyearOpt=oyearOpt,verb=verb)
MF.dTimer('md3-load')

dtgs=None
if(dtgopt != None):
    dtgs=dtg_dtgopt_prc(dtgopt)
    
    if(doVitals):

        for dtg in dtgs:
            
            trks={}
            stmids=md3.getMd3Stmids4dtg(dtg,dobt=dobt)
            for stmid in stmids:
                (rc,m3trk)=md3.getMd3track(stmid)
                m3trkdtg=m3trk[dtg]
                trks[stmid]=m3trkdtg
                
            (tcVcards,tcvpath)=md3.makeTCvCards(stmids,dtg,trks,verb=verb)
                
            
        
        
        
    else:
    
        for dtg in dtgs:
            stmdtgs=md3.getMd3Stmids4dtg(dtg,dobt=dobt)
            #print 'DDD',dtg,stmdtgs
            for stmid in stmdtgs:
                (rc,m3trk)=md3.getMd3track(stmid,dobt=dobt)
                if(rc == 0):
                    print 'EEE m3trk for: ',stmid
                else:
                    card=printMd3Trk(m3trk[dtg],dtg)
                    print card
            
stmids=None
if(stmopt != None):
    
    stmids=[]
    stmopts=getStmopts(stmopt)
    for stmopt in stmopts:
        stmids=stmids+md3.getMd3Stmids(stmopt,dobt=dobt,dofilt9x=dofilt9x,verb=verb)

    for stmid in stmids:
        
        if(sumonly):
            (rc,scard)=md3.getMd3StmMeta(stmid)
            print scard
            continue
            # -- check for big life or errors in NNB-sum.txt file
            #tclife=float(rc[7])
            #if(tclife > 25.0):
                #sname=rc[4]
                #print 'big life for: ',stmid,sname,'tclife: ',tclife
            #continue
        
        # -- get track
        #
        rc=md3.getMd3track(stmid,dobt=dobt,verb=verb,domiss=domiss)

        if(rc[0] == None):
            cmissdtgs=''
            missdtgs=rc[1]
            missdtgs.sort()
            for missdtg in missdtgs:
                cmissdtgs="%s %s"%(cmissdtgs,missdtg)
            print 'MMMdtg for stmid:',stmid,'dtgs: %s'%(cmissdtgs)
            m3dtgs=[]
            continue
        elif(rc[0]):
            m3trk=rc[1]
            m3dtgs=m3trk.keys()
            m3dtgs.sort()
            if(domiss): m3dtgs=[]
        
        if(dtgs != None):
            for m3dtg in m3dtgs:
                if(m3dtg in dtgs):
                    print 'dd',m3dtg,'trk: ',m3trk[m3dtg]
        else:
            for m3dtg in m3dtgs:
                card=printMd3Trk(m3trk[m3dtg],m3dtg)
                print card





#stmids=None
#if(stmopt != None):
    
    #stmids=[]
    #stmopts=getStmopts(stmopt)
    #for stmopt in stmopts:
        #stmids=stmids+md3.getMd3Stmids(stmopt,dobt=dobt,dofilt9x=dofilt9x,verb=verb)

    #slists=[]
    #stmTrks={}
    
    #for stmid in stmids:
        
        ## -- get storm summary from meta data
        ##
        #(rc,scard)=md3.getMd3StmMeta(stmid)
        #slists.append(rc)
        ## -- error checking
            ##print scard
            ##continue
            ## -- check for big life or errors in NNB-sum.txt file
            ##tclife=float(rc[7])
            ##if(tclife > 25.0):
                ##sname=rc[4]
                ##print 'big life for: ',stmid,sname,'tclife: ',tclife
            ##continue
        
        ## -- get track
        ##
        #rc=md3.getMd3track(stmid,dobt=dobt,verb=verb,domiss=domiss)

        #if(rc[0] == None):
            #cmissdtgs=''
            #missdtgs=rc[1]
            #missdtgs.sort()
            #for missdtg in missdtgs:
                #cmissdtgs="%s %s"%(cmissdtgs,missdtg)
            #print 'MMMdtg for stmid:',stmid,'dtgs: %s'%(cmissdtgs)
            #m3dtgs=[]
            #continue
        #elif(rc[0]):
            #m3trk=rc[1]
            #stmTrks[stmid]=m3trk
            #m3dtgs=m3trk.keys()
            #m3dtgs.sort()
            #if(domiss): m3dtgs=[]
        
        #if(dtgs != None):
            #for m3dtg in m3dtgs:
                #if(m3dtg in dtgs):
                    #print 'dd',m3dtg,'trk: ',m3trk[m3dtg]
        #else:
            #if(not(sumonly)):
                #for m3dtg in m3dtgs:
                    #card=printMd3Trk(m3trk[m3dtg],m3dtg)
                    #print card
            

    #sNN={}
    #s9X={}
    #sN9={}
    #s9XDev={}
    #s9XNon={}
    #nNN=0
    #n9Xd=0
    #n9Xn=0
    #for sl in slists:
        #stmid="%s.%s"%(sl[1].lower(),sl[0])
        #if(IsNN(stmid)):
            #time2gen=sl[-3].split(":")[1].strip()
            #stmid9x="%s.%s"%(sl[-2].split(':')[-1].strip().lower(),sl[0])
            #nNN=nNN+1
            #sNN[stmid]=(stmid9x,sl)
            #sN9[stmid9x]=(stmid,sl)
            #if(verb): print 'NN:',nNN,stmid,stmid9x,time2gen
        #else:
            #tt=sl[-2].split(':')
            #dtype=tt[0].strip()
            #d9x=tt[1].strip()
            #if(dtype == 'NN'):
                #stmidNN="%s.%s"%(d9x.lower(),sl[0])
                #stmid9x="%s.%s"%(sl[1].lower(),sl[0])
                #if(stmidNN in stmids):
                    #s9X[stmidNN]=(stmid9x,sl)
                    #s9XDev[stmid]=(sl,stmTrks[stmid])
                    #n9Xd=n9Xd+1
                #else:
                    #print 'WWWBBB -- basin crossing of 9X: ',stmid9x,' into: ',stmidNN
            #else:
                #n9Xn=n9Xn+1
                #s9XNon[stmid]=(sl,stmTrks[stmid])
              
    #if(not(sumonly)):
        #sys.exit()
        
    #print 'NNN nNN: ',nNN,'n9Xd: ',n9Xd,'n9Xn: ',n9Xn
    #kksNN=sNN.keys()
    #kks9X=s9X.keys()
    #kksN9=sN9.keys()
    #kks9XDev=s9XDev.keys()
    #kks9XNon=s9XNon.keys()
    #print 'nnn-keys: len(sNN): ',len(kksNN),' len(s9X): ',len(kks9X),' len(sN9): ',len(kksN9),\
          #'len(s9XDev): ',len(kks9XDev),'len(s9XNon): ',len(kks9XNon)

    #if(find(anlType,'mo')):

        #moA={}
        
        #kkD=kks9XDev
        #kkD.sort()

        #kkN=kks9XNon
        #kkN.sort()
        
        #for kd in kkD:
            #strk=s9XDev[kd][1]
            ##print 'DDD',kd,s9XDev[kd][0]
            #(lastyyyymm,movals)=anlDevNon(strk,kd)
            #MF.append2KeyDictList(moA,'dev',lastyyyymm,movals)
            
        #for kn in kkN:
            #strk=s9XNon[kn][1]
            ##print 'NNN',kn,s9XNon[kn][0]
            #(lastyyyymm,movals)=anlDevNon(strk,kn)
            #MF.append2KeyDictList(moA,'non',lastyyyymm,movals)
            
        #mkkD=moA['dev'].keys()
        #mkkN=moA['non'].keys()

        #mkkD.sort()
        #mkkN.sort()
        
        #print 'mkkD:',mkkD
        #ncaseD=0
        #for kk in mkkD:
            #mvals=moA['dev'][kk]
            #print 'DDD',kk,len(mvals)
            #for mval in mvals:
                #ncaseD=ncaseD+1
                ##print mval
                
        #print 'MMM--DDD: len(s9XDev): ',len(kks9XDev),'ncaseD: ',ncaseD
        
        #ncaseN=0
        #for kk in mkkN:
            #mvals=moA['non'][kk]
            #print 'NNN',kk,len(mvals)
            #for mval in mvals:
                #ncaseN=ncaseN+1
                ##print mval
                
        #print 'MMM-NNN: len(s9XNon): ',len(kks9XNon),'ncaseN: ',ncaseN
        

    
    #elif(anlType == 'time2gen'):

        #kkD=kks9XDev
        #kkD.sort()
        
        #vmaxD={}
        
        #for kk in kkD:
    
            #strk=sN9[kk][1]
            #stmnn=sN9[kk][0]
            #time2gen=float(strk[-3].split(":")[1].strip())
            #time2gen=time2gen-0.0
            #s9trk=s9XDev[kk][0]
            #trk=s9XDev[kk][1]
            #dtgs=trk.keys()
            #dtgs.sort()
            ##(rlat,rlon,vmax,pmin,tdir,tspd,r34m,r50m,tcstate,warn,roci,poci,
            ##  alf,depth,eyedia,tdo,ostmid,ostmname,r34,r50)
            #vmaxs=[]
            #sace9x=0.0
            #for dtg in dtgs:
                #vmax=trk[dtg][2]
                #vmaxs.append(vmax)
                #sace9x=sace9x+vmax*vmax
                ##print'dd',dtg,trk[dtg][2]
                
            #time9x=(len(dtgs)-1)*6.0
            #timediff=(time2gen-time9x)
            #if(timediff < -6.0):
                #print 'WWW999 -- stmNN/9X: %s/%s   9Xlife %3.0f != time2gen: %3.0f  diff: %3.0f'%\
                #(stmnn,kk,time9x,time2gen,timediff)
            #print 'DDDD %s : %s  9X: %3.0f  Gen: %3.0f Diff: %2.0f   sace9x: %7.0f'%(stmnn,kk,time9x,time2gen,timediff,sace9x)
            
        
            
    
    #if(verb):
        #kksNN.sort()
        #for k in kksNN:
            #print 'kN:',k,sNN[k]
            
        #kks9X.sort()
        #for k in kks9X:
            #print 'k9:',k,s9X[k]

MF.dTimer('ALL')



sys.exit()


