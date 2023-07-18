#from tcbase import *
#from ga2 import setGA

#from WxMAP2 import *
#w2=W2()

#from M import *
#MF=MFutils()

#from M2 import setModel2

from subprocess import Popen, PIPE, STDOUT,check_output
import os,sys,glob,time,getopt,copy,getpass,struct,errno
import inspect
import shelve
import cPickle as pickle
from socket import gethostname,getfqdn
import datetime

from time import time as timer
from time import sleep,mktime
from types import StringType,IntType,FloatType,ListType,DictType,TupleType
from math import atan2,atan,pi,fabs,cos,sin,log,tan,acos,sqrt
import array

import zipfile
import filecmp


# -- VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVvvvvv
#

# -- VVVVVVVV -- hard-wire dirs
#
from sbtLocal import *

version='v03'

# -- VVVVVVVV - sBT dirs & vars
#

bm3year=2007
em3year=2023
 
sbtMeta='h-meta-sbt-%s-vars-csv.txt'%(version)
md3SumMeta='h-meta-md3-sum-csv.txt'
md3VarsMeta='h-meta-md3-vars-csv.txt'

sbtDatDir="%s/dat"%(sbtRoot)
sbtProdDir='%s/products/tcdiag'%(sbtRoot)
sbtSrcDir="%s/src"%(sbtRoot)
sbtVerDir="%s/%s"%(sbtRoot,version)
sbtVerDirDat="%s/%s/dat"%(sbtRoot,version)

geogDatDir="%s/geog"%(sbtVerDirDat)

tsbdbdir="%s/tcdiag"%(sbtDatDir)
adeckSdir="%s/adeck-dtg"%(sbtDatDir)
tmtrkbdir="%s/tmtrkN"%(sbtDatDir)
abdirStm='%s/adeck-stm'%(sbtDatDir)
abdirDtg='%s/adeck-dtg'%(sbtDatDir)


# -- VVVVVVVV -- basic constants and settings
#

pi=4.0*atan2(1.0,1.0)
pi4=pi/4.0
pi2=pi/2.0

deg2rad=pi/180.0
rad2deg=1.0/deg2rad

# -- earth ~ flattened sheriod r=6335.4 -> 6399.6 km
# this values is mean GC distance
#
rearth=6371.0

km2nm=60.0/(2*pi*rearth/360.0)
nm2km=1.0/km2nm
deglat2km=((2.0*pi*rearth)/360.0)
deglat2nm=60.0
knots2ms=1000.0/(km2nm*3600.0)
ms2knots=1.0/knots2ms

# -- units 
#
tcunits='metric'
tcunits='english'

# -- epsilon
#
epsilon=1e-10
epsilonm5=1.0e-5

# --- wmo gravity
#
gravity=9.80665

# -- VVVVVVVV -- mfbase
#
MandatoryPressureLevels=[1000,925,850,700,500,400,300,250,200,150,100,70,50,30,20,10]

# -- set units or 'metric'
#
units='english'

# -- 20030828 -- set calendar; can change by mf.calendar='365day'
#
calendar='gregorian'

# -- new future w3 vars for moving to hopper.orc.gmu.edu
# -- funny place to put because of the many imports

ptmpBaseDir=os.getenv('PTMP')


# -- VVVVVVVV -- tcVM.py
#

# tc parameters/limits
#
TCvmin=25.0
#TCvmin=30.0

vmaxTS=35.0
vmaxTY=65.0

IPerror=15.0 # nmi

ddtgTrack=6

Basin1toBasin2 = {
    'A':'IO',
    'B':'IO',
    'L':'AL',
    'I':'IO',
    'S':'SH',
    'P':'SH',
    'H':'SH', # -- to handle both s and p for shem
    'W':'WP',
    'C':'CP',
    'E':'EP',
    'Q':'SL',
    'T':'SA',
    'X':'XX',
}

Basin1toHemi = {
    'A':'nhem',
    'B':'nhem',
    'L':'nhem',
    'I':'nhem',
    'S':'shem',
    'P':'shem',
    'W':'nhem',
    'C':'nhem',
    'E':'nhem',
    'Q':'shem',
    'T':'shem',
    'H':'shem',
    'X':'XXXX',
}

Basin1toFullBasin = {
    'A':'nio',
    'B':'nio',
    'L':'lant',
    'I':'nio',
    'S':'shem',
    'H':'shem',
    'P':'shem',
    'W':'wpac',
    'C':'cpac',
    'E':'epac',
    'Q':'slant',
    'T':'slant',
    'X':'XXXXX',
}

Basin2toBasin1 = {
    'IO':'I',
    'SH':'P',
    'SH':'S',
    'SI':'S',
    'SP':'P',
    'WP':'W',
    'CP':'C',
    'EP':'E',
    'AT':'L',
    'AL':'L',
    'NA':'L',
    'SL':'Q',
    'SA':'T',
    'BB':'B',
    'AS':'A',
    'AA':'A',
    'XX':'X',
    # -- default in gettrk_gen.x  how he handles 'I' storms...
    'HC':'I',
}


ClimoBasinsHemi = {
    'NHS':['nhem','wpac','epac','lant','nio','shem','global'],
    'SHS':['shem','sio','swpac','nhem','global'],
}

Basin2toBasin1Tpc = {
    'IO':'I',
    'SP':'P',
    'SL':'Q',
    'SI':'S',
    'WP':'W',
    'CP':'C',
    'EP':'E',
    'AL':'L',
    'NA':'A',
    'BB':'B',
}


Basin1toBasin2 = {
    'A':'IO',
    'B':'IO',
    'L':'AT',
    'L':'AL',
    'I':'IO',
    'S':'SH',
    'P':'SH',
    'H':'SH',
    'W':'WP',
    'C':'CP',
    'E':'EP',
    'Q':'SL',
    'X':'XX',
}

Basin1toForecastCenter = {
    'A':'JTWC',
    'B':'JTWC',
    'L':'NHC',
    'I':'JTWC',
    'S':'JTWC',
    'P':'JTWC',
    'W':'JTWC',
    'C':'CPHC',
    'E':'NHC',
    'Q':'NHC',
    'X':'XHC',
}

Basin1toButtonStyle = {
    'A':'bnio',
    'B':'bnio',
    'L':'blant',
    'I':'bnio',
    'S':'bsio',
    'P':'bspac',
    'W':'bwpac',
    'C':'bcpac',
    'E':'bepac',
    'Q':'blant',
}

Basin1toButtonColor = {
    'A':'wheat',
    'B':'wheat',
    'L':'pink',
    'I':'wheat',
    'S':'#ADD8E6',
    'P':'#EE82EE',
    'W':'#EE82EE',
    'C':'lightgreen',
    'E':'lightgrey',
    'Q':'pink',
}

Basin1toBasinNumber = {
    'L':'1',
    'E':'2',
    'W':'3',
    'C':'4',
    'A':'5',
    'B':'6',
    'I':'7',
    'S':'8',
    'P':'9',
    'Q':'10',
}

Basin1toBasinName = {
    'A':'   ASEA - Arabian Sea',
    'B':'   BAYB - Bay of Bengal',
    'L':'   LANT - north Atlantic',
    'I':'    NIO - north Indian Ocean',
   'S':'    SIO - south Indian Ocean',
    'P':'  SPWAC - southwest Pacific',
    'W':'WESTPAC - western North Pacific',
    'C':'CENTPAC - central North Pacific',
    'E':'EASTPAC - eastern North Pacific',
    'Q':'  SLANT - south Atlantic'
}

Basin1toBasinNameShort = {
    'A':'ASEA',
    'B':'BAYB',
    'L':'LANT',
    'I':'NIO',
    'S':'SIO',
    'P':'SPWAC',
    'W':'WESTPAC',
    'C':'CENTPAC',
    'E':'EASTPAC',
    'Q':'SLANT'
}

Basin1toHemi1 = {
    'A':'N',
    'B':'N',
    'L':'N',
    'I':'N',
    'S':'S',
    'P':'S',
    'W':'N',
    'C':'N',
    'E':'N',
    'Q':'S',
}

Basin1toHemi3 = {
    'A':'NHS',
    'B':'NHS',
    'L':'NHS',
    'I':'NHS',
    'S':'SHS',
    'P':'SHS',
    'W':'NHS',
    'C':'NHS',
    'E':'NHS',
    'Q':'SHS',
}

Basin1toHemi4 = {
    'A':'nhem',
    'B':'nhem',
    'L':'nhem',
    'I':'nhem',
    'S':'shem',
    'P':'shem',
    'W':'nhem',
    'C':'nhem',
    'E':'nhem',
    'Q':'shem',
}

Basin1toBasin3 = {
    'A':'nio',
    'B':'nio',
    'I':'nio',
    'L':'atl',
    'S':'shm',
    'P':'shm',
    'W':'wpc',
    'C':'epc',
    'E':'epc',
    'Q':'slt',
    'T':'slt',
}


SuperBasins=['NHS','SHS','LTS','WPS','EPS','NIS']

Hemi1toHemiName = {
    'NHS':'NHEM Super Basin',
    'SHS':'SHEM Super Basin',
    'LTS':'LANT Super Basin',
    'WPS':'WPAC Super Basin',
    'EPS':'EPAC Super Basin',
    'NIS':'NIO  Super Basin',
}

Hemi3toHemiName = {
    'NHS':'NHEM Super Basin',
    'SHS':'SHEM Super Basin',
    'LTS':'LANT Super Basin',
    'WPS':'WPAC Super Basin',
    'EPS':'EPAC Super Basin',
    'NIS':'NIO  Super Basin',
}

Hemi3toHemiNameShort = {
    'NHS':'NHEM',
    'SHS':'SHEM',
    'LTS':'LANT SB',
    'WPS':'WPAC SB',
    'EPS':'EPAC SB',
    'NIS':'NIO  SB',
}

Hemi1toHemiVeriName = {
    'NHS':'nhem',
    'SHS':'shem',
    'LTS':'lant',
    'WPS':'wpac',
    'EPS':'epac',
    'NIS':'nio',
}

Hemi1toBasins = {
    'NHS':('A','B','I','W','C','E','L'),
    'SHS':('S','P','Q'),
    'LTS':('L'),
    'WPS':('W'),
    'EPS':('C','E'),
    'NIS':('A','B','I'),
}

Hemi3toBasins = {
    'NHS':('A','B','I','W','C','E','L'),
    'SHS':('S','P','Q'),
    'LTS':('L'),
    'WPS':('W'),
    'EPS':('C','E'),
    'NIS':('A','B','I'),
}

Hemi3toSuperBasins = {
    'NHS':('NHS','NIS','WPS','EPS','LTS'),
    'SHS':('SHS','S','P','Q'),
}

BasinsAll=['L','E','C','W','A','B','I','S','P','Q']


TcGenBasin2Area={
    'lant':'troplant',
    'epac':'tropepac',
    'wpac':'tropwpac',
    'shem':'tropshem',
    'nio':'tropnio',
}

TcGenBasin2PrwArea={
    'lant':'prwLant',
    'epac':'prwEpac',
    'cepac':'prwCEpac',
    'wpac':'prwWpac',
    'shem':'prwSpac',
    'nio':'prwIo',
}

TcGenBasin2B1ids={
    'lant':['l'],
    'epac':['c','e'],
    'wpac':['w'],
    'shem':['s','p'],
    'nio':['a','b'],
}


tdmin=25.0
tsmin=35.0
tymin=65.0
stymin=130.0

peakNhemMMDDHH='090100'
peakShemMMDDHH='021500'

#primeMeridianChk=60.0 -- too big for AS, e.g., 01A.12
primeMeridianChk=30.0

centerid='MFTC'
tcVcenterid='M2TC'

maxNNnum=49

# -- VVVVVVVV - w2base/ga2
#


tcVcenterid='M3TC'
global undef,taus,oPrsizMin,\
       radInfPrKm,radInfPrNM,\
       radInfPrKM,radkms,oPrpre

undef=-999.0
undefVar=1e20

taus=[0,12,24,48,72]
taus=[0,6,12,18,24]
taus=[6,12,18]
taus=[6,12]
# -- only using 6-h precip accumulations...
taus=[6]

oPrsizMin=0
radInfPrKm=[300,500,800]
radInfPrNM={}
radInfPrKM={}

def nint(f):
    if(f>=0.0): rc=int(f+0.5)
    if(f<=0.0): rc=int(f-0.5)
    return(rc)

for rad in radInfPrKm:
    radn=nint(rad*km2nm)*1.0
    radInfPrNM[rad]=radn
    radInfPrKM[radn]=rad
    
radkms=radInfPrNM.keys()
radkms.sort()

oPrpre='pr'
mname = {
'01':'January',
'02':'February',
'03':'March',
'04':'April',
'05':'May',
'06':'June',
'07':'July',
'08':'August',
'09':'September',
'10':'October',
'11':'November',
'12':'December'
}

mname3 = {
'01':'Jan',
'02':'Feb',
'03':'Mar',
'04':'Apr',
'05':'May',
'06':'Jun',
'07':'Jul',
'08':'Aug',
'09':'Sep',
'10':'Oct',
'11':'Nov',
'12':'Dec'
}

cname3 = {
'JAN':'01',
'FEB':'02',
'MAR':'03',
'APR':'04',
'MAY':'05',
'JUN':'06',
'JUL':'07',
'AUG':'08',
'SEP':'09',
'OCT':'10',
'NOV':'11',
'DEC':'12'
}



#
#  add 0 for indexing by month vice month-1
#
mday=(0,31,28,31,30,31,30,31,31,30,31,30,31)
mdayleap=(0,31,29,31,30,31,30,31,31,30,31,30,31)
aday=(1,32,60,91,121,152,182,213,244,274,305,335)
adayleap=(1,32,61,92,122,153,183,214,245,275,306,336)


sec2hr=1/3600.0


# -- MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM

# -- MMMMMMMMMM - py methods
#

def ndayyr(yyyy):
    nd=365
    if (int(yyyy)%4 == 0): nd=366
    return(nd)

def ndaymo(yyyymm):
    yyyy=string.atoi(yyyymm[0:4])
    mm=string.atoi(yyyymm[4:6])

    leap=0
    if (yyyy%4 == 0): leap=1

    #
    # override leaping if 365 day calendar
    #
    if(calendar == '365day'): leap=0

    if(leap):
        return(mdayleap[mm])
    else:
        return(mday[mm])


def TimeZoneName():

    import time
    tz=time.tzname
    tz=tz[time.daylight]
    return(tz)


def Dtg2JulianDay(dtg):

    import time
    year=int(str(dtg)[0:4])
    month=int(str(dtg)[4:6])
    day=int(str(dtg)[6:8])

    t = time.mktime((year, month, day, 0, 0, 0, 0, 0, 0))
    jday=time.gmtime(t)[7]
    jday="%03d"%(int(jday))
    return (jday)

def YearJulianDay2YMD(year,jday):

    from datetime import date,timedelta
    ymd=date(int(str(year)),1,1) + timedelta(int(str(jday))-1)
    ymd=ymd.strftime("%Y%m%d")
    return(ymd)



def dtg6(opt="default"):

    import time
    tzname=" %s "%(TimeZoneName())

    if (opt == "curtime" or opt == "curtimeonly" ):t=time.localtime(time.time())
    else:t=time.gmtime(time.time())

    yr="%04d" % t[0]
    mo="%02d" % t[1]
    dy="%02d" % t[2]
    hr="%02d" % t[3]
    fhr="%02d" % (int(t[3]/6)*6)
    mn="%02d" % t[4]
    sc="%02d" % t[5]

    if opt == "default":
        dtg=yr + mo + dy + fhr
    elif opt == "dtg.hm":
        dtg=yr + mo + dy + fhr + " " + hr + ":" + mn
    elif (opt == "timeonly"):
        dtg=hr+":"+mn+":"+sc+ " UTC "
    elif (opt == "time"):
        dtg=hr+":"+mn+":"+sc+ " UTC " + str(t[2]) + " " + mname[mo] + ", " + yr
    elif (opt == "curtime"):
        dtg=hr+":"+mn+":"+sc+ tzname + str(t[2]) + " " + mname[mo] + ", " + yr
    else:
        dtg=yr + mo + dy + fhr + " " + hr + ":" + mn

    return(dtg)

def dtg(opt="default"):

    import time
    
    from datetime import datetime
    from dateutil import tz
    
    tzname=" %s "%(TimeZoneName())
    
    from_zone = tz.gettz('UTC')
    to_zone   = tz.gettz('America/Denver')

    if (opt == "curtime" or opt == "curtimeonly" or opt == 'cur_hms'):
        t=time.localtime(time.time())
    else:
        t=time.gmtime(time.time())

    yr="%04d" % t[0]
    mo="%02d" % t[1]
    dy="%02d" % t[2]
    hr="%02d" % t[3]
    fhr="%02d" % (int(t[3]/6)*6)
    phr=int(t[3])%6
    mn="%02d" % t[4]
    sc="%02d" % t[5]
    fphr=float(phr)*1.0 + float(mn)/60.0;

    if opt == "default":
        dtg=yr + mo + dy + fhr
    elif opt == "phr":
        dtg="%4.2f"%(fphr)
    elif opt == "fphr":
        dtg=fphr
    elif opt == "dtg.hm":
        dtg=yr + mo + dy + fhr + " " + hr + ":" + mn
    elif opt == "cur.hm":
        dtg=yr + mo + dy + " " + hr + ":" + mn
    elif opt == "dtg.phm":
        cphr="%02d"%(phr)
        dtg=yr + mo + dy + fhr + " " + cphr + ":" + mn
    elif opt == "dtg.phms":
        cphr="%02d"%(phr)
        dtg=yr + mo + dy + fhr + " " + cphr + ":" + mn + ":" + sc
    elif opt == "dtgmn":
        dtg=yr + mo + dy +  hr + mn
    elif opt == "dtg_mn":
        dtg=yr + mo + dy +  hr + '_%s'%(mn)
    elif opt == "dtg_ms":
        dtg=yr + mo + dy +  hr + "_%s_%s"%(mn,sc)
    elif opt == "dtg_hms":
        dtg=yr + mo + dy + "_%s_%s_%s"%(hr,mn,sc)
    elif opt == "cur_hms":
        dtg="  ---> CurDT: " + yr + mo + dy + " %s:%s:%s <---"%(hr,mn,sc)
    elif opt == "dtg.hm":
        dtg=yr + mo + dy + fhr + " " + hr + ":" + mn
    elif opt == "dtg.hms":
        dtg=yr + mo + dy +  " " + hr + ":" + mn + ":" + sc
    elif opt == "dtgcurhr":
        dtg=yr + mo + dy + hr
    elif (opt == "timeonly"):
        dtg=hr+":"+mn+":"+sc+ " UTC "
    elif (opt == "time"):
        dtg=hr+":"+mn+":"+sc+ " UTC " + str(t[2]) + " " + mname[mo] + ", " + yr
    elif (opt == "curtime"):
        dtg=hr+":"+mn+":"+sc+ tzname + str(t[2]) + " " + mname[mo] + ", " + yr
    elif (opt == "curtimeonly"):
        dtg=hr+":"+mn+":"+sc+ tzname
    else:
        dtg=yr + mo + dy + fhr + " " + hr + ":" + mn

    return(dtg)

def dtg12(opt="default"):
    import time
    tzname=" %s "%(TimeZoneName())

    if (opt == "curtime" or opt == "curtimeonly" ):t=time.localtime(time.time())
    else:t=time.gmtime(time.time())

    yr="%04d" % t[0]
    mo="%02d" % t[1]
    dy="%02d" % t[2]
    hr="%02d" % t[3]
    fhr="%02d" % (int(t[3]/12)*12)
    phr=int(t[3])%12
    mn="%02d" % t[4]
    sc="%02d" % t[5]
    fphr=float(phr)*1.0 + float(mn)/60.0;

    if opt == "default":
        dtg=yr + mo + dy + fhr
    elif opt == "phr":
        dtg="%4.2f"%(fphr)
    elif opt == "fphr":
        dtg=fphr
    elif opt == "dtg.hm":
        dtg=yr + mo + dy + fhr + " " + hr + ":" + mn
    elif (opt == "timeonly"):
        dtg=hr+":"+mn+":"+sc+ " UTC "
    elif (opt == "time"):
        dtg=hr+":"+mn+":"+sc+ " UTC " + str(t[2]) + " " + mname[mo] + ", " + yr
    elif (opt == "curtime"):
        dtg=hr+":"+mn+":"+sc+ tzname + str(t[2]) + " " + mname[mo] + ", " + yr
    elif (opt == "curtimeonly"):
        dtg=hr+":"+mn+":"+sc+ tzname
    else:
        dtg=yr + mo + dy + fhr + " " + hr + ":" + mn

    return(dtg)


def isRealTime(tdtgs,age=72.0):
    curdtg=dtg()
    alldtgs=tdtgs
    if(type(tdtgs) != ListType): alldtgs=[tdtgs]
    
    rc=1
    for tdtg in alldtgs:
        dtgd=dtgdiff(tdtg,curdtg)
        if(dtgd > age): 
            rc=0
            break
        
    return(rc)
    

def rhh2hhmm(hh):

    if(hh < 0):
        rhh=abs(hh)
        lt0=1
    else:
        rhh=hh
        lt0=0

    imm=int(rhh*60.0+0.5)
    ihh=imm/60
    imm=imm%60
    if(lt0):
        ohhmm="-%02d:%02d"%(ihh,imm)
    else:
        ohhmm="+%02d:%02d"%(ihh,imm)

    return(ohhmm)



def yyyymmrange(byyyymm,eyyyymm,inc=1):

    yyyymms=[]

    byyyymm=str(byyyymm)
    eyyyymm=str(eyyyymm)

    yyyymm=byyyymm

    while(yyyymm<=eyyyymm):
        yyyymms.append(yyyymm)
        yyyymm=yyyymminc(yyyymm,inc)


    return(yyyymms)

def yyyyrange(byyyy,eyyyy,inc=1):

    yyyys=[]

    byyyy=str(byyyy)
    eyyyy=str(eyyyy)

    yyyy=byyyy

    while(yyyy<=eyyyy):
        yyyys.append(yyyy)
        yyyy=yyyyinc(yyyy,inc)

    return(yyyys)



def yyyymmdiff(yyyymm1,yyyymm2):

    yyyy1=int(yyyymm1[0:4])
    yyyy2=int(yyyymm2[0:4])
    mm1=int(yyyymm1[4:6])
    mm2=int(yyyymm2[4:6])
    dyyyy=yyyy2-yyyy1
    dmm=mm2-mm1+1

    dyyyymm=(dyyyy*12)+dmm

    return(dyyyymm)


def yyyymminc(yyyymm,inc=1):
    yyyy=int(yyyymm[0:4])
    mm=int(yyyymm[4:6])
    mm=mm+inc
    if mm > 12:
        mm=mm-12
        yyyy=yyyy+1
    if mm < 1:
        mm=mm+12
        yyyy=yyyy-1

    nyyyymm="%04d%02d"%(yyyy,mm)
    return(nyyyymm)

def yyyyinc(yyyy,inc):

    yyyy=int(yyyy)

    nyyyy=yyyy+inc

    nyyyy="%04d"%(nyyyy)
    return(nyyyy)

def IsLeapYear(yyyy):
    rc=0
    if(yyyy%4 == 0 and (yyyy%100 != 0) or (yyyy%400 == 0)):
        rc=1
    return(rc)


def dtginc(idtg,off):

    dtg=str(idtg)
    
    if(len(dtg) == 10):
        yr=int(dtg[0:4])    
        mo=int(dtg[4:6])
        dy=int(dtg[6:8])
        hr=int(dtg[8:10])
    elif(len(dtg) == 11):
        yr=int(dtg[0:5])    
        mo=int(dtg[5:7])
        dy=int(dtg[7:9])
        hr=int(dtg[9:11])
        
    hr=hr+int(off)

    #
    # do leap if going forward in time
    #

    leap=0

    #200201120
    # problem, limit backward offset
    #
    if (IsLeapYear(yr) and off > -120): leap=1

    #
    # turn off leap of 365 day calendar
    #
    if(calendar == '365day'): leap=0

    ndyyr=365+leap

    jdy=dy-1

    ada=aday[mo-1]
    if leap == 1:ada=adayleap[mo-1];
    jdy=jdy+ada

    while hr >= 24:
        hr=hr-24
        jdy=jdy+1

    while hr < 0:
        hr=hr+24
        jdy=jdy-1

    if jdy <= 0:
        yr=yr-1
        leap=0
        if(IsLeapYear(yr)):
            leap=1
            ndyyr=366
            if(calendar == '365day'):
                leap=0
                ndyyr=365
        else:
            ndyyr=365

        jdy=jdy+ndyyr

    if jdy > ndyyr:
        jdy=jdy-ndyyr
        yr=yr+1
        leap=0
        if(IsLeapYear(yr)):
            leap=1
            ndyyr=366
            if(calendar == '365day'):
                leap=0
                ndyyr=365
        else:
            ndyyr=365

    if(calendar == '365day'): leap=0

    i=11
    if leap == 1:
        while(jdy<adayleap[i]):i=i-1
        ndy=jdy-adayleap[i]+1
    else:
        while(jdy<aday[i]):i=i-1
        ndy=jdy-aday[i]+1

    yr="%04d"%yr
    mo="%02d"%(i+1)
    dy="%02d"%ndy
    hr="%02d"%hr

    ndtg=yr+mo+dy+hr

    return(ndtg)

def dtg2time(dtg):


    cdtg=str(dtg)

    try:
        yy=int(cdtg[0:4])
        mm=int(cdtg[4:6])
        dd=int(cdtg[6:8])
        hh=int(cdtg[8:10])

        ct=(yy,mm,dd,hh,0,0,0,0,0)
        time=mktime(ct)
    except:
        print 'dtg2time: invalid dtg: ',dtg,' sayoonara'
        sys.exit()

    return(time)

def dtgmn2time(dtg):

    from time import mktime 

    cdtg=str(dtg)

    yy=int(cdtg[0:4])
    mm=int(cdtg[4:6])
    dd=int(cdtg[6:8])
    hh=int(cdtg[8:10])
    mn=int(cdtg[10:12])

    ct=(yy,mm,dd,hh,mn,0,0,0,0)
    time=mktime(ct)
    return(time)


def dtgdiff(dtg1,dtg2):

    #from time import *

    dtg1=str(dtg1)
    dtg2=str(dtg2)

    yyyy1=int(dtg1[0:4])
    yyyy2=int(dtg2[0:4])

    offyear=1981
    if(yyyy1%4==0):
        offyear=1980
    if(yyyy2%4==0):
        offyear=1979

    #
    # override leaping if 365 day calendar
    #
    if(calendar == '365day'): offyear=1981

    #
    # 20030828 -- fix crossing year if offsetting
    #

    dyyyy=yyyy2-yyyy1

    if(yyyy1 < offyear or yyyy2 < offyear):
        dtg1off=offyear-int(dtg1[0:4])
        dtg1="%04d"%(offyear)+dtg1[4:10]
        dtg2="%04d"%(offyear+dyyyy)+dtg2[4:10]

    t1=dtg2time(dtg1)
    t2=dtg2time(dtg2)
    nhr=(t2-t1)*sec2hr

    return(nhr)

def dtgmndiff(dtgmn1,dtgmn2):

    #from time import *

    dtgmn1=str(dtgmn1)
    dtgmn2=str(dtgmn2)

    yyyy1=int(dtgmn1[0:4])
    yyyy2=int(dtgmn2[0:4])

    offyear=1981
    if(yyyy1%4==0):
        offyear=1980
    if(yyyy2%4==0):
        offyear=1979

    #
    # override leaping if 365 day calendar
    #
    if(calendar == '365day'): offyear=1981

    #
    # 20030828 -- fix crossing year if offsetting
    #

    dyyyy=yyyy2-yyyy1

    if(yyyy1 < offyear or yyyy2 < offyear):
        dtg1off=offyear-int(dtg1[0:4])
        dtg1="%04d"%(offyear)+dtgmn1[4:10]
        dtg2="%04d"%(offyear+dyyyy)+dtgmn2[4:10]

    t1=dtgmn2time(dtgmn1)
    t2=dtgmn2time(dtgmn2)
    nhr=(t2-t1)*sec2hr

    return(nhr)


def dtgShift0012(dtg,round=1):

    bstart=8
    if(len(dtg) == 11): bstart=9
    
    if(round):
        if(dtg[bstart:] == '06' or dtg[bstart:] == '18'):
            odtg=dtginc(dtg,6)
        else:
            odtg=dtg
    else:
        if(dtg[bstart:] == '06' or dtg[bstart:] == '18'):
            odtg=dtginc(dtg,-6)
        else:
            odtg=dtg

    return(odtg)


def dtgrange(dtg1,dtg2,inc=6):

    verb=0

    inc=int(inc)
    dtg1=str(dtg1)
    dtg2=str(dtg2)

    if(verb): print 'ddd dtgrange',dtg1,dtg2,inc

    if(inc > 0 and dtg2 < dtg1 and inc > 0):
        print "EEE invalid edtg (before bdtg) in dtgrange: dtg1: %s  dtg2: %s"%(dtg1,dtg2)
        sys.exit()

#
# return dtg1 if dtg1=dtg2
#
    if(dtg1 == dtg2):
        dtgs=[dtg1]
        return(dtgs)

#
# pre 1970? problem
#
    dtg1off=0

    yyyy1=int(dtg1[0:4])
    yyyy2=int(dtg2[0:4])

    offyear=1981
    #
    # 20031114 fix problem when begin/end year are the same
    #
    if(yyyy1%4 == 0 and yyyy2%4 == 0):
        offyear=1980
    if(yyyy2%4 == 0 and yyyy1%4 != 0):
        offyear=1979

    if(verb): print 'aaa ',yyyy1,yyyy2,yyyy1%4,yyyy2%4,offyear
    #
    # override leaping if 365 day calendar
    #
    if(calendar == '365day'): offyear=1981

    #
    # 20030828 -- fix crossing year if offsetting
    #

    dyyyy=yyyy2-yyyy1

    if(verb): print 'bbb ',dtg1,dtg2,yyyy1,yyyy2,offyear
    if(yyyy1 < offyear or yyyy2 < offyear):
        dtg1off=offyear-int(dtg1[0:4])
        dtg1="%04d"%(offyear)+dtg1[4:10]
        dtg2="%04d"%(offyear+dyyyy)+dtg2[4:10]

    t1=dtg2time(dtg1)
    t2=dtg2time(dtg2)


    nhr=(t2-t1)*sec2hr
    dtgs=[]
    dtgo=str(dtg1)

    if(inc > 0):
        ntime=nhr/inc
        if(verb): print 'ddd dtgrange',ntime,nhr,inc
        dtga=dtgo
        dtgs.append(dtga)
        i=1
        while(i<=ntime):
            dtgn=dtginc(dtgo,inc)
            dtga=dtgn
            dtgs.append(dtga)
            dtgo=dtgn
            i=i+1

        if(dtg1off != 0):
            i=0
            for dtg in dtgs:
                yyyy=int(dtg[0:4])-dtg1off
                dtga="%04d%s"%(yyyy,dtg[4:10])
                dtgs[i]=dtga
                i=i+1

    elif(inc <  0):
        dtgo=str(dtg1)
        ntime=abs(nhr/inc)
        if(verb): print 'ddd ------------ dtgrange',ntime,nhr,inc
        dtga=dtgo
        dtgs.append(dtga)
        i=1
        while(i<=ntime):
            dtgn=dtginc(dtgo,inc)
            dtga=dtgn
            dtgs.append(dtga)
            dtgo=dtgn
            i=i+1

        if(dtg1off != 0):
            i=0
            for dtg in dtgs:
                yyyy=int(dtg[0:4])-dtg1off
                dtga="%04d%s"%(yyyy,dtg[4:10])
                dtgs[i]=dtga
                i=i+1

    else:
        dtgs=[-999]

    return(dtgs)

def dtg2ymdh(dtg):

    cdtg=str(dtg)
    if(len(cdtg) == 10):
        yy=cdtg[0:4]
        mm=cdtg[4:6]
        dd=cdtg[6:8]
        hh=cdtg[8:10]
        
    elif(len(cdtg) == 11):
        yy=cdtg[0:5]
        mm=cdtg[5:7]
        dd=cdtg[7:9]
        hh=cdtg[9:11]
        
    else:
        yy=cdtg[0:2]
        mm=cdtg[2:4]
        dd=cdtg[4:6]
        hh=cdtg[6:8]
        yy='19'+yy

    return(yy,mm,dd,hh)

def dtg2vtime(dtg):

    tt=dtg2time(dtg)
    gmt=gmtime(tt)
    #vtime=strftime("%a %HZ %d %b %y",gmt)
    vtime=strftime("%a %d %b %HZ",gmt)
    return(vtime)

def dtg2gtime(dtg):
    try:
        (y,m,d,h)=dtg2ymdh(dtg)
    except:
        return(none)
    mo=mname3[m]
    gtime="%sZ%s%s%s"%(h,d,mo,y)
    return(gtime)

def yyyymm2gtime(yyyymm):
    y=yyyymm[0:4]
    m=yyyymm[4:]
    mo=mname3[m]
    gtime="%s%s"%(mo,y)
    return(gtime)

def gtime2dtg(gtime):
    h=gtime[0:2]
    d=gtime[3:5]
    m=gtime[5:8]
    y=gtime[8:]
    cm=cname3[m]
    dtg=y+cm+d+h
    return(dtg)

def chomp(string):
    ss=string[:-1]
    return ss

def uniq(ulist):
    weirdtest='asdasdfasdfasdfasdf'
    #
    # sort before length check for case of two
    #
    ulist.sort()
    rlist=[]

    if(len(ulist) > 2):
        test=ulist[1]
        test=weirdtest
    elif(len(ulist) == 0):
        return(rlist)
    else:
        test=ulist[0]

    if(test != weirdtest):
        rlist.append(test)

    for l in ulist:
        #if(repr(l) != repr(test)):
        if(l != test):
            rlist.append(l)
            test=l
    return(rlist)


def fopen(file,state='r'):
    from sys import exit
    try:
        fh=open(file,state)
        return(fh)
    except:
        print "unable to open: ",file,"\nsayoonara"
        exit()


def argopt(i):
    import sys
    try:
        if(sys.argv[i]):
            return(1)
    except:
        return(0)


def dtg_dtgopt_prc(dtgopt,ddtg=6):

    ddc=dtgopt.split(',')
    
    if(len(ddc) > 1):
        dtgs=[]
        for dc in ddc:
            if(find(dc,'.') or len(dc) != 10):
                dtgs=dtgs+dtg_dtgopt_prc(dc)
            else:
                dtgs.append(dc)
        return(dtgs)


    dd=dtgopt.split('.')
    if(len(dd) == 1):
        if(len(dtgopt) == 6 and dtgopt.isdigit()):
            bdtg="%s0100"%(dtgopt)
            edtg=dtginc("%s0100"%(yyyymminc(dtgopt,1)),-6)

        else:
            bdtg=dtg_command_prc(dtgopt)
            edtg=bdtg

    if(len(dd) >= 2):

        if(len(dd[0]) == 6 and dd[1].isdigit()):
            bdtg="%s0100"%(dd[0])
        else:
            bdtg=dtg_command_prc(dd[0])
 
        if(len(dd[0]) == 6):
            if(dd[1].isdigit()):
                if(len(dd[1]) == 6):
                    edtg=dtginc("%s0100"%(yyyymminc(dd[1],1)),-6)
                elif(len(dd[1]) == 2 or dd[1] == '6'):
                    edtg=dtginc("%s0100"%(yyyymminc(dd[0],1)),-int(dd[1]))
                    ddtg=int(dd[1])
            else:
                edtg=dtg_command_prc(dd[1])    
        else:
            edtg=dtg_command_prc(dd[1])

    if(len(dd) == 3):
        ddtg=dd[2]

    if(find(dtgopt,'cur12')): ddtg=12

    dtgs=dtgrange(bdtg,edtg,ddtg)

    if(dtgs[0] == '-1'):
        print 'EEE dtg_dtgopt_prc bad dtgopt: ',dtgopt
        sys.exit()

    return(dtgs)


def dtg_command_prc(dtg,quiet=0,curdtg12=0,opsfhr=5.0):

    odtg=dtg
    if(curdtg12):
        curdtg=dtg12()
    else:
        curdtg=dtg6()

    if(dtg == 'cur+12'):
        odtg=dtginc(curdtg,+12)
    elif(dtg == 'cur+6'):
        odtg=dtginc(curdtg,+6)
    elif(dtg == 'cur'):
        odtg=curdtg
    elif(dtg == 'cur12'):
        odtg=dtg12()
    elif(dtg == 'cur-6'):
        odtg=dtginc(curdtg,-6)
    elif(dtg == 'cur-12'):
        odtg=dtginc(curdtg,-12)
    elif(dtg == 'cur-18'):
        odtg=dtginc(curdtg,-18)
    elif(dtg == 'cur-24'):
        odtg=dtginc(curdtg,-24)
    elif(dtg == 'cur-30'):
        odtg=dtginc(curdtg,-30)
    elif(dtg == 'cur-36'):
        odtg=dtginc(curdtg,-36)
    elif(dtg == 'cur-42'):
        odtg=dtginc(curdtg,-42)
    elif(dtg == 'cur-48'):
        odtg=dtginc(curdtg,-48)
    elif(dtg == 'cur-d1'):
        odtg=dtginc(curdtg,-24)

    elif(find(dtg,'cur-')  and not(find(dtg,'cur-d')) ):
        ld=len(dtg)
        nhr=int(dtg[4:ld])
        odtg=dtginc(curdtg,-1*nhr)

    elif(find(dtg,'cur12-')  and not(find(dtg,'cur12-d')) ):
        ld=len(dtg)
        nhr=int(dtg[6:ld])
        odtg=dtginc(dtg12(),-1*nhr)

    elif(find(dtg,'cur+') and not(find(dtg,'cur+d')) ):
        ld=len(dtg)
        nhr=int(dtg[4:ld])
        odtg=dtginc(curdtg,nhr)

    elif(find(dtg,'cur12+') and not(find(dtg,'cur12+d')) ):
        ld=len(dtg)
        nhr=int(dtg[6:ld])
        odtg=dtginc(curdtg,nhr)

#
# -dXXX
#
    elif(find(dtg,'cur-d')):
        ld=len(dtg)
        nday=int(dtg[5:ld])
        odtg=dtginc(curdtg,-1*nday*24)

    elif(find(dtg,'cur12-d')):
        ld=len(dtg)
        nday=int(dtg[7:ld])
        odtg=dtginc(dtg12(),-1*nday*24)

    elif(find(dtg,'cur+d')):
        ld=len(dtg)
        nday=int(dtg[5:ld])
        odtg=dtginc(curdtg,nday*24)

    elif(find(dtg,'cur12+d')):
        ld=len(dtg)
        nday=int(dtg[7:ld])
        odtg=dtginc(curdtg,nday*24)

    elif(dtg == 'ops12'):
        odtg=dtg12()
        fphr=float(dtg12('fphr'))
        if(fphr <= opsfhr):
            odtg=dtginc(odtg,-12)
    elif(dtg == 'ops12long'):
        opsfhrl=11.0
        odtg=dtg12()
        fphr=float(dtg12('fphr'))
        if(fphr <= opsfhrl):
            odtg=dtginc(odtg,-12)
    elif(dtg == 'ops6'):
        (odtg,phr)=dtg_phr_command_prc('cur')
        fphr=float(phr)
        if(fphr <= opsfhr*0.5):
            odtg=dtginc(odtg,-6)

    if(len(odtg) != 10):
        if(quiet != 0):
            print "EEE odtg ",odtg," fouled len: ",len(odtg)
        odtg=-1

    if(len(dtg.split('.')) > 1):
        odtg=len(dtg.split('.'))

    return(odtg)

def dtg_phr_command_prc(idtg):

    curdtg=dtg()
    curphr=dtg('phr')

    ddtg=-9999

    odtg=dtg_command_prc(idtg)

    if(ddtg != -9999):
        odtg=dtginc(curdtg,ddtg)

    if(len(odtg) != 10):
        print "EEE odtg ",odtg," fouled len: ",len(odtg)
        odtg=-1
        ocurphr=-1
        return(odtg,ocurphr)

    deltadtg=dtgdiff(odtg,curdtg)
    curphr=float(curphr)+float(deltadtg)

    if(curphr >= 0.0 and curphr < 10.0):
        ocurphr="+%3.2f"%(curphr)
    elif(curphr >= 10.0 and curphr < 100.0):
        ocurphr="+%4.2f"%(curphr)
    elif(curphr >= 100.0 and curphr < 1000.0):
        ocurphr="+%5.2f"%(curphr)

    else:
        ocurphr="%7.2f"%(curphr)


    return(odtg,ocurphr)


def dtg_12_command_prc(idtg):

    odtg=idtg
    curdtg=dtg()
    if(idtg == 'cur+12'):
        odtg=dtginc(curdtg,+12)
    elif(idtg == 'cur'):
        odtg=curdtg
    elif(idtg == 'cur-12'):
        odtg=dtginc(curdtg,-12)
    elif(idtg == 'cur-24'):
        odtg=dtginc(curdtg,-24)

    if(len(odtg) != 10):
        print "EEE odtg ",odtg," fouled len: ",len(odtg)

    return(odtg)

def cur2dtg(idtg):

    odtg=idtg

    curdtg=dtg6()

    if(idtg == 'cur+12'): odtg=dtginc(curdtg,+12)
    if(idtg == 'cur+6'): odtg=dtginc(curdtg,+6)
    if(idtg == 'cur'): odtg=curdtg
    if(idtg == 'cur-6'): odtg=dtginc(curdtg,-6)
    if(idtg == 'cur-12'): odtg=dtginc(curdtg,-12)
    if(idtg == 'cur-18'): odtg=dtginc(curdtg,-18)
    if(idtg == 'cur-24'): odtg=dtginc(curdtg,-24)
    if(idtg == 'cur-36'): odtg=dtginc(curdtg,-36)
    if(idtg == 'cur-48'): odtg=dtginc(curdtg,-48)


    if(len(odtg) != 10):
        print "EEE odtg ",odtg," fouled len: ",len(odtg)

    return(odtg)

# --------- python cookbood p.228 -- capture stderr/stdout
#
# -- turn off buffering

## def makeNonBlocking(fd):
##     fl = fcntl.fcntl(fd, FCNTL.F_GETFL)
##     try:
##         fcntl.fcntl(fd, FCNTL.F_SETFL,fl | FCNTL.O_NDELAY)
##     except AttributeError:
##         fcntl.fcntl(fd, FCNTL.F_SETFL,fl | FCNTL.NDELAY)

## def getCommandOutput(command,erropt='stderr'):

##     child = popen2.Popen3(command, 1)
##     child.tochild.close()
##     outfile = child.fromchild
##     outfd = outfile.fileno()
##     errfile = child.childerr
##     errfd = errfile.fileno()

##     makeNonBlocking(outfd)
##     makeNonBlocking(errfd)

##     outdata = errdata = ''
##     outeof = erreof = 0

##     while 1:

##         ready = select.select([outfd,errfd],[],[]) # wait for input

##         if outfd in ready[0]:
##             outchunk = outfile.read()
##             if outchunk == '': outeof = 1
##             outdata = outdata + outchunk

##         if errfd in ready[0]:
##             errchunk = errfile.read()
##             if errchunk == '': erreof = 1
##             errdata = errdata + errchunk

##         if outeof and erreof: break
##         select.select([],[],[],.1) # allow a little time for buffers to fill

##     err = child.wait()

##     if err != 0:

##         if(erropt != 'nostderr'):
##             print "EEE: %s failed with the exit code %d\nEEE: %s" % ( command, err, errdata)

##         return outdata
## #        raise RuntimeError, "%s failed with the exit code %d\n%s" % ( command, err, errdata)

##     return outdata


def getCommandOutput2(command):
    child = os.popen(command)
    data = child.read()
    err= child.close()
    if err:
        raise RuntimeError, '%s failed with the exit code %d\n' % (command,err)
    return data



def runcmd(command,logpath='straightrun',lsopt='',prefix='',postfix=''):

    if(logpath == ''):
        logpath='straightrun'

    oprefix=''
    if(prefix != ''): oprefix="(%s)"%(prefix)
    
    opostfix=''
    if(postfix != ''): opostfix="[%s]"%(postfix)

    if(logpath == 'straightrun' or logpath == 'norun'):

        curtime=dtg('cur_hms')
        occc="CCC"
        if(oprefix != ''): occc="%s(%s)"%(occc,oprefix)
        if(lsopt != 'q'): print "%s: %s %s %s"%(occc,command,curtime,opostfix)
        if(logpath != 'norun'): os.system(command)
        return

    if(logpath == 'quiet'):
        os.system(command)
        return

    global LF

    #
    # output to log file (append and add title line)
    #

    if(logpath != 'nologpath'):

        log=getCommandOutput2(command)

        lout="\nTTT: %s  :: CCC: %s\n\n"%(dtg6('curtime'),command)
        lout=lout+log

        if(not(os.path.exists(logpath))):
            try:
                LF=open(logpath,'a')
                LF.writelines(lout)
                LF.flush()
            except:
                print 'EEE(runcmd): unable to open logpath: %s'%(logpath)
                return
        else:
            try:
                LF.writelines(lout)
                LF.flush()
            except:
                try:
                    LF=open(logpath,'a')
                    LF.writelines(lout)
                    LF.flush()
                except:
                    LF.writelines(lout)
                    LF.flush()
                    print 'EEE(runcmd): unable to write to logpath: %s'%(logpath)
                    return

    #
    # output to terminal
    #

    else:

        log=getCommandOutput2(command)

        print "CCC(log): %s\n"%command
        print log

    return

def runcmd2(command, ropt='', verb=1, lsopt='', prefix='', postfix='', ostdout=1,
            wait=False):

    oprefix=''
    if(prefix != ''): oprefix="(%s)"%(prefix)
    
    opostfix=''
    if(postfix != ''): opostfix="[%s]"%(postfix)

    if(ropt == 'norun'):  
        if(oprefix != ''):  oprefix="%s-NNNrun"%(oprefix)
        else:               oprefix='NNNrun'
        if(opostfix != ''): opostfix="%s-NNN"%(opostfix)
        else:               opostfix='NNN'
    curtime=dtg('cur_hms')
    occc="CCC-222"
    if(oprefix != ''): occc="%s(%s)"%(occc,oprefix)
    ocard="%s: %s %s %s"%(occc,command,curtime,opostfix)
    if(lsopt != 'q'): print ocard
    
    if(ropt == 'norun'): return(0)
    
    import subprocess
    try:
        if (wait):

            p = subprocess.Popen(
                [command], 
                stdout = subprocess.PIPE,
                shell = True)
            p.wait()
        else:
            if(ostdout == 1):
                p = subprocess.Popen(
                    [command], 
                    shell = True, 
                    stdin = None, stdout = PIPE, stderr = PIPE, close_fds = True)
            else:
                p = subprocess.Popen(
                    [command], 
                    shell = True, 
                    stdin = None, stdout = None, stderr = PIPE, close_fds = True)
                
        (result, error) = p.communicate()

        
    except subprocess.CalledProcessError as e:
        sys.stderr.write(
            "common::run_command() : [ERROR]: output = %s, error code = %s\n" 
            % (e.output, e.returncode))
        
        return(-999)


    rc=1
    if(ostdout == 1):
        slines=result.split('\n')

        if(verb): 
            print 'STDOut...'
            for line in slines:
                if(len(line) > 0):  print line

    elines=error.split('\n')
    if(verb and len(elines) > 1): print'STDErr...'
    for line in elines:
        if(verb): 
            if(len(line) > 0):  print line
        if(find(line,'error')): 
            rc=-999

    if(ostdout == 1): rc=(rc,slines)
    
    return (rc)



def PathCreateTime(path):
    import time
    timei=os.path.getctime(path)
    ltimei=time.localtime(timei)
    gtimei=time.gmtime(timei)
    dtimei=time.strftime("%Y%m%d%H:%M%S",ltimei)
    gdtimei=time.strftime("%Y%m%d%H:%M%S",gtimei)
    ldtg=dtimei[0:10]
    gdtg=gdtimei[0:10]
    return(dtimei,ldtg,gdtg)

def PathModifyTime(path):
    import time
    timei=os.path.getmtime(path)
    ltimei=time.localtime(timei)
    gtimei=time.gmtime(timei)
    dtimei=time.strftime("%Y%m%d%H:%M%S",ltimei)
    gdtimei=time.strftime("%Y%m%d%H:%M%S",gtimei)
    ldtg=dtimei[0:10]
    gdtg=gdtimei[0:10]
    return(dtimei,ldtg,gdtg)

def ChkDirOld(dir,diropt='verb'):

    if(dir == None):
        if(diropt != 'quiet'): print "dir      = None : "
        return(-2)

    if not(os.path.isdir(dir)) :
        if(diropt != 'quiet'): print "dir  (not there): ",dir
        if(diropt == 'mk' or diropt == 'mkdir'):
            try:
                os.system('mkdir -p %s'%(dir))
            except:
                print 'EEE unable to mkdir: ',dir,' in ChkDir, return -1 ...'
                return(-1)
            print 'dir     (MADE): ',dir
            return(2)
        else:
            return(0)
    else:
        if(diropt == 'verb'):
            print "dir      (there): ",dir
        return(1)

def ChkDir(ddir,diropt='verb'):

    if(ddir == None):
        if(diropt != 'quiet'): print "dir      = None : "
        return(-2)

    if not os.path.exists(ddir):
        
        if(diropt != 'quiet'): print "dir  (not there): ",ddir
        if(diropt == 'mk' or diropt == 'mkdir'):
    
            try:
                os.makedirs(ddir)
                print 'dir     (MADE): ',ddir
                return(2)
                
            except OSError as exception:
                if exception.errno != errno.EEXIST:
                    raise
                    #print 'EEE unable to mkdir: ',dir,' in ChkDir, return -1 ...'
                    #return(-1)
                else:
                    print "\nBE CAREFUL! Directory %s already exists." % path
    
        else:
            return(0)
        
    else:
        if(diropt == 'verb'):
            print "dir      (there): ",ddir
        return(1)

def ChangeDir(dir,diropt='verb'):

    try:
        os.chdir(dir)
        print 'cd---> ',dir
    except:
        print 'WWW unable to cd to: ',dir

def ChkPath(path,pathopt='noexit',verb=1):

    if not(os.path.exists(path)) :
        if(verb): print "EEE(ChkPath): path: %s NOT there... "%(path)
        if(pathopt == 'exit'):
            print "EEE(ChkPath): Sayoonara..."
            sys.exit()
        else:
            return(0)
    else:
        return(1)

def GetPathSiz(path,pathopt='exit',verb=1):

    if(ChkPath(path,pathopt='noexit') != 1):
        siz=None
    else:
        siz=os.path.getsize(path)

    return(siz)





def LsPids():

    #
    # get executing processes
    #

    processes=os.popen('ps -ef ').readlines()
    pids=[]
    for i in range(1,len(processes)):
        process=processes[i]
        tt=process.split()
        pname=''
        for n in range(7,len(tt)):
            pname="%s %s"%(pname,tt[n])
        piddate=tt[4]
        pname=pname.lstrip()
        pids.append( (int(tt[1]),int(tt[2]),pname,piddate) )

    return(pids)

def findPyPids(job):

    #
    # get executing processes
    #

    processes=os.popen('ps kstart_time -ef | grep -i %s'%(job)).readlines()
    pids=[]
    for i in range(1,len(processes)):
        process=processes[i]
        tt=process.split()
        pname=''
        for n in range(7,len(tt)):
            pname="%s %s"%(pname,tt[n])
        piddate=tt[4]
        pname=pname.lstrip()
        pids.append( (int(tt[1]),int(tt[2]),pname,piddate) )
        
    opids=[]
    for pid in pids:
        if(find(pid[2],'python')):
            opids.append(pid)
        

    return(opids)


def LsPids3():

    # get executing processes and three ids (on bsd/mac only?)
    #
    processes=os.popen('ps -ef ').readlines()
    pids=[]
    for i in range(1,len(processes)):
        process=processes[i]
        tt=process.split()
        pname=''
        for n in range(7,len(tt)):
            pname="%s %s"%(pname,tt[n])
        piddate=tt[4]
        pname=pname.lstrip()
        pids.append( (int(tt[0]),int(tt[1]),int(tt[2]),pname,piddate) )

    return(pids)


def PsTime2Hours(time):
    tt=time.split('-')

    if(len(tt) == 2):
        days=float(tt[0])
        ttime=tt[1].split(':')
    else:
        days=0.0
        ttime=time.split(':')

    hours=float(ttime[0])
    minutes=float(ttime[1])
    seconds=float(ttime[2])

    totaltime=days*24.0 + hours + (minutes+ (seconds/60.0) )/60.0

    return(totaltime)


def LsPidsuSer():

    #
    # get user executing processes
    #
    user=os.getenv('USER')
    processes=os.popen("ps -u %s -o \"pid,ppid,time,comm\""%(user)).readlines()
    pids=[]

    for n in range(1,len(processes)):
        p=processes[n]
        tt=p.split()
        pid=int(tt[0])
        ppid=int(tt[1])
        time=tt[2]
        command=tt[3]
        totaltime=PsTime2Hours(time)
        pids.append( (pid, ppid, totaltime, command) )

    return(pids)

def KillLongRunningProcess(timelimitkill,command2kill):

    upids=LsPidsuSer()
    for upid in upids:
        pid=upid[0]
        totaltime=upid[2]
        command=upid[3]
        if(totaltime >= timelimitkill and command == command2kill):
            print 'KKKKKKKKKKKilling: ',pid,totaltime,command
            os.kill(pid,signal.SIGKILL)






def KillPids(parentpid):

    verb=1

    #
    #  look for children (cpid) of the current parent process (ppid)
    #  put in list of spawned pids (spids)
    #
    #  initialize with input pid from calling parent

    curpid=parentpid

    spids=[]

    pids=LsPids()

    for pid in pids:
        cpid=pid[0]
        ppid=pid[1]
        pname=pid[2]

        if(ppid == curpid):
            spids.append(cpid)
            curpid=cpid
            if(verb): print cpid,ppid,curpid,pname

    #
    #  send kill signal to spids
    #

    nspids=len(spids)
    if(verb): print 'KKKKKKKKKKKK',nspids,spids,parentpid
    for spid in spids:
        try:
            print 'Killing pid: ',spid
            os.kill(spid,signal.SIGKILL)
        except:
            if(verb):
                print "unable to kill spawnd process: ",spid
            else:
                pass

    #
    #  now kill the main process if the one of the spawned 
    #

    try:
        os.kill(curpid,signal.SIGKILL)
    except:
        pass



def CleanReturns(istring):

    olist=[]

    o=istring.split('\n')

    for oo in o:
        if(len(oo) != 0):
            olist.append(oo+'\n')

    return(olist)

#
# calculate age of file using current and motime (h)
#
def PathDmtime(ipath):

    import time
    import os
    ctime=time.time()
    mtime=os.path.getmtime(ipath)
    dmtime=(ctime-float(mtime))/3600.0
    return(dmtime)


def doFTPsimple(server,localdir,remotedir,mask,
                opt='ftp.put',passive='off',doitout=0,quittime=None,
                verb=0):


    ftpopt=''
    if(quittime != None):
        ftpopt="-q %s"%(quittime)

    if(passive == 'off'):
        passopt=''
    elif(passive == 'on'):
        passopt='passive'
    else:
        passopt='passive'

    if(opt == 'ftp.ls' or opt == 'ftp.noload'):
        cmd="""
%s
cd %s
pwd
dir %s
quit
"""%(passopt,remotedir,mask)

    elif(opt == 'local.ls' or opt == 'ftp.noload'):
        cmd="""
%s
lcd %s
pwd
!ls -l %s
quit
"""%(passopt,localdir,mask)

    elif(opt == 'ftp.mkdir'):
        cmd="""
%s
mkdir %s
"""%(passopt,remotedir)

    elif(opt == 'ftp.rm'):
        cmd="""
%s
###verbose
prompt
cd %s
pwd
mdel %s
"""%(passopt,remotedir,mask)

    elif(opt == 'ftp.put' or opt == 'ftp'):

        cmd="""
#passive
verbose
cd %s
lcd %s
bin
prompt
mput %s
"""%(remotedir,localdir,mask)

    elif(opt == 'ftp.put.mk' or opt == 'ftp'):

        cmd="""
#passive
verbose
mkdir %s
cd %s
lcd %s
bin
prompt
mput %s
"""%(remotedir,remotedir,localdir,mask)

    elif(opt == 'ftp.get'):

        cmd="""
#passive
verbose
cd %s
lcd %s
bin
prompt
mget %s
"""%(remotedir,localdir,mask)

    else:
        print 'EEEEEEEEEEE in doFTPsimple invalid opt: ',opt
        sys.exit()


    doit=1
    if(opt == 'ftp.noload'): doit=0

    if(doit and doitout==0):
        ftppopen="ftp %s %s"%(ftpopt,server)
        if(verb): print 'ftppopen: ',ftppopen,' ftp cmd: ',cmd
        o=os.popen(ftppopen,"w")
        o.write(cmd)
        o.close()

    if(doitout):
        if(verb): print "ftp cmd:",cmd
        cmd="""ftp %s %s << EOF
%s
EOF
"""%(ftpopt,server,cmd)
        rc=os.popen(cmd).readlines()
        return(rc)

    #if(opt == 'ftp.ls'): sys.exit()

#
# 20031120 - process __doc__ string (str)
# to add pyfile
#

def usage(str,arg,curdtg=None,curtime=None,curphr=None):
    n=str.count('%s')
    pp=[]
    for n in range(0,n): pp.append(arg)
    pp=tuple(pp)
    print str%(pp)
    if(curdtg!=None and curtime!=None and curphr!=None):
        print "The Current DTG: %s  Phr: %s  Time: %s"%(curdtg,curphr,curtime)
    elif(curdtg!=None and curtime!=None):
        print "The Current DTG: %s  Time: %s"%(curdtg,curtime)


def find(mystr,pattern):
    rc=0
    if(mystr.find(pattern) != -1): rc=1
    return(rc)





def WriteCtl(ctl,ctlpath,verb=0):

    try:
        c=open(ctlpath,'w')
    except:
        print "EEE unable to open: %s"%(ctlpath)
        sys.exit()

    if(verb): print "CCCC creating .ctl: %s"%(ctlpath)
    c.writelines(ctl)
    c.close()
    return

def WriteList(llist,opath,verb=0,wmode='w'):

    try:
        c=open(opath,wmode)
    except:
        print "EEE unable to open: %s"%(opath)
        sys.exit()

    if(verb): print "CCCC creating list output file: %s"%(opath)
    for card in llist:
        card=card+'\n'
        c.writelines(card)
    c.close()
    return


def PrintCtl(ctl,ctlfile=None):

    if(ctlfile):
        otitle=ctlfile
    else:
        otitle="ctl file"
    print "PPPPPPPPP printing: %s ..................."%(otitle)

    for cc in ctl:
        print cc[:-1]

def PrintCurrency(title,ns=54,amount=-999):
    ntot=str(amount)
    nl=len(ntot)
    if(nl>9):
        n9=nl-9
        n6=nl-6
        n3=nl-3
        format="%%-%ds :: %4s,%3s,%3s,%3s"%(ns-4,ntot[0:n9],ntot[n9:n6],ntot[n6:n3],ntot[n3:])
    elif(nl>6):
        n6=nl-6
        n3=nl-3
        format="%%-%ds :: %8s,%3s,%3s"%(ns-4,ntot[0:n6],ntot[n6:n3],ntot[n3:])
    elif(nl>3):
        n3=nl-3
        format="%%-%ds :: %12s,%3s"%(ns-4,ntot[0:n3],ntot[n3:])
    else:
        format="%%-%ds :: %16s"%(ns-4,ntot)
    print format%(title)

    return

def PyVer():
    (pyverMajor,pyverMinor,pyverRel)=sys.version.split()[0].split('.')[0:3]
    fpyver=float("%s.%s%s"%(pyverMajor,pyverMinor,pyverRel))
    return(fpyver)

def Timer(str,stime):
    import time
    dtime=time.time()-stime
    print "ffffffff %-60s time: %5.2f s"%(str,dtime)


#
# function to glob than cp files 
#

def cpfiles(sdir,tdir,mask,ropt=''):

    files=glob.glob("%s/%s"%(sdir,mask))

    for file in files:
        cmd="cp %s %s/."%(file,tdir)
        runcmd(cmd,ropt)


def rmfiles(sdir,mask,ropt='norun'):

    files=glob.glob("%s/%s"%(sdir,mask))

    for file in files:
        cmd="rm %s"%(file)
        runcmd(cmd,ropt)

def h2hm(age):

    fh=int(age)*1.0
    im=int( (age-fh)*60.0+0.5 )
    if(im == 60):
        fh=fh+1.0
        im=0

    cage="%4.0f:%02d"%(fh,im)
    return(cage)


def min2minsec(min):

    fm=int(min)*1.0
    im=int( (min-fm)*60.0+0.5 )
    if(im == 60):
        fm=fm+1.0
        im=0

    cmin="%4.0f:%02d"%(fm,im)
    return(cmin)



# -- MMMMMMMMMM -- w2methods
#

def is0012Z(dtg):
    rc=0
    if(dtg[8:10] == '00' or dtg[8:10] == '12'): rc=1
    return(rc)


def is0618Z(dtg):
    rc=0
    if(dtg[8:10] == '06' or dtg[8:10] == '18'): rc=1
    return(rc)

def IsOffTime(dtg):
    dtghh=int(dtg[8:10])
    if(dtghh == 6 or dtghh == 18):
        return(1)
    else:
        return(0)


def SetLandFrac(lfres='1deg',ni=720,nj=361):

    lf=array.array('f')
    gdir=geogDatDir
    lfres='1deg'
    lfpath="%s/lf.%s.dat"%(gdir,lfres)
    LF=open(lfpath,'rb')
    nij=ni*nj
    lf.fromfile(LF,nij)
    return(lf)

#  return land frac given lat/lon; note defaults; same as used by .gs
#

def GetLandFrac(lf,tlat,tlon,ni=720,nj=361,blat=-90.0,blon=0.0,dlat=0.5,dlon=0.5):


    def w2ij(wi,wj,ni,nj,wi0,wj0,dwi,dwj):

        i=(wi-wi0)/dwi + 0.5
        j=(wj-wj0)/dwj + 0.5

        #
        # cyclic continuity in x
        #
        if(i <  0.0): i=float(ni)+i
        if(i >   ni): i=i-float(ni)

        i=int(i+1.0)
        j=int(j+1.0)

        return(i,j)


    (i,j)=w2ij(tlon,tlat,ni,nj,blon,blat,dlon,dlat)
    ij=(j-1)*ni+i-1
    return(lf[ij])




def add2000(y):
    if(len(y) == 1):
        yyyy=str(2000+int(y))
    elif(len(y) == 2):
        if(int(y) > 25):
            yyyy=str(1900+int(y))
        else:
            yyyy=str(2000+int(y))
            
    else:
        yyyy=y
    return(yyyy)

# -- MMMMMMMMMM -- tcVM methods
#
def getStmParams(stmid,convert9x=0):

    istmid=stmid
    if(convert9x): istmid=get9XstmidFromNewForm(stmid)

    tt=istmid.split('.')

    # -- case of genesis stmid tgNNNNN
    #
    if(len(tt) == 1):
        year=-9999
        snum='-99'
        b1id='X'
        b2id='XX'
        stm2id='NNXX.YYYY'
        stm1id='NNX.YYYY'
        if(istmid[0:2] == 'tg'):     snum='-1'
        
        return(snum,b1id,year,b2id,stm2id,stm1id)

    else:
        year=tt[1]

    if(len(tt[0]) == 4):
        snum=istmid[2:4]
        b2id=istmid[0:2]
        b1id=Basin2toBasin1[b2id.upper()]
        stm2id=istmid
    elif(len(tt[0]) == 7):
        snum=istmid[4:7]
        b2id=istmid[0:2].lower()
        b1id=Basin2toBasin1[b2id.upper()]
        stm2id=b2id+'cc'+snum+'.'+year
    elif(len(tt[0]) == 6):
        snum=istmid[2:5]
        b1id=istmid.split('.')[0][-1]
        b2id=Basin1toBasin2[b1id.upper()]
        stm2id=b2id+'cc'+snum+'.'+year
        stm2id=stm2id.lower()
    else:
        snum=istmid[0:2]
        b1id=istmid[2]
        b2id=Basin1toBasin2[b1id.upper()]
        stm2id=b2id+snum+'.'+year
        stm2id=stm2id.lower()

    stm1id=snum+b1id+'.'+year

    return(snum,b1id,year,b2id,stm2id,stm1id)



def Is9X(stmid):
    rc=0
    (snum,b1id,year,b2id,stm2id,stm1id)=getStmParams(stmid)
    if((snum[0].isalpha() and int(snum[1]) >=0 and int(snum[1]) <= 9) or
       (snum.isdigit() and (int(snum) >= 90 and int(snum) <= 99) )
       ):
        rc=1

    return(rc)

def IsNN(stmid):
    rc=0
    (snum,b1id,year,b2id,stm2id,stm1id)=getStmParams(stmid)
    if(
        (snum.isdigit() and (int(snum) >= 1 and int(snum) <= maxNNnum) )
        ):
        rc=1
    return(rc)


def IsTc(tcstate):
    #
    # if tc = 1
    # if stc = 2
    # if neither = 0
    # if undefined = -1
    #
    tcstate=tcstate.upper()

    if(
        tcstate == 'TD' or
        tcstate == 'TS' or
        tcstate == 'TY' or
        tcstate == 'HU' or
        tcstate == 'ST' or
        tcstate == 'TC' 
        #or tcstate == 'TW' no -- this is a Tropical Wave
        ):
        tc=1
    elif(
        tcstate == 'SS' or
        tcstate == 'SD'
        ):
        tc=2
    elif(
        tcstate == 'EX'
        ):
        tc=3
    elif(
        tcstate.lower() == 'xx' or
        tcstate == '  ' or
        len(tcstate) == 0
        ):
        tc=-1
    else:
        tc=0

    return(tc)

def IsTcWind(vmax):

    tc=0
    if(vmax >= TCvmin): tc=1
    return(tc)


def IsWarn(warnstate):
    #
    # if tc = 1
    # if stc = 2
    # if neither = 0
    #
    if(
        warnstate == 'WN'
        ):
        warn=1
    else:
        warn=0

    return(warn)



def pltHist(lista,listi,listo,
            stmopt,basin,year,
            tlist=None,
            ptitle2=None,
            filttype='season',
            donorm=1,
            docum=1,
            xmax=None,
            xmin=None,
            xint=None,
            ymax=None,
            ymin=0,
            yint=5,
            binint=None,
            dostacked=0,
            ptype='bar',
            var1='Dev',
            var2='NonDev',
            pngpath=None,
            doAllOnly=0,
            tag='',
            doshow=1):

    import matplotlib.pyplot as plt
    from numpy import array,arange

    xa=array(lista)
    xi=array(listi)
    xo=array(listo)

    ymaxi=xi.max()
    try:
        ymaxi=x.max()
    except:
        ymaxi=undef
        
    try:
        ymaxo=xo.max()
    except:
        ymaxo=undef

    rca=SimpleListStats(lista,hasflag=0)
    rci=SimpleListStats(listi,hasflag=0)
    rco=SimpleListStats(listo,hasflag=0)
    
    meana=rca[0]
    
    mediana=rca[-3]
    sigmaa=rca[2]

    meani=rci[0]
    mediani=rci[-3]
    sigmai=rci[2]

    meano=rco[0]
    mediano=rco[-3]
    sigmao=rco[2]

    if(donorm):
        ymax=0.75
        yint=0.25

    pyaxis=None
    if(docum):
        ymax=1.0
        yint=0.25
        pyaxis=[0,0.25,0.50,0.75,0.90,1.0]


    if(xmax == None): xmax=15
    if(xmin == None): xmin=0
    if(xint == None): xint=1

    if(binint == None):
        nbins=(xmax/xint)
        nbins=nbins*5
    else:
        nbins=(xmax-xmin)/binint

    xa=lista

    hrange=[xmin,xmax]

    fc1='green'
    fc2='red'
    ec1='black'
    ec2='black'


    if(donorm or docum):
        ylab='prob [0-1]'
    else:
        ylab='N'

    nbins=nint(nbins)

    if(doAllOnly):

        (n1, bins, patches) = plt.hist(xa,bins=nbins,histtype=ptype,range=hrange,\
                                       density=donorm,cumulative=docum,
                                       facecolor=fc1,edgecolor=ec1,
                                       alpha=0.75,rwidth=1.0)

        print '1111111111111' ,n1,bins
        
        n2=n1
        
        


    elif(dostacked):

        ptype='barstacked'
        ptype='bar'

        xplot=(xi,xo)
    
        (n1, bins, patches) = plt.hist(xplot,nbins,histtype=ptype,range=hrange,\
                                       normed=donorm,cumulative=docum,
                                       color=['green', 'red'],
                                       alpha=1.0,rwidth=1.0)

    else:

        fa1=0.75
        fa2=1.0
        fr1=1.0
        fr2=0.50
        if(docum):
            fr1=fr2=0.25
            fa1=fa2=0.50
        
        (n1, bins, patches) = plt.hist(xi,nbins,histtype=ptype,range=hrange,\
                                       density=donorm,cumulative=docum,
                                       facecolor=fc1,edgecolor=ec1,
                                       alpha=fa1,rwidth=fr1)

        print '1111111111111' ,n1,bins
        
        (n2, bins, patches) = plt.hist(xo,nbins,histtype=ptype,range=hrange,\
                                       density=donorm,cumulative=docum,
                                       facecolor=fc2,edgecolor=ec2,
                                       alpha=fa2,rwidth=fr2)
        print '22222222222222 ',n2,bins
        
        # -- make x&y for line plots if docum=1
        #
        if(docum):
            x=[]
            y90=[]
            for n in range(0,len(bins)-1):
                xb=(bins[n]+bins[n+1])*0.5
                x.append(xb)
                y90.append(0.9)
                
            y1=smooth(n1,window_len=7)
            y2=smooth(n2,window_len=7)
            rc=plt.plot(x,y1,color=fc1)
            rc=plt.plot(x,y2,color=fc2)
            rc=plt.plot(x,y90,color='black')


    ymax1=n1.max()
    ymax2=n2.max()

    if(ymax1 > ymax2):
        maxy=ymax1
    else:
        maxy=ymax2

    if(maxy >= 100):
        yint=20
    elif(maxy >= 50 and maxy < 100):
        yint=10
        
    if(ymax == None):
        ymax=int((float(maxy)/float(yint))+0.5 + 1)*float(yint)
    
        
    xs=[]
    for i in range(0,len(bins)-1):
        xs.append( (bins[i]+bins[i+1])*0.5 )

    def zerolt0(ys):
        oys=[]
        for y in ys:
            if(y < 0.0):
                oys.append(0.0)
            else:
                oys.append(y)
        return(oys)


    xlab='Nada'
    if(tlist == 'stmlife'):
        xlab='Storm Life [d]'

    elif(tlist == '9xlife'):
        xlab='pre-genesis 9X Life [d]'

    elif(tlist == 'latb'):
        xlab='Begin Latitude [deg]'

    elif(tlist == 'time2gen'):
        xlab='Time to Genesis [d]'

    plt.xlabel(xlab)
    plt.ylabel(ylab)

    if(ptitle2 == None):
        ptitle2="Stmopt: %s"%(stmopt)

    if(tlist == 'time2gen'):

        ptitle="N: %d  Mn: %3.1f $\sigma$: %3.1f  Median: %3.1f\n%s"%(
            len(lista),meana,sigmaa,mediana,
            stmopt)

    elif(find(filttype,'dev')):

        ni=len(listi)
        no=len(listo)
        devratio=(float(ni)/float(no))*100.0
        ptitle="%s(G) N %d Mn %3.1f $\sigma$: %3.1f %s(R) N %d Mn: %3.1f $\sigma$: %3.1f %%: %3.0f\n%s"%(
            var1,ni,meani,sigmai,
            var2,no,meano,sigmao,
            devratio,
            ptitle2)

    elif(find(filttype,'seas')):

        ptitle="%s(G)  N: %d Mn: %3.1f $\sigma$: %3.1f %s(R)  N: %d Mn: %3.1f $\sigma$: %3.1f\n%s"%(
            var1,len(listi),meani,sigmai,
            var2,len(listo),meano,sigmao,
            stmopt)


        
    #ptitle="$\sigma=$"
    plt.title(r"%s"%(ptitle),fontsize=12)
    

   
    plt.xlim(xmin,xmax)
    xaxis=arange(xmin,xmax+1,xint)
    plt.xticks(xaxis)

    if(ymax != None):
        plt.ylim(ymin,ymax)
        yaxis=arange(ymin,ymax+0.001,yint)
        if(pyaxis != None):
            plt.yticks(pyaxis)

    plt.grid(True)

    if(pngpath == None):
        pngpath="/tmp/9x.%s.%s.png"%(basin,year)

    print 'ppppppppppppppppppppppp ',pngpath
    plt.savefig(pngpath)
    
    doCp2Aori=0
    if(doCp2Aori):
        cmd="cp %s ~/pCloudDrive/AORI/TALKS/plt/"%(pngpath)
        runcmd(cmd)

    if(doshow): plt.show()

def SimpleListStats(dlist,verb=0,undef=-77,undef2=1e20,hasflag=1,flagval=None):
    """
    added undef2 which is semi-universal undef -- used in vdVM in processing VdeckS()
"""
    mean=0.0
    amean=0.0
    sigma=0.0
    mean2=0.0
    max=-1e20
    min=1e20
    
    odlist=[]
    n=0
    for ll in dlist:

        if(hasflag):
            flag=ll[0][0]
            val=ll[1]
            # -- if not a float set to undef
            if(type(val) is StringType): val=undef
        else:
            flag=1
            val=float(ll)
            
        # -- flag test
        #
        flagtest=(flag >= 1)
        if(flagval != None): flagtest=(flag == flagval)
        
        if(val == float(undef) or val == undef2): flagtest=0
                
        if(flagtest):
            odlist.append(val)
            mean=mean+val
            mean2=mean2+val*val
            amean=amean+fabs(val)
            if(val > max): max=val
            if(val < min): min=val
            if(verb):
                print 'stats n: ',n,'flag: ',flag,' val: ',val,' flagtest: ',flagtest
            n=n+1

    if(n > 0):
        mean=mean/float(n)
        amean=amean/float(n)
        var=mean2/float(n) - mean*mean
        if(fabs(var) > epsilonm5):
            sigma=sqrt(var)
        else:
            sigma=0.0
    else:
        mean=None
        amean=None
        sigma=None
        mean=amean=sigma=max=min=undef

    odlist.sort()
    if(n <= 1):
        ptl25=median=ptl75=ptl90=undef
    else:
        width=float(n-1)
        ptl25=width*0.25 ; n250=int(ptl25); n251=n250+1 ; d25=ptl25-n250
        ptl50=width*0.50 ; n500=int(ptl50); n501=n500+1 ; d50=ptl50-n500
        ptl75=width*0.75 ; n750=int(ptl75); n751=n750+1 ; d75=ptl75-n750
        ptl90=width*0.90 ; n900=int(ptl90); n901=n900+1 ; d90=ptl90-n900

        ptl25 =odlist[n250]*(1.0-d25) + odlist[n251]*d25
        median=odlist[n500]*(1.0-d50) + odlist[n501]*d50
        ptl75 =odlist[n750]*(1.0-d75) + odlist[n751]*d75
        ptl90 =odlist[n900]*(1.0-d90) + odlist[n901]*d90

        if(verb):
            print '50: ',n500,n501,d50,odlist[n500],odlist[n501],median
            print '25: ',n250,n251,d25,odlist[n250],odlist[n251],ptl25
            print '75: ',n750,n751,d75,odlist[n750],odlist[n751],ptl75
            print '90: ',n900,n901,d90,odlist[n900],odlist[n901],ptl90
    
    
    rc=(mean,amean,sigma,max,min,n,ptl25,median,ptl75,ptl90)
    return(rc)


def setFilter(filtopt,stmopt):
    
    tt=filtopt.split('.')
    if(len(tt) != 3):
        print """EEE improper form of filtopt
FF.TT.NN
FF: all|season|dev|CC|CC-bt|CC-9x
TT: latb|latmn|stmlife|9xlife
NN: 0 - counts; 1 - donorm=1; 2 donorm=1,docum=1
"""
        sys.exit()


    filtBySeason=0
    filtByDev=0
    filtByCC=0

    tlist='stmlife'

    ymax=None
    yint=None
    xmax=10
    xmin=0
    xint=1

    ftype=tt[0]
    tlist=tt[1]
    dtype=int(tt[2])
    binint=0.25

    ptitle2="Stmopt: %s"%(stmopt)
    
    if(find(ftype,'sea')): filtBySeason=1
    if(find(ftype,'dev')): filtByDev=1

    if(tlist == '9xlife'):
        yint=5
        xmax=10
        xmin=0
        xint=1
        binint=0.25
        binint=0.33
        
    elif(tlist == 'stmlife' or tlist == 'time2gen'):
        yint=5
        xmax=10
        xmin=0
        xint=1
        binint=0.5
        if(tlist == 'time2gen'):
            ptitle2="Time to Genesis Stmopt: %s"%(stmopt)
        
    
    elif(tlist == 'latb'):
        yint=5
        xmax=45
        xmin=0
        xint=5
        binint=5

    donorm=0
    docum=0
    if(dtype == 1):donorm=1
    if(dtype == 2):donorm=1; docum=2

    return(filtBySeason,filtByDev,filtByCC,tlist,donorm,docum,
           ymax,yint,xmax,xmin,xint,binint,ptitle2)


def smooth(x,window_len=5,
           window='hanning',
           #window='flat',
           adjustWindowLen=1):

    import numpy

    """smooth the data using a window with requested size.
    
    This method is based on the convolution of a scaled window with the signal.
    The signal is prepared by introducing reflected copies of the signal 
    (with the window size) in both ends so that transient parts are minimized
    in the begining and end part of the output signal.
    
    input:
        x: the input signal 
        window_len: the dimension of the smoothing window
        window: the type of window from 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'
            flat window will produce a moving average smoothing.

    output:
        the smoothed signal
        
    example:

    t=linspace(-2,2,0.1)
    x=sin(t)+randn(len(t))*0.1
    y=smooth(x)
    
    see also: 
    
    numpy.hanning, numpy.hamming, numpy.bartlett, numpy.blackman, numpy.convolve
    scipy.signal.lfilter
 
    TODO: the window parameter could be the window itself if an array instead of a string   
    """

    if(x.size < window_len and adjustWindowLen): window_len=x.size-1
    if x.ndim != 1:
        raise ValueError, "smooth only accepts 1 dimension arrays."

    if x.size < window_len:
        raise ValueError, "Input vector needs to be bigger than window size."


    if window_len<3:
        return x


    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError, "Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'"


    s=numpy.r_[2*x[0]-x[window_len:1:-1],x,2*x[-1]-x[-1:-window_len:-1]]
    #print(len(s))
    if window == 'flat': #moving average
        w=numpy.ones(window_len,'d')
    else:
        w=eval('numpy.'+window+'(window_len)')

    y=numpy.convolve(w/w.sum(),s,mode='same')
    return y[window_len-1:-window_len+1]

def uv2dirspd(u,v):
    sdir=atan2(u,v)*rad2deg
    if(sdir < 0.0): sdir=360.0+sdir
    sspd=sqrt(u*u+v*v)
    return(sdir,sspd)



def rumhdsp(rlat0,rlon0,rlat1,rlon1,dt,units='english',verb=0):

    verb=0

    if(verb):
        print "***** ",rlat0,rlon0,rlat1,rlon1,dt,units,opt

    if(units == 'metric'):
        distfac=111.19
        spdfac=0.2777
    else:
        distfac=60.0
        spdfac=1.0


    #
    # assumes deg W
    #
    rnumtor=(rlon0-rlon1)*deg2rad

    #
    #--- assume DEG E!!!!!!!!!!!!!!!!!!!!!!!!
    #

    rnumtor=(rlon1-rlon0)*deg2rad
    d1=(45.0+0.5*rlat1)*deg2rad
    d2=(45.0+0.5*rlat0)*deg2rad

    td1=tan(d1)
    td2=tan(d2)
    rlogtd1=log(td1)
    rlogtd2=log(td2)
    rdenom=rlogtd1-rlogtd2
    rmag=rnumtor*rnumtor + rdenom*rdenom

    course=0.0
    if(rmag != 0.0):
        course=atan2(rnumtor,rdenom)*rad2deg

    if(course <= 0.0):  
        course=360.0+course

    #
    #...     now find distance
    #

    icourse=int(course+0.1)
    if(icourse ==  90.0 or icourse == 270.0 ):
        distance=distfac*abs(rlon0-rlon1)*cos(rlat0*deg2rad)
    else:
        distance=distfac*abs(rlat0-rlat1)/abs(cos(course*deg2rad))

    #
    #...     now get speed
    #
    speed=distance/dt

    #
    #...      convert to u and v motion
    #

    spdmtn=speed*spdfac
    ispeed=int(spdmtn*100+0.5)/100
    angle=(90.0-course)*deg2rad

    umotion=spdmtn*cos(angle)
    vmotion=spdmtn*sin(angle)
    iumotion=int(umotion*100+0.5)/100
    ivmotion=int(vmotion*100+0.5)/100
    rumotion=float(iumotion)
    rvmotion=float(ivmotion)
    rcourse=float(course)
    rspeed=float(spdmtn)
    if(verb):
        print "%5.2f %4.0f %5.2f %5.2f %5.2f %5.2f\n"%\
              (distance,icourse,spdmtn,angle,umotion,vmotion)

    return(rcourse,rspeed,umotion,vmotion)



# -- MMMMMMMMMM -- sBT methods
#

def getShemYear(dtg):
    """
     convert year in stm dtg to basinyear
    """

    yyyy=int(dtg[0:4])
    mm=int(dtg[4:6])

    if(mm >= 7): yyyy=yyyy+1
    cyyyy=str(yyyy)
    return(cyyyy)

def getStmopts(stmopt):
    
    ss=stmopt.split('.')
    bb=ss[0].split(',')

    stmopts=[]
    
    if(ss[0] == 'all'):
        for b1 in ['w','e','c','l','i','h']:
            stm="%s.%s"%(b1,ss[1])
            stmopts.append(stm)

    elif(len(bb) > 1):
        for b1 in bb:
            stm="%s.%s"%(b1,ss[1])
            stmopts.append(stm)
    else:
        stmopts.append(stmopt)
        
    return(stmopts)
            


def getPyp(pyppath):

    ppath=pyppath

    if(os.path.exists(ppath)):
        PS=open(ppath)
        pyp=pickle.load(PS)
        PS.close()
        return(pyp)
    else:
        return(None)


def putPyp(pyp,pyppath):

    ppath=pyppath
    pyppckle=pyp

    try:
        PS=open(ppath,'w')
        pickle.dump(pyppckle,PS)
        PS.close()
    except:
        print 'EEEEE unable to pickle.dump: ',ppath
        sys.exit()


def printTrk(stmid,dtg,rlat,rlon,vmax,pmin,
             dir=-999,spd=-999,dirtype='X',
             tdo='---',
             tccode='XX',
             wncode='XX',
             ntrk=0,
             ndtgs=0,
             r34m=None,
             r50m=None,
             alf=None,
             sname='---------',
             gentrk=0,
             doprint=1):

    (clat,clon)=Rlatlon2Clatlon(rlat,rlon,dodec=1)

    if(vmax == None or vmax == undef or vmax == 0):  cvmax='---'
    else:              cvmax="%03d"%(vmax)
    if(pmin == None):  cpmin='----'
    else:              cpmin="%4d"%(pmin)

    if(r34m == None or r34m == undef):
        cr34m='---'
    else:
        cr34m="%3.0f"%(float(r34m))

    if(r50m == None or r50m == undef):
        cr50m='---'
    else:
        cr50m="%3.0f"%(r50m)

    # -- if first posit set to 360.0 and -0 spd
    #
    if(dir == -999.): dir=360.0
    if(spd == -999.): spd=-0.0

    cdir="%5.1f"%(dir)
    cspd="%4.1f"%(spd)

    if(alf == None or alf == undef):
        clf='----'
    else:
        clf="%4.2f"%(alf)

    if(gentrk):
        card="%s* %12s "%(dtg,stmid.upper())
    else:
        card="%s  %12s "%(dtg,stmid.upper())

    if(tdo == 'NaN' or tdo == ''): tdo='---'
    card=card+"%s %s %s  %s  %s %s"%(cvmax,cpmin,clat,clon,cr34m,cr50m)
    card=card+"  %s %s %s  %s %s  %s"%(cdir,cspd,dirtype,tccode,wncode,tdo)
    card=card+" %3d/%-3d lf: %s %-9s"%(ntrk,ndtgs,clf,sname[0:9])
    if(gentrk): card=card+" <**Genesis"
    if(doprint): print card
    return(card)

def printMd3Trk(md3trk,dtg,doprint=0):

    (rlat,rlon,vmax,pmin,tdir,tspd,r34m,r50m,tccode,wncode,
     roci,poci,alf,depth,eyedia,tdo,ostmid,ostmname,r34,r50)=md3trk
        
    card=printTrk(ostmid,dtg,rlat,rlon,vmax,pmin,
                   tdir,tspd,tdo=tdo,
                   tccode=tccode,wncode=wncode,
                   r34m=r34m,r50m=r50m,alf=alf,
                   sname=ostmname,doprint=0)
    
    if(doprint):
        print card
        
    return(card)


def mergeMd3Cvs(mpath,mpathBT,opath,verb=0):

    mcards={}
    mcardsbt={}
    btcards=[]

    ocards=[]
    
    cards=open(mpath).readlines()
    if(mpathBT != None):
        btcards=open(mpathBT).readlines()
        
    for card in cards:
        tt=card.split(",")
        dtg=tt[0]
        stmid=tt[1]
        mcards[dtg]=card
        
    for btcard in btcards:
        tt=btcard.split(',')
        dtg=tt[0]
        stmid=tt[1]
        mcards[dtg]=btcard
        mcardsbt[dtg]=btcard
        
        
    dtgs=mcards.keys()
    dtgs.sort()

    for dtg in dtgs:
        mcard=mcards[dtg]
        ocards.append(mcard)
        try:
            mcardb=mcardsbt[dtg]
        except:
            None
            mcardb='nnnooobbbttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt'
            
        if(verb):
            print 'dtg: ',dtg,'  M:',mcard[0:50],'  B:',mcardb[0:50]
        
    return(ocards)
        
    
def setCvsYearOptPaths(sbtSrcDir,oyearOpt,headAll,headSum,doMergeOnly=1,doWBTonly=0):
    
    allCvsPath="%s/all-md3-%s.csv"%(sbtSrcDir,oyearOpt)
    allCvsPathBT="%s/all-md3-%s-BT.csv"%(sbtSrcDir,oyearOpt)
    allCvsPathMRG="%s/all-md3-%s-MRG.csv"%(sbtSrcDir,oyearOpt)

    sumCvsPath="%s/sum-md3-%s.csv"%(sbtSrcDir,oyearOpt)
    sumCvsPathBT="%s/sum-md3-%s-BT.csv"%(sbtSrcDir,oyearOpt)
    sumCvsPathMRG="%s/sum-md3-%s-MRG.csv"%(sbtSrcDir,oyearOpt)
    

    if(doMergeOnly):
        
        if(MF.ChkPath(allCvsPathMRG)):
            cmd='rm  %s'%(allCvsPathMRG)
            runcmd(cmd)
        
        if(MF.ChkPath(sumCvsPathMRG)):
            cmd='rm  %s'%(sumCvsPathMRG)
            runcmd(cmd)
        
        cmd="cat %s > %s"%(headAll,allCvsPathMRG)
        runcmd(cmd)
        
        cmd="cat %s > %s"%(headSum,sumCvsPathMRG)
        runcmd(cmd)

        return(allCvsPathMRG,sumCvsPathMRG)
        
    else:
        
        if(MF.ChkPath(allCvsPath)):
            cmd='rm  %s'%(allCvsPath)
            runcmd(cmd)
    
        if(MF.ChkPath(allCvsPathBT)):
            cmd='rm  %s'%(allCvsPathBT)
            runcmd(cmd)
        
        if(MF.ChkPath(sumCvsPath)):
            cmd='rm  %s'%(sumCvsPath)
            runcmd(cmd)
        
        if(MF.ChkPath(sumCvsPathBT)):
            cmd='rm %s'%(sumCvsPathBT)
            runcmd(cmd)
            
        # -- headers
        #
        cmd="cat %s > %s"%(headAll,allCvsPath)
        runcmd(cmd)

        if(not(doWBTonly)):
            cmd="cat %s > %s"%(headAll,allCvsPathBT)
            runcmd(cmd)
        
        cmd="cat %s > %s"%(headSum,sumCvsPath)
        runcmd(cmd)
        
        cmd="cat %s > %s"%(headSum,sumCvsPathBT)
        runcmd(cmd)
            
        return(allCvsPath,allCvsPathBT,sumCvsPath,sumCvsPathBT)

def setCvsSbtYearOptPaths(sbtSrcDir,oyearOpt,version,headAll,dorm=0):
    
    allCvsPath="%s/sbt-%s-%s-MRG.csv"%(sbtSrcDir,version,oyearOpt)
    sumCvsPath="%s/sum-md3-%s-MRG.csv"%(sbtSrcDir,oyearOpt)

    if(MF.ChkPath(allCvsPath) and dorm):
        cmd='rm  %s'%(allCvsPath)
        runcmd(cmd)
    
    cmd="cat %s > %s"%(headAll,allCvsPath)
    runcmd(cmd)
    
    return(allCvsPath,sumCvsPath)


def getBasin4b1id(b1id):
    ib1id=b1id.lower()
    if(ib1id == 'l'):
        basin='lant'
    elif(ib1id == 'w'):
        basin='wpac'
    elif(ib1id == 'e' or ib1id == 'c'):
        basin='epac'
    elif(ib1id == 'i' or ib1id == 'b' or ib1id == 'a'):
        basin='io'
    elif(ib1id == 'h' or ib1id == 's' or ib1id == 'p'):
        basin='shem'
    else:
        print 'EEE in getBasin4b1id b1id: ',b1id
        sys.exit()
        
        
    return(basin)
        
def mkFloat(var,convU2Uvar=0):
    ovar=undef
    if(var != 'NaN' and var != ''): 
        ovar=float(var)
    if(convU2Uvar and ovar == undef):
        ovar=undefVar
        
    return(ovar)

def mkFloatU(var,convU2Uvar=1):
    ovar=undef
    if(var != 'NaN' and var != ''): 
        ovar=float(var)
    if(convU2Uvar and ovar == undef):
        ovar=undefVar
        
    return(ovar)


def setMd3track(m3trk,stmid,verb=0):
    
    def interpM3trk(m1,m2,f1,f2):
        
        def dointerp(v1,v2,f1,f2):
            if(v1 != undef and v1 != undef): vi=v1*f1+v2*f2
            if(v1 != undef and v2 == undef): vi=v1
            if(v2 != undef and v1 == undef): vi=v2
            if(v1 == undef and v2 == undef): vi=undef
            return(vi)
            
            
        (rlat1,rlon1,vmax1,pmin1,tdir1,tspd1,r34m1,r50m1,tcstate1,warn1,roci1,poci1,alf1,depth1,eyedia1,tdo1,ostmid1,ostmname1,r341,r501)=m1
        (rlat2,rlon2,vmax2,pmin2,tdir2,tspd2,r34m2,r50m2,tcstate2,warn2,roci2,poci2,alf2,depth2,eyedia2,tdo2,ostmid2,ostmname2,r342,r502)=m2
        
        rlati=rlat1*f1+rlat2*f2
        rloni=rlon1*f1+rlon2*f2
        vmaxi=dointerp(vmax1,vmax2,f1,f2)
        pmini=dointerp(pmin1,pmin2,f1,f2)
        tdiri=dointerp(tdir1,tdir2,f1,f2)
        tspdi=dointerp(tspd1,tspd2,f1,f2)
        r34mi=dointerp(r34m1,r34m2,f1,f2)
        r50mi=dointerp(r50m1,r50m2,f1,f2)
        tcstatei=tcstate1
        warni=warn1
        rocii=dointerp(roci1,roci2,f1,f2)
        pocii=dointerp(poci1,poci2,f1,f2)
        alfi=dointerp(alf1,alf2,f1,f2)
        depthi=depth1
        eyediai=eyedia1
        tdoi=tdo1
        ostmidi=ostmid1
        ostmnamei=ostmname1
        r34i=r341
        r50i=r501
        
        mi=(rlati,rloni,vmaxi,pmini,tdiri,tspdi,r34mi,r50mi,tcstatei,warni,rocii,pocii,alfi,depthi,eyediai,tdoi,ostmidi,ostmnamei,r34i,r50i)
        return(mi)
        
    # -- check if we need to interpolate for missing dtgs
    #
    idtgs=m3trk.keys()
    idtgs.sort()
    fdtgs=dtgrange(idtgs[0],idtgs[-1],6)
    li=len(idtgs)
    lf=len(fdtgs)
    
    # -- we do need to interpolate... can handle 12 and 18 gaps
    
    if(li != lf):
    
        mdtgs=[]
        if(verb): print 'li lf',stmid,li,lf
        for n in range(0,lf):
            fdtg=fdtgs[n]
            try:
                m3i=m3trk[fdtg]
            except:
                
                dtg1=fdtgs[n-1]
                indx=idtgs.index(dtg1)
                dtg2=idtgs[indx+1]
                
                if(verb): print 'have to interpolate...',fdtg,'dtg1 2',dtg1,dtg2
                # -- do the interpolation here...
                #
                dtgib=dtginc(dtg1,+6)
                dtgie=dtginc(dtg2,-6)
                dtgis=dtgrange(dtgib, dtgie)
                iden=dtgdiff(dtg1, dtg2)
                
                if(iden > 36.0):
                    print'EEE big iterp interval for stmid',stmid,dtg1,dtg2,iden
                    sys.exit()
                
                m1=m3trk[dtg1]
                m2=m3trk[dtg2]
    
                for dtgi in dtgis:
    
                    inum1=dtgdiff(dtg1, dtgi)
                    inum2=dtgdiff(dtgi,dtg2)
    
                    f1=inum2/iden
                    f2=inum1/iden
                
                    if(verb): print 'interp for dtg',dtg1,dtgi,dtg2,inum1,inum2,f1,f2
                    m3trk[dtgi]=interpM3trk(m1,m2,f1,f2)
                    mdtgs.append(dtgi)
                    n=n+1
                n=n+1
                
    return(m3trk)
    
    
    

def parseMd3Card(mm,dobt=0,verb=0):
    
    
    #n:  0 2019122118
    #n:  1 30w.2019
    #n:  2 PHANFONE
    #n:  3 TY
    #n:  4 NN
    #n:  5 6.4
    #n:  6 139.9
    #n:  7 30
    #n:  8 1002
    #n:  9 293
    #n: 10 14
    #n: 11 293
    #n: 12 14
    #n: 13 NaN
    #n: 14 NaN
    #n: 15 NaN
    #n: 16 NaN
    #n: 17 NaN
    #n: 18 NaN
    #n: 19 NaN
    #n: 20 NaN
    #n: 21 NaN
    #n: 22 NaN
    #n: 23 TD
    #n: 24 WN
    #n: 25 B  dirtype
    #n: 26 B  posttype
    #n: 27 140
    #n: 28 1006
    #n: 29 NaN
    #n: 30 S
    #n: 31 30
    #n: 32 RCB
 
    if(verb == 2):
        for n in range(0,len(mm)):
            print 'n: %2d'%(n),mm[n]
        sys.exit()
        
    dtg=mm[0]
    ostmid=mm[1]

    ostmname=mm[2].strip()
    if(Is9X(ostmid)):
        ostmname="9X-%s"%(ostmid.split('.')[0].upper())
    tcstate=mm[3].strip()
    stmDev=mm[4].strip()
    
    # -- handle NN here vice with dobt and continue if 9X
    #
    if(dobt and ((IsNN(ostmid) and stmDev != 'NN') or (Is9X(ostmid)) ) ):
        return(None)
        
    n=5
    rlat=mm[n] ; n=n+1
    rlon=mm[n] ; n=n+1
    vmax=mm[n] ; n=n+1
    pmin=mm[n] ; n=n+1
    cdir=mm[n] ; n=n+1
    cspd=mm[n] ; n=n+1
    tdir=mm[n] ; n=n+1
    tspd=mm[n] ; n=n+1
    
    # -- get full r34
    #
    r34m=mm[n] ; n=n+1
    r34ne=mm[n] ; n=n+1
    r34se=mm[n] ; n=n+1
    r34sw=mm[n] ; n=n+1
    r34nw=mm[n] ; n=n+1

    # -- get full r50
    #
    r50m=mm[n]  ; n=n+1
    r50ne=mm[n] ; n=n+1
    r50se=mm[n] ; n=n+1
    r50sw=mm[n] ; n=n+1
    r50nw=mm[n] ; n=n+1
    
    tcstate=mm[n] ; n=n+1
    warn=mm[n] ; n=n+1
    dirtype=mm[n] ; n=n+1
    posttype=mm[n] ; n=n+1
    
    roci=mm[n] ; n=n+1
    poci=mm[n] ; n=n+1
    
    alf=mm[n] ; n=n+1
    depth=mm[n] ; n=n+1
    eyedia=mm[n] ; n=n+1
    tdo=mm[n].strip() 
    
    if(dirtype == ''):
        dirtype='NaN'
    if(posttype == ''):
        posttype='NaN'
        
    rlat=float(rlat)
    rlon=float(rlon)
    tdir=mkFloat(tdir)
    tspd=mkFloat(tspd)
    vmax=mkFloat(vmax)
    pmin=mkFloat(pmin)

    r34m=mkFloat(r34m)
    r34ne=mkFloat(r34ne)
    r34se=mkFloat(r34se)
    r34sw=mkFloat(r34sw)
    r34nw=mkFloat(r34nw)
    
    r50m=mkFloat(r50m)
    r50ne=mkFloat(r50ne)
    r50se=mkFloat(r50se)
    r50sw=mkFloat(r50sw)
    r50nw=mkFloat(r50nw)
    
    
    if(alf == 'NaN' or alf == ''): alf=0.0
    else:                          alf=float(alf)

    roci=mkFloat(roci)
    poci=mkFloat(poci)
    
    #if(warn == 'NaN' or warn == ''): warn='--'
    #if(depth == 'NaN' or depth == ''): depth='-'
    
    eyedia=float(eyedia)
    r34=(r34ne,r34se,r34sw,r34nw)
    r50=(r50ne,r50se,r34sw,r50nw)

    if(verb):
        print 'rrrrr',dtg,rlat,rlon,vmax,pmin,tdir,tspd,r34m,r50m,tcstate,warn,roci,poci,ostmid
    rc=(dtg,rlat,rlon,vmax,pmin,tdir,tspd,r34m,r50m,tcstate,warn,roci,poci,alf,depth,eyedia,tdo,ostmid,ostmname,r34,r50)
    return(rc)


def makeMd3Card(dtg,m3t,m3i,m2t,verb=0):

    def getr34(r34):
        or34='   '
        if(r34 != undef):
            or34="%3.0f"%(r34)
        return(or34)
            
    def getr50(r50):
        or50='   '
        if(r50 != undef):
            or50="%3.0f"%(r50)
        return(or50)
    
    
    #n:  0 2019122118
    #n:  1 30w.2019
    #n:  2 PHANFONE
    #n:  3 TY
    #n:  4 NN
    #n:  5 6.4
    #n:  6 139.9
    #n:  7 30
    #n:  8 1002
    #n:  9 293
    #n: 10 14
    #n: 11 293
    #n: 12 14
    #n: 13 NaN
    #n: 14 NaN
    #n: 15 NaN
    #n: 16 NaN
    #n: 17 NaN
    #n: 18 NaN
    #n: 19 NaN
    #n: 20 NaN
    #n: 21 NaN
    #n: 22 NaN
    #n: 23 TD
    #n: 24 WN
    #n: 25 B  dirtype
    #n: 26 B  posttype
    #n: 27 140
    #n: 28 1006
    #n: 29 NaN
    #n: 30 S
    #n: 31 30
    #n: 32 RCB
    
        
    ostmid=m3i[0]
    ostmname=m3i[1].strip()
    if(Is9X(ostmid)):
        ostmname="9X-%s"%(ostmid.split('.')[0].upper())
    tctype=m3i[2].strip()
    stmDev=m3i[3].strip()
    
    if(verb):
        print 'mmm',dtg,m3t[0:9],m3i,len(m3t),len(m3i),m2t.sname,m2t.stmid
        print '000',dtg,ostmid,ostmname,tctype,stmDev
    #(rlat,rlon,vmax,pmin,tdir,tspd,r34m,r50m,tcstate,warn
    
    n=0
    nb=n
    rlat=m3t[n] ; n=n+1
    rlon=m3t[n] ; n=n+1
    vmax=m3t[n] ; n=n+1
    pmin=m3t[n] ; n=n+1
    trkdir=m3t[n] ; n=n+1
    trkspd=m3t[n] ; n=n+1
    r34m=m3t[n] ; n=n+1
    r50m=m3t[n] ; n=n+1
    tccode=m3t[n] ; n=n+1
    wncode=m3t[n] ; n=n+1
    
    if(verb):
        print 'mmm',nb,n,m3t[nb:n]
        print '111',rlat,rlon,vmax,pmin,trkdir,trkspd,r34m,r50m,tccode,wncode
        
    nb=n
    #(roci,poci,alf,depth,eyedia,tdo,ostmid,ostmname,r34,r50)
    roci=m3t[n] ; n=n+1
    poci=m3t[n] ; n=n+1
    alf=m3t[n] ; n=n+1
    depth=m3t[n] ; n=n+1
    eyedia=m3t[n] ; n=n+1
    tdo=m3t[n].strip() ; n=n+1
    
    if(verb):
        print 'mmm',nb,n,m3t[nb:n]
        print '222',roci,poci,alf,depth,eyedia,tdo

    nb=n
    ne=len(m3t)
    ostmidm3=m3t[n] ; n=n+1
    ostmname=m3t[n] ; n=n+1
    r34=m3t[n] ; n=n+1
    r50=m3t[n] ; n=n+1
    
    if(verb):
        print 'mmm',nb,ne,m3t[nb:ne]
        print '333',ostmidm3,ostmname,r34,r50

    # -- this done below
    3
    #r34ne=r34[0]
    #r34se=r34[1]
    #r34sw=r34[2]
    #r34nw=r34[3]

    ## -- get full r50
    ##
    #r50ne=r50[0]
    #r50se=r50[1]
    #r50sw=r50[2]
    #r50nw=r50[3]
    #print '444',r34ne,r34se,r34sw,r34nw,'50',r50ne,r50se,r50sw,r50nw
        
    # -- 2222222222222222222222222222 - from m2.trk object made in class MD3trk
    #
    cdir=m2t.dir         #275.449145529
    dirtype=m2t.dirtype   #B
    ndtgs=m2t.ndtgs       #40
    ntrk=m2t.ntrk         #19
    posttype=m2t.postype  #B
    cspd=m2t.spd          #15.7957548819
    stmid=m2t.stmid.lower()      #30W.2019
    stmidm2=stmid
    sname=m2t.sname
    undef=m2t.undef      #-999
    rmax=m2t.rmax        #15
    
    # -- use m3 sname
    #
    sname=ostmname
    if(sname != None and sname != undef and len(sname) > 0):
        osname="%-15s"%(sname)
    else:
        osname="%-15s"%('NaN')
 
    oroci='NaN'
    if(roci != None and roci != undef and roci != 0):
        oroci="%3.0f"%(roci)
        
    opoci='NaN '
    if(poci != None and poci != undef and poci != 0):
        opoci="%4.0f"%(poci)
        
    if(vmax != None and vmax != undef):
        ovmax="%3.0f"%(vmax)
 
    opmin='NaN '   
    if(pmin != None and pmin != undef):
        opmin="%4.0f"%(pmin)

    
    got34=0
    if(r34m != None and r34m != undef):
        got34=1
        or34ne=getr34(r34[0])
        or34se=getr34(r34[1])
        or34sw=getr34(r34[2])
        or34nw=getr34(r34[3])
        or34=' %s , %s , %s , %s , '%(or34ne,or34se,or34sw,or34nw)
        or34m='    , '
        if(r34m != None and r34m != undef):
            or34m="%3.0f , "%(r34m)
    else:
        or34=' NaN , NaN , NaN , NaN ,'
        or34m='NaN , '
    
    got50=0
    if(r50m != None and r50m!= undef):
        got50=1
        or50ne=getr50(r50[0])
        or50se=getr50(r50[1])
        or50sw=getr50(r50[2])
        or50nw=getr50(r50[3])
        or50=' %s , %s , %s , %s , '%(or50ne,or50se,or50sw,or50nw)
        or50m='    , '
        if(r50m != None and r50m != undef):
            or50m="%3.0f , "%(r50m)
    else:
        or50=' NaN , NaN , NaN , NaN ,'
        or50m=' NaN , '
        if(got34):
            or50m='NaN , '

    ormax='NaN'
    if(rmax != None and rmax != undef and rmax != 0):
        ormax="%3.0f"%(rmax)
        
    odepth='NaN'
    if(depth != None and depth != undef and depth != ''):
        odepth=' %s '%(depth)
        

    odtgstm="%s , %s , %s , %s , %s ,"%(dtg,ostmid,osname,tctype,stmDev)
    omotion="%3.0f , %2.0f , "%(cdir,cspd)
    otrkmotion="%3.0f , %2.0f , "%(trkdir,trkspd)
    oposition="%5.1f , %5.1f , "%(rlat,rlon)
    ointensity="%s , %s ,"%(ovmax,opmin)
    ocodes="%s , %s , %s , %s , "%(tccode,wncode,dirtype,posttype)
    orocipoci="%s , %s , "%(oroci,opoci)

        
    if(alf == 0.0 or alf == undef):
        oalf=' NaN'
    else:
        oalf="%4.2f"%(alf)
        
    # -- 20230125 -- bug in odepth -- has extra ','  adds extra column
    #
    tdo=tdo.strip()
    if(tdo == '---' or tdo == ''): tdo='NaN'
    omisc="%s , %s , %s , %s "%(oalf,odepth,ormax,tdo)    
    
    if(verb):
        print 'dtg        : ',odtgstm,stmidm2,stmid,ostmid
        print 'position   : ',oposition
        print 'intensity  : ',ointensity
        print 'motion:    : ',omotion,'type: ',dirtype
        print 'trkmotion  : ',otrkmotion
        print 'tc|wncodes : ',ocodes
        print 'roci/poci  : ',orocipoci
        print 'r34        : ',or34m,or34
        print 'r50        : ',or50m,or50
        print 'misc       : ',omisc
    
    opart1="%s %s %s"%(odtgstm,oposition,ointensity)
    opart2="%s %s"%(omotion,otrkmotion)
    opart3="%s %s %s %s"%(or34m,or34,or50m,or50)
    if(got50): ocodes="%s"%(ocodes)
    else:      ocodes=" %s"%(ocodes)
    opart4="%s %s %s"%(ocodes,orocipoci,omisc)
    ocard="%s %s %s %s"%(opart1,opart2,opart3,opart4)
    ocard=ocard.replace(' ','')
    ocard=ocard+','
    if(verb): print 'ooo---ooo',ocard
    return(ocard)
    
    

def parseStmSumCard(card):
    
    tt=card.split(",")
    tstmid=tt[0]
    sname=tt[3]
    bdtg=tt[9]
    edtg=tt[10]
    stm9x=tt[22]
    t2gen=tt[23]
    dtggen=tt[24].strip()
    rc=(tstmid,bdtg,edtg,sname,stm9x,t2gen,dtggen)
    return(rc)
    

def getTcData(year,basin):
    
    print 'qqqq',year,basin
    if(basin =='shem'):
        stmopt='h.%s'%(year)
        tD=TcData(stmopt=stmopt)
    elif(basin =='io'):
        stmopt='i.%s'%(year)
        tD=TcData(stmopt=stmopt)
    elif(basin =='epac'):
        stmopt='c.%s,e.%s'%(year,year)
        tD=TcData(stmopt=stmopt)
    elif(basin =='lant'):
        stmopt='l.%s'%(year)
        tD=TcData(stmopt=stmopt)
    elif(basin =='wpac'):
        stmopt='w.%s'%(year)
        tD=TcData(stmopt=stmopt)
    return(tD)

def getMd3path(tstmid):
    
    rc=getStmParams(tstmid)
    stm3id="%s%s"%(rc[0],rc[1])
    stm3id=stm3id.upper()
    
    tyear=rc[2]
    tmask="%s/%s/*/%s*"%(sbtSrcDir,tyear,stm3id)
    odirs=glob.glob("%s"%(tmask))
    if(len(odirs) == 1):
        sdir=odirs[0]
    else:
        print 'EEE -- finding sdir in getMd3path for sbtSrcDir: ',sbtSrcDir,' tstmid: ',tstmid,'sayounara'
        sys.exit()

    if(IsNN(tstmid)):
        md3mask="%s/*-%s-md3-BT.txt"%(sdir,tyear)
        md3paths=glob.glob(md3mask)
    else:
        md3mask="%s/*-%s-md3.txt"%(sdir,tyear)
        md3paths=glob.glob(md3mask)
        
    if(len(md3paths) == 1):
        md3path=md3paths[0]
    else:
        print 'EEE -- finding md3path in getMd3Spath for sbtSrcDir: ',sbtSrcDir,' tstmid: ',tstmid,'sayounara'
        sys.exit()
        
    return(md3path)
    


def getTstmidsSum(year,basin,spath,ropt='norun',doBTonly=0,verb=0):
    
    (ddir,ffile)=os.path.split(spath)
    cards=open(spath).readlines()
    
    basinStm={}
    allStm={}
    for card in cards:
        
        if(verb):
            n=0
            tt=card.split(',')
            for n in range(0,len(tt)):
                print 'n: %2d'%(n),tt[n]
        
        rc=parseStmSumCard(card)
        (tstmid,bdtg,edtg,sname,stm9x,t2gen,dtggen)=rc
        
        # -- option to do BT only
        #
        if(doBTonly and not(IsNN(stm1id))):
            continue

        basinStm[rc[0]]=(bdtg,edtg,sname,stm9x,t2gen,dtggen)
        
    bstmids=basinStm.keys()
    for bstmid in bstmids:
        allStm[bstmid]=basinStm[bstmid]
        

    return(allStm)    



def getMd3trackSpath(md3path,dobt=0,verb=0):
    
    m3trk={}
    m3info={}
        
    stmcards=open(md3path).readlines()

    for m3card in stmcards:

        mm=m3card.split(',')
        rc=parseMd3Card(mm,dobt=dobt,verb=verb)
        if(rc == None):continue

        (dtg,rlat,rlon,vmax,pmin,tdir,tspd,r34m,r50m,
         tcstate,warn,
         roci,poci,alf,
         depth,eyedia,tdo,ostmid,ostmname,r34,r50)=rc
        m3info[dtg]=mm[1:5]
        if(verb):
            print 'rrrrr',dtg,rlat,rlon,vmax,pmin,tdir,tspd,r34m,r50m,tcstate,warn,roci,poci,ostmid
        m3trk[dtg]=(rlat,rlon,vmax,pmin,tdir,tspd,r34m,r50m,tcstate,warn,roci,poci,alf,depth,eyedia,tdo,ostmid,ostmname,r34,r50)
        
    return(m3trk,m3info)
    


def getTstmidsSumOLD(year,basin,spath,ropt='norun',doBTonly=0):
    
    (ddir,ffile)=os.path.split(spath)
    cards=open(spath).readlines()
    tstmids=[]
    
    for card in cards:
        tt=card.split(":")
        stm3id=tt[0].split()[1]
        stm1id="%s.%s"%(stm3id,year)
        
        # -- option to do BT only
        #
        if(doBTonly and not(IsNN(stm1id))):
            continue

        tstmids.append(stm1id)

    return(tstmids)    



def getTstmidsByYearBasin(years,basins,stbdir):
    
    tstmids=[]
    for year in years:
        tdir="%s/%s"%(stbdir,year)
        MF.ChkDir(tdir,'mk')
        
        for basin in basins:
            spath="%s/stm-%s-%s.txt"%(tdir,basin,year)
            tstmids=tstmids+getTstmidsSum(year,basin,spath)
    
    return(tstmids)        

    
def getPrStatus(tstmid,oPrsiz,verb=0):
    
    def getstatus(siz):
        if(siz < 0):
            stat=0
        elif(siz == 0):
            stat=-1
        else:
            stat=1
        return(stat)
        
    sPr=getstatus(oPrsiz)

    if(verb):
        print 'tstmid: %s'%(tstmid),' sPr: ',sPr
        
    card="%s sPr: %d "%(tstmid,sPr)
    
    return(card)
        
    
def getTClatlonNew(bdtg,tau,m3trk,undef=-999,verb=0):

    tdtg=dtginc(bdtg,tau)

    rlat=rlon=tdir=undef
    try:
        trk=m3trk[tdtg]
    except:
        print 'WWW -- no BT for tdtg: ',tdtg
        return(rlat,rlon,tdir)
    
    (rlat,rlon,vmax,pmin,tdir,tspd,r34m,r50m,tcstate,warn,roci,poci,alf,depth,eyedia,tdo,ostmid,ostmname,r34,r50)=trk
    if(tdir == undef): tdir=270.0
    
    if(verb): print 'md3:',rlat,rlon,tdir
    
    return(rlat,rlon,tdir)


def getEraTrk(eraDir,tstmid,model,dtg,verb=0):
    
    etrk={}
    
    tdmask="%s/tcmeta.*%s*"%(eraDir,tstmid.lower())
    tdfiles=glob.glob(tdmask)
    if(len(tdfiles) == 1):
        trkpath=tdfiles[0]
        print 'TTT trkpath: ',trkpath
    else:
        print 'NOOOOO ERA5 tcmeta for: ',tstmid,'dtg: ',dtg,' return etrk={}'
        return(etrk)
    
    if(MF.getPathSiz(trkpath) > 0):
        cards=open(trkpath).readlines()
    else:
        print 'EEE - no tcmeta at ',trkpath
        return(etrk)

    if(len(cards) == 1):
        print 'EEE-badTCmeta in getEraTrk: ',trkpath
        return(etrk)

    sname=cards[0].split()[-1]
    ntaus=cards[1].split()[-2]
    
    
    for card in cards[2:]:
        tt=card[0:-1].split()
        tau=int(tt[0])
        elat=float(tt[1])
        elon=float(tt[2])
        epmin=float(tt[-3])
        edir=float(tt[-2])
        espd=float(tt[-1])
    
        etrk[tau]=(elat,elon,edir,epmin,espd)
        if(verb): print 'eeeeeeeeeeeeeeee',tau,elat,elon,epmin,edir,espd
        
    return(etrk)

def makePrCard(dtgdat,tcdat,ctpr6bm,ctpr6em,gtpr6bm,gtpr6em,itpr6bm,itpr6em,eprm,eprmc,
               doRad=0,verb=0):
    
    (tstmid,dtg,tau)=dtgdat
    card1="%10s , %s , "%(tstmid,dtg)

    (pblat,pblon,pbdir,pelat,pelon,pedir)=tcdat
    cardb="BT:, %5.1f , %5.1f , %3.0f , "%(pblat,pblon,pbdir)
    carde='E5:, %5.1f , %5.1f , %3.0f , '%(pelat,pelon,pedir)
    card1=card1+cardb+carde
    
    kk=ctpr6bm.keys()
    kk.sort()

    if(doRad):
        cardpr="rad, "
        for k in kk:
            r=radInfPrKM[k]
            cardpr=cardpr+"%3d , "%(r)
    else:
        cardpr=''
        
    cardpr=cardpr+'obBT, '
    for k in kk:
        c6bm=float(ctpr6bm[k])
        g6bm=float(gtpr6bm[k])
        i6bm=float(itpr6bm[k])
        cardpr=cardpr+"C%-5.1f , G%-5.1f , I%-5.1f , "%(c6bm,g6bm,i6bm)

    cardpr=cardpr+' obE5, '
    for k in kk:
        c6em=float(ctpr6em[k])
        g6em=float(gtpr6em[k])
        i6em=float(itpr6em[k])
        cardpr=cardpr+"C%-5.1f , G%-5.1f , I%-5.1f , "%(c6em,g6em,i6em)
    
    cardpr=cardpr+' E5pr, '
    for k in kk:
        e6em=float(eprm[k])
        r6em=float(eprmc[k])
        cardpr=cardpr+"%5.1f , %5.0f , "%(e6em,r6em)
    
    fcard=card1+cardpr
    
    if(verb): print fcard
    return(fcard)

def parseDssTrk(dtg,dds,verb=0):
    
    def getr34(r34):
        or34='   '
        if(r34 != undef):
            or34="%3.0f"%(r34)
        return(or34)
            
    def getr50(r50):
        or50='   '
        if(r50 != undef):
            or50="%3.0f"%(r50)
        return(or50)
            
    #alf=b1id=depth=dir=dirtype=ndtgs=ntrk=ostmid=pmin=poci=posttype=r34=r34m=r50=r50m=rlat\
    #    =rlon=rmax=roci=sname=spd=stmid=tccode=tdo=trkdir=trkspd=undef=vmax=wncode=None
    
    alf=dds.alf          #0.0
    b1id=dds.b1id        #W
    depth=dds.depth      #M
    dir=dds.dir          #275.449145529
    dirtype=dds.dirtype  #B
    ndtgs=dds.ndtgs      #40
    ntrk=dds.ntrk        #19
    ostm2id=dds.ostm2id  #wp30.2019
    pmin=dds.pmin        #984
    poci=dds.poci        #1009
    posttype=dds.postype #B
    r34=dds.r34          #[90, 45, 50, 80]
    r34m=dds.r34m        #66.25
    r50=dds.r50          #[40, 15, 15, 35]
    r50m=dds.r50m        #26.25
    rlat=dds.rlat        #10.8
    rlon=dds.rlon        #127.7
    rmax=dds.rmax        #15
    roci=dds.roci        #165
    sname=dds.sname      #PHANFONE
    spd=dds.spd          #15.7957548819
    stmid=dds.stmid      #30W.2019
    tccode=dds.tccode    #TY
    tdo=dds.tdo          #AMN
    trkdir=dds.trkdir    #275.449145529
    trkspd=dds.trkspd    #15.7957548819
    undef=dds.undef      #-999
    vmax=dds.vmax        #75
    wncode=dds.wncode    #WN

    osname='               , '
    if(sname != None and sname != undef):
        osname="%-15s"%(sname)
 
    oroci='   '
    if(roci != None and roci != undef and roci != 0):
        oroci="%3.0f"%(roci)
        
    opoci='    '
    if(poci != None and poci != undef and poci != 0):
        opoci="%4.0f"%(poci)
        
    if(vmax != None and vmax != undef):
        ovmax="%3.0f"%(vmax)
 
    opmin='    '   
    if(pmin != None and pmin != undef):
        opmin="%4.0f"%(pmin)

    
    got34=0
    if(r34 != None and r34 != undef):
        got34=1
        or34ne=getr34(r34[0])
        or34se=getr34(r34[1])
        or34sw=getr34(r34[2])
        or34nw=getr34(r34[3])
        or34=' %s , %s , %s , %s , '%(or34ne,or34se,or34sw,or34nw)
        or34m='    , '
        if(r34m != None and r34m != undef):
            or34m="%3.0f , "%(r34m)
    else:
        or34='     ,     ,     ,     ,'
        or34m='    , '
    
    got50=0
    if(r50 != None and r50 != undef):
        got50=1
        or50ne=getr50(r50[0])
        or50se=getr50(r50[1])
        or50sw=getr50(r50[2])
        or50nw=getr50(r50[3])
        or50=' %s , %s , %s , %s , '%(or50ne,or50se,or50sw,or50nw)
        or50m='    , '
        if(r50m != None and r50m != undef):
            or50m="%3.0f , "%(r50m)
    else:
        or50='     ,     ,     ,     ,'
        or50m='     , '
        if(got34):
            or50m='    , '

    ormax='NaN'
    if(rmax != None and rmax != undef and rmax != 0):
        ormax="%3.0f"%(rmax)
        
    odepth='NaN'
    if(depth != None and depth != undef and depth != ''):
        odepth='%s'%(depth)
        
    otdo='NaN'
    print 'ttt',tdo
    
    omotion="%3.0f , %2.0f , "%(dir,spd)
    otrkmotion="%3.0f , %2.0f , "%(trkdir,trkspd)
    odtgstm="%s , %s , %s , "%(dtg,stmid,osname)
    oposition="%5.1f , %5.1f , "%(rlat,rlon)
    ointensity="%s , %s ,"%(ovmax,opmin)
    ocodes="%s , %s , %s , %s , "%(tccode,wncode,dirtype,posttype)
    orocipoci="%s , %s , "%(oroci,opoci)

        
    if(alf == 0.0 or alf == undef):
        oalf='NaN'
    else:
        oalf="%4.2f"%(alf)
        
    # -- 20230125 -- bug in odepth -- has extra ','  adds extra column
    #
    omisc="%s , %s , %s , %s "%(oalf,odepth,ormax,otdo)    
    
    if(verb):
        print 'dtg        : ',odtgstm
        print 'position   : ',oposition
        print 'intensity  : ',ointensity
        print 'motion:    : ',omotion,'type: ',dirtype
        print 'trkmotion  : ',otrkmotion
        print 'tc|wncodes : ',ocodes
        print 'roci/poci  : ',orocipoci
        print 'r34        : ',or34m,or34
        print 'r50        : ',or50m,or50
        print 'misc       : ',omisc
    
    opart1="%s %s %s"%(odtgstm,oposition,ointensity)
    opart2="%s %s"%(omotion,otrkmotion)
    opart3="%s %s %s %s"%(or34m,or34,or50m,or50)
    if(got50): ocodes="%s"%(ocodes)
    else:      ocodes=" %s"%(ocodes)
    opart4="%s %s %s"%(ocodes,orocipoci,omisc)
    ocard="%s %s %s %s"%(opart1,opart2,opart3,opart4)
    return(ocard)
    
def getStmids4SumPath(sumPath):
    (sdir,sfile)=os.path.split(sumPath)
    ss=sdir.split("/")
    storm=ss[-1]
    ss=storm.split('-')
    stmid="%s.%s"%(ss[0],ss[1])
    if(IsNN(stmid)):
        stype='NN'
        stm1id=stmid
        sname=ss[2]
        stm9xid="%s.%s"%(ss[-1],ss[1])
    elif(Is9X(stmid)):
        stype='9X'
        stm9xid=stmid
        sname=ss[2]
        if(find(sname,'NON')):
            stm1id='XXX.%s'%(ss[1])
        else:
            stm1id="%s.%s"%(ss[-1],ss[1])
        
    return(stype,stm1id,sname,stm9xid)         
    
# -- bug in parseDssTrk -- handle here since we can't redo making NNW-sum.txt
#
def parseDssTrkMD3(dtg,dds,stm1id,stm9xid,basin,rcsum=None,sname=None,verb=0,warn=0):
    
    def getr34(r34):
        or34='   '
        if(r34 != undef):
            or34="%3.0f"%(r34)
        return(or34)
            
    def getr50(r50):
        or50='   '
        if(r50 != undef):
            or50="%3.0f"%(r50)
        return(or50)
            
    #alf=b1id=depth=dir=dirtype=ndtgs=ntrk=ostmid=pmin=poci=posttype=r34=r34m=r50=r50m=rlat\
    #    =rlon=rmax=roci=sname=spd=stmid=tccode=tdo=trkdir=trkspd=undef=vmax=wncode=None
    
    tctype='Nan'
    stmDev='Nan'
    if(rcsum != None):
        tctype=rcsum[0]
        stmDev=rcsum[1]
        
    alf=dds.alf          #0.0
    b1id=dds.b1id        #W
    depth=dds.depth      #M
    dir=dds.dir          #275.449145529
    dirtype=dds.dirtype  #B
    ndtgs=dds.ndtgs      #40
    ntrk=dds.ntrk        #19
    ostm2id=dds.ostm2id  #wp30.2019
    pmin=dds.pmin        #984
    poci=dds.poci        #1009
    posttype=dds.postype #B
    r34=dds.r34          #[90, 45, 50, 80]
    r34m=dds.r34m        #66.25
    r50=dds.r50          #[40, 15, 15, 35]
    r50m=dds.r50m        #26.25
    rlat=dds.rlat        #10.8
    rlon=dds.rlon        #127.7
    rmax=dds.rmax        #15
    roci=dds.roci        #165
    # -- not here...sname=dds.sname      #PHANFONE
    spd=dds.spd          #15.7957548819
    stmid=dds.stmid      #30W.2019
    tccode=dds.tccode    #TY
    tdo=dds.tdo          #AMN
    trkdir=dds.trkdir    #275.449145529
    trkspd=dds.trkspd    #15.7957548819
    undef=dds.undef      #-999
    vmax=dds.vmax        #75
    wncode=dds.wncode    #WN

    if(sname != None and sname != undef):
        osname="%-15s"%(sname)
    else:
        osname="%-15s"%('NaN')
 
    oroci='NaN'
    if(roci != None and roci != undef and roci != 0):
        oroci="%3.0f"%(roci)
        
    opoci='NaN '
    if(poci != None and poci != undef and poci != 0):
        opoci="%4.0f"%(poci)
        
    if(vmax != None and vmax != undef):
        ovmax="%3.0f"%(vmax)
 
    opmin='NaN '   
    if(pmin != None and pmin != undef):
        opmin="%4.0f"%(pmin)

    
    got34=0
    if(r34m != None and r34m != undef):
        got34=1
        or34ne=getr34(r34[0])
        or34se=getr34(r34[1])
        or34sw=getr34(r34[2])
        or34nw=getr34(r34[3])
        or34=' %s , %s , %s , %s , '%(or34ne,or34se,or34sw,or34nw)
        or34m='    , '
        if(r34m != None and r34m != undef):
            or34m="%3.0f , "%(r34m)
    else:
        or34=' NaN , NaN , NaN , NaN ,'
        or34m='NaN , '
    
    got50=0
    if(r50m != None and r50m!= undef):
        got50=1
        or50ne=getr50(r50[0])
        or50se=getr50(r50[1])
        or50sw=getr50(r50[2])
        or50nw=getr50(r50[3])
        or50=' %s , %s , %s , %s , '%(or50ne,or50se,or50sw,or50nw)
        or50m='    , '
        if(r50m != None and r50m != undef):
            or50m="%3.0f , "%(r50m)
    else:
        or50=' NaN , NaN , NaN , NaN ,'
        or50m=' NaN , '
        if(got34):
            or50m='NaN , '

    ormax='NaN'
    if(rmax != None and rmax != undef and rmax != 0):
        ormax="%3.0f"%(rmax)
        
    odepth='NaN'
    if(depth != None and depth != undef and depth != ''):
        odepth=' %s '%(depth)
        
        
    # -- replace md2 stmid with stmid from DIRECTORY
    # -- stm1id is set to NN or 9X
    #
    ostmid=stmid.lower()
    if(stmDev == 'DEV' and Is9X(ostmid)): 
        ostmid=stm1id.lower()
    elif(stmDev == 'NONdev' and Is9X(ostmid)): 
        ostmid=stm9xid.lower()
    if(IsNN(ostmid)): ostmid=stm1id.lower()


    odtgstm="%s , %s , %s , %s , %s ,"%(dtg,ostmid,osname,tctype,stmDev)
    omotion="%3.0f , %2.0f , "%(dir,spd)
    otrkmotion="%3.0f , %2.0f , "%(trkdir,trkspd)
    oposition="%5.1f , %5.1f , "%(rlat,rlon)
    ointensity="%s , %s ,"%(ovmax,opmin)
    ocodes="%s , %s , %s , %s , "%(tccode,wncode,dirtype,posttype)
    orocipoci="%s , %s , "%(oroci,opoci)

        
    if(alf == 0.0 or alf == undef):
        oalf=' NaN'
    else:
        oalf="%4.2f"%(alf)
        
    # -- 20230125 -- bug in odepth -- has extra ','  adds extra column
    #
    tdo=tdo.strip()
    if(tdo == '---' or tdo == ''): tdo='NaN'
    omisc="%s , %s , %s , %s "%(oalf,odepth,ormax,tdo)    
    
    if(verb):
        print 'dtg        : ',odtgstm
        print 'position   : ',oposition
        print 'intensity  : ',ointensity
        print 'motion:    : ',omotion,'type: ',dirtype
        print 'trkmotion  : ',otrkmotion
        print 'tc|wncodes : ',ocodes
        print 'roci/poci  : ',orocipoci
        print 'r34        : ',or34m,or34
        print 'r50        : ',or50m,or50
        print 'misc       : ',omisc
    
    opart1="%s %s %s"%(odtgstm,oposition,ointensity)
    opart2="%s %s"%(omotion,otrkmotion)
    opart3="%s %s %s %s"%(or34m,or34,or50m,or50)
    if(got50): ocodes="%s"%(ocodes)
    else:      ocodes=" %s"%(ocodes)
    opart4="%s %s %s"%(ocodes,orocipoci,omisc)
    ocard="%s %s %s %s"%(opart1,opart2,opart3,opart4)                                                        
    return(ocard)
    
def getStmids4SumPath(sumPath):
    (sdir,sfile)=os.path.split(sumPath)
    ss=sdir.split("/")
    storm=ss[-1]
    basin=ss[-2]
    ss=storm.split('-')
    stmid="%s.%s"%(ss[0],ss[1])
    if(IsNN(stmid)):
        stype='NN'
        stm1id=stmid
        if(len(ss) == 5):
            sname="%s-%s"%(ss[2],ss[3])
        else:
            sname=ss[2]
        stm9xid="%s.%s"%(ss[-1],ss[1])
        stm9xid=stm9xid.lower()
    elif(Is9X(stmid)):
        sname='9X-%s'%(ss[0])
        stm9xid=stmid
        stype=ss[2]
        if(stype == 'NONdev'):
            stm1id=stmid
        elif(stype == 'DEV'):
            stm1id="%s.%s"%(ss[-1],ss[1])
        else:
            stm1id='XXX.%s'%(ss[1])
            stm1id=stm1id
            
        stm1id=stm1id.lower()
        
    return(stype,stm1id,sname,stm9xid,basin)         
    
def getCtlpathTaus(model,dtg,maxtau=168,verb=0,doSfc=0):
    
    taus=[]
    ctlpath=taus=nfields=tauOffset=None
    rc=w2.getW2fldsRtfimCtlpath(model,dtg,maxtau=maxtau,verb=verb,doSfc=doSfc)
    if(rc == None):
        print 'EEEE---tcVM-getCtlpathTaus-w2base.getW2fldsRtfimCtlpath...sayounara...for model: ',model,' dtg: ',dtg
        sys.exit()
    if(rc[0]):
        ctlpath=rc[1]
        taus=rc[2]
        nfields=rc[-2]
        tauOffset=rc[-1]

    return(ctlpath,taus,nfields,tauOffset)

def getInvPath4Dtgopt(dtgopt,invdir='./inv',getonly=0):

    invmask="%s/inv-sbt-track-v??-%s.txt"%(invdir,dtgopt)
    invs=glob.glob(invmask)
    
    nnver=0
    npver=0
    if(len(invs) > 0):
        previnv=invs[-1]
        tt=previnv.split('-')
        pver=tt[-2]
        npver=int(pver[-2:])
        nnver=npver+1
        
    if(getonly): nnver=npver
        
    nver="v%02d"%(nnver)
    
    invpath="inv/inv-sbt-track-%s-%s.txt"%(nver,dtgopt)
    return(invpath)

def Rlatlon2Clatlon(rlat,rlon,dotens=1,dodec=0,dozero=0):

    hemns='X'
    hemew='X'
    ilat=999
    ilon=9999

    if(rlat > -90.0 and rlat < 88.0):

        if(dotens):
            ilat=nint(rlat*10)
        else:
            ilat=nint(rlat)

        hemns='N'
        if(ilat<0):
            ilat=abs(ilat)
            hemns='S'
            rlat=abs(rlat)

        if(rlon > 180.0):
            rlon=360.0-rlon
            hemew='W'
        else:
            hemew='E'

        if(rlon < 0.0):
            rlon=abs(rlon)
            hemew='W'

        if(dotens):
            ilon=nint(rlon*10)
        else:
            ilon=nint(rlon)

    if(dotens):
        clat="%3d%s"%(ilat,hemns)
        clon="%4d%s"%(ilon,hemew)
        if(dozero):
            clat="%03d%s"%(ilat,hemns)
            clon="%04d%s"%(ilon,hemew)
    else:
        if(dozero):
            clat="%02d%s"%(ilat,hemns)
            clon="%03d%s"%(ilon,hemew)
        else:
            clat="%02d%s"%(ilat,hemns)
            clon="%03d%s"%(ilon,hemew)

    if(dodec):
        clat="%5.1f%s"%(rlat,hemns)
        clon="%5.1f%s"%(rlon,hemew)

    return(clat,clon)

def isIOBasinStm(stmid):

    tt=stmid.split('.')
    stmid=tt[0]

    if(len(stmid) > 4):
        return(-1)

    if(len(stmid) == 1):
        ustmid=stmid.upper()
    elif(len(stmid) == 2):
        ustmid=stmid.upper()
    elif(len(stmid) == 3):
        ustmid=stmid[2].upper()
    elif(len(stmid) == 4):
        ustmid=stmid[0:2].upper()

    if(len(ustmid) == 1):
        if(ustmid == 'I' or ustmid == 'A' or ustmid == 'B'):
            return(1)
        else:
            return(0)
    elif(len(ustmid) == 2):
        if(ustmid == 'IO' or ustmid == 'BB' or ustmid == 'AA'):
            return(1)
        else:
            return(0)
def isShemBasinStm(stmid):

    tt=stmid.split('.')
    stmid=tt[0]

    if(len(stmid) > 4):
        return(-1)

    if(len(stmid) == 1):
        ustmid=stmid.upper()
    elif(len(stmid) == 2):
        ustmid=stmid.upper()
    elif(len(stmid) == 3):
        ustmid=stmid[2].upper()
    elif(len(stmid) == 4):
        ustmid=stmid[0:2].upper()

    if(len(ustmid) == 1):
        if(ustmid == 'S' or ustmid == 'P' or ustmid == 'Q' or ustmid == 'H'):
            return(1)
        else:
            return(0)
    elif(len(ustmid) == 2):
        if(ustmid == 'SH' or ustmid == 'SP' or ustmid == 'SI' or ustmid == 'SL'):
            return(1)
        else:
            return(0)


# -- CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC

class MFbase():

    def sendEmail(self,to_addr_list,subject,message,
                  passwdFile='/data/amb/users/fiorino/w21/prc/lib/python/passwdMFemail',
                  cc_addr_list=[],
                  from_addr='michael.fiorino@noaa.gov',
                  smtpserver='smtp.gmail.com:587',
                  login='michael.fiorino@noaa.gov',
                  password=None,
                  ):


        import smtplib,base64

        # did base64.b64encode(real password) - put in passwdFile and made it rw by owner only
        # and did NOT include in svn
        #

        password=open(passwdFile).read()
        password=base64.b64decode(password)

        header  = 'From: %s\n' % from_addr
        header += 'To: %s\n' % ','.join(to_addr_list)
        if(len(cc_addr_list) > 0): header += 'Cc: %s\n' % ','.join(cc_addr_list)
        header += 'Subject: %s\n\n' % subject

        message = header + message

        server = smtplib.SMTP(smtpserver)
        server.starttls()
        server.login(login,password)
        problems = server.sendmail(from_addr, to_addr_list, message)
        server.quit()

    def find(self,mystr,pattern):
            rc=0
            if(mystr.find(pattern) != -1): rc=1
            return(rc)


    def ls(self,findstr=None,lsopt=None,maxchar=116,varsonly=0,quiet=0):

        methods=[]
        variables=[]
        clss=[]
        nvar=0

        mlen=28

        mformat="MMM: %%-%ds: %%s"%(mlen)
        cformat="CCC: %%-%ds: %%s"%(mlen)
        vformat="VVV(%%3d): %%-%ds: %%s"%(mlen)
        dd=inspect.getmembers(self)

        for d in dd:
            name=d[0]
            if(findstr != None):
                if(not(find(name,findstr))): continue

            if(type(d[1]) is ListType and len(str(d[1])) > maxchar):
                val=str(d[1])[0:maxchar]+' ... '
            elif(type(d[1]) is DictType and len(str(d[1])) > maxchar):
                val=str(d[1])[0:maxchar]+' ... '
            else:
                try:
                    val=str(d[1])
                except:
                    val='undef...'

            if(lsopt != None): val=str(d[1])
            

            if(find(val,'<bound method') or find(val,'<module ')):
                methods.append(mformat%(name[0:mlen],val[0:maxchar]))
            elif(find(val,'instance at')):
                clss.append(cformat%(name[0:mlen],val[0:maxchar]))
            else:
                if(len(val) >= maxchar): val=val[0:maxchar] + '... NOT ListType or DictType'
                variables.append(vformat%(nvar,name[0:mlen],val))
                nvar=nvar+1

        if(not(quiet)):

            if(len(clss) > 0 and not(varsonly)):
                print
                for cls in clss:
                    print cls
                print

            if(len(methods) > 0 and not(varsonly)):
                for method in methods:
                    print method
                print

            for variable in variables:
                print variable


        return(clss,methods,variables)


    def setObjVarsNone(self):

        keepvars=keepclss=None

        if(hasattr(self,'keepObjVars')):
            keepvars=self.keepObjVars

        if(hasattr(self,'keepObjClss')):
            keepclss=self.keepObjClss

        if(keepvars == None and keepclss == None):
            return


        # -- get the classes, methods, vars
        #
        (clss,methods,variables)=self.ls(quiet=1)

        if(keepvars != None):
            for var in variables:
                vvar=var.split()[2].strip()
                if(find(vvar,'__')): continue
                if(not(vvar in keepvars)):
                    try:
                        cmd="self.%s=None"%(vvar)
                        exec(cmd)
                    except:
                        print 'MFbase.setObjVarsNone -- did not None vvar: ',vvar

        if(keepclss != None):
            for cls in clss:
                vcls=cls.split()[1].strip()
                if(find(vcls,'__')): continue
                if(not(vcls in keepclss)):
                    try:
                        cmd="self.%s=None"%(vcls)
                        exec(cmd)
                    except:
                        print 'MFbase.setObjVarsNone -- did not None vcls: ',vcls




    def setPyppath(self,pyppath=None):
        """ method to set the pyppath for getPyp and putPyp"""

        if(pyppath == None and hasattr(self,'pyppath') and self.pyppath == None):
            ppath='/tmp/zy0x1w2.pyp'

        elif(pyppath != None):
            ppath=pyppath

        elif(hasattr(self,'pyppath') and self.pyppath != None):
            ppath=self.pyppath

        else:
            print 'EEE unable to open either pyppath: ',pyppath,' or self.pyppath: ',self.pyppath
            return(None)

        return(ppath)



    def getPyp(self,pyppath=None,unlink=0,verb=0):

        ppath=self.setPyppath(pyppath=pyppath)
        if(ppath == None): return(None)

        if(unlink):
            try:    os.unlink(ppath)
            except:  None

        if(os.path.exists(ppath)):
            if(verb): print "getPyp opening: ",ppath
            PS=open(ppath)
            try:
                FR=pickle.load(PS)
                if(verb): print "hai, getPyp ha, itadakimasu..."
            except:
                if(verb): print "IEE, getPyp ga, komarimashita ne! "
                FR=None
            PS.close()
            return(FR)

        else:
            return(None)


    def putPyp(self,pyp=None,pyppath=None,unlink=0,
               unlinkException=0,
               unlinkBadDump=0,
               verb=1):

        ppath=self.setPyppath(pyppath=pyppath)
        if(ppath == None): return(None)

        if(pyp != None):
            pyppckle=pyp
        else:
            pyppckle=self

        if(unlink):
            try:
                os.unlink(ppath)
            except:
                None

        try:
            PS=open(ppath,'w')
            pickle.dump(pyppckle,PS)
            PS.close()
            siz=os.path.getsize(ppath)
            if(verb):
                print 'III dumping pyp: ',pyppckle
                print 'III     to path: ',ppath,' size: ',siz
        except:
            if(unlinkException):
                print 'WWW killing ppath: ',ppath,' on open/dump exception'
                os.unlink(ppath)
                try:
                    PS=open(ppath,'w')
                    pickle.dump(pyppckle,PS)
                    PS.close()
                except:
                    print """EEEEE unable to pickle.dump: ',ppath,' after unlinkException, kill it anyway...it's baaad, it's baaad..."""
                    os.unlink(ppath)

            else:
                print 'EEEEE unable to pickle.dump: ',ppath,' so unlink it???'
                if(unlinkBadDump): os.unlink(ppath)


    def initCurState(self):

        self.curdtg=dtg()
        self.curphr=dtg('phr')
        self.curyear=self.curdtg[0:4]

        if(not(hasattr(self,'curtime'))):  self.curtime=[]

        self.curtime.append(dtg('dtg.phms'))



    def sTimer(self,tag='notag'):

        if(not(hasattr(self,'stimers'))):    self.stimers={}
        value=timer()
        self.loadDictList(self.stimers,tag,value)

    def dTimer(self,tag='notag'):

        sleep(0.1)
        phms=dtg('dtg.phms')
        if(hasattr(self,'stimers')):
            value=time.time()-self.stimers[tag][-1]
            
        card="TTTTTTTTTTTTTTTTTTTTTTT-------------------timer: %-72s: %6.3f      at: %s"%(tag,value,phms)
        print card
        return(card)

    def sTime(self,tag='notag'):

        if(not(hasattr(self,'stimes'))):    self.stimes={}
        value=timer()
        self.loadDictList(self.stimes,tag,value)


    def dTime(self,tag='notag'):

        if(not(hasattr(self,'curdtimes'))):
            self.curdtimes={}
        else:
            if( type(self.curdtimes) is not(DictType) ): self.curdtimes={}

        value=dtg('dtg.phms')
        self.loadDictList(self.curdtimes,tag,value)

        if(not(hasattr(self,'dtimes'))):   self.dtimes={}
        value=time.time()-self.stimes[tag][-1]
        self.loadDictList(self.dtimes,tag,value)



    def loadDictList(self,dict,key,value):
        try:
            dict[key].append(value)
        except:
            dict[key]=[]
            dict[key].append(value)




class MFutils(MFbase):

    import mf

    calendar='gregorian'

    mname = {
        '01':'January',
        '02':'February',
        '03':'March',
        '04':'April',
        '05':'May',
        '06':'June',
        '07':'July',
        '08':'August',
        '09':'September',
        '10':'October',
        '11':'November',
        '12':'December'
    }

    mday=(0,31,28,31,30,31,30,31,31,30,31,30,31)
    mdayleap=(0,31,29,31,30,31,30,31,31,30,31,30,31)
    aday=(1,32,60,91,121,152,182,213,244,274,305,335)
    adayleap=(1,32,61,92,122,153,183,214,245,275,306,336)

    sec2hr=1/3600.0

    pyppath=None

    def nDayYear(self,yyyy):
        nd=365
        if (int(yyyy)%4 == 0): nd=366
        return(nd)

    def nDayMonth(self,yyyymm):
        yyyy=int(yyyymm[0:4])
        mm=int(yyyymm[4:6])

        leap=0
        if (yyyy%4 == 0): leap=1

        #
        # override leaping if 365 day calendar
        #
        if(self.calendar == '365day'): leap=0

        if(leap):
            return(self.mdayleap[mm])
        else:
            return(self.mday[mm])


    def TimeZoneName(self):

        import time
        tz=time.tzname
        tz=tz[time.daylight]
        return(tz)


    def Dtg2JulianDay(self,dtg):

        import time
        year=int(str(dtg)[0:4])
        month=int(str(dtg)[4:6])
        day=int(str(dtg)[6:8])

        t = time.mktime((year, month, day, 0, 0, 0, 0, 0, 0))
        jday=time.gmtime(t)[7]
        jday="%03d"%(int(jday))
        return (jday)

    def YearJulianDay2YMD(self,year,jday):

        from datetime import date,timedelta
        ymd=date(int(str(year)),1,1) + timedelta(int(str(jday))-1)
        ymd=ymd.strftime("%Y%m%d")
        return(ymd)



    def YearJulianDay2Dtg(self,year,jday,chour=None):

        from datetime import date,timedelta
        ijday=int(jday)
        rjdayhr=jday-ijday*1.0
        ymd=date(int(str(year)),1,1) + timedelta(ijday-1)
        if(chour == None):
            chour="%02d"%(int(rjdayhr*24.0+0.5))
        ymd=ymd.strftime("%Y%m%d")
        dtg=ymd+chour
        return(dtg)


    def Dtg2Timei(self,dtg):
        timei=time.strptime(dtg,"%Y%m%d%H")
        return(timei)


    def DeltaTimei(self,timei1,timei2):

        t1=time.mktime(timei1)
        t2=time.mktime(timei2)
        dt=(t1-t2)/3600.0
        return(dt)

    def getGtime4DTG(self,dtg,
                     #localTZ='America/Denver', localTZname='MST', localTZnameDST='MDT',
                     localTZ='US/Eastern', localTZname='EST', localTZnameDST='EDT',
                     local=1,verb=0):
        
        from datetime import datetime
        from dateutil import tz
        from datetime import date
        import calendar
        import pytz
        
        
        def findDay(year,month,day):
            born = date(year, month, day)
            return born.strftime("%a")
        
        
        def is_dst (localTZ,dtg=None):
            
            """Determine whether or not Daylight Savings Time (DST)
            is currently in effect"""
            # -- use dtg
        
            if(dtg != None):
                yy=int(dtg[0:4])
                mm=int(dtg[4:6])
                dd=int(dtg[6:8])
    
                x=datetime(yy,1,1,0,0,0)
                y=datetime(yy,mm,dd,0,0,0)
                timezone = pytz.timezone(localTZ)
                tzy = timezone.localize(y, is_dst=None)
                tzx = timezone.localize(x, is_dst=None)
                xoff=str(tzx)[-6:-3]
                yoff=str(tzy)[-6:-3]
                xoff=int(xoff)
                yoff=int(yoff)
                
                return not(xoff == yoff)
        
            # -- use current
            else:
                x = datetime(datetime.now().year, 1, 1, 0, 0, 0, tzinfo=pytz.timezone(localTZ)) # Jan 1 of this year
                y = datetime.now(pytz.timezone(localTZ))
        
                # if DST is in effect, their offsets will be different
                return not (y.utcoffset() == x.utcoffset())
        
    
        utcTZname='UTC'
        
        isDst=is_dst(localTZ,dtg=dtg)
        if(isDst): localTZname=localTZnameDST
        
        from_zone = tz.gettz('utc'.upper())
        to_zone = tz.gettz(localTZ)
        
        if(verb): print 'iii ',isDst,from_zone,to_zone
            
        cdtg=str(dtg)
        
        yy=int(cdtg[0:4])
        mm=int(cdtg[4:6])
        dd=int(cdtg[6:8])
        hh=int(cdtg[8:10])
        ct='%4d-%02d-%02d %02d:%02d:%02d'%(yy,mm,dd,hh,0,0)
        if(verb): print ct
        
        utc = datetime.strptime(ct, '%Y-%m-%d %H:%M:%S')
        utc = utc.replace(tzinfo=from_zone)
    
        # -- get the standard time string for utc and local
        #
        uuu=utc.astimezone(from_zone)
        uu=str(uuu)
    
        mountain = utc.astimezone(to_zone)
        mm=str(mountain)
        
        myy=int(mm[0:4])
        mmm=int(mm[5:7])
        mdd=int(mm[8:10])
        mhh=int(mm[11:13])
        mmn=int(mm[14:16])
        
        uyy=int(uu[0:4])
        umm=int(uu[5:7])
        udd=int(uu[8:10])
        uhh=int(uu[11:13])
        umn=int(uu[14:16])
        
        
        mDDName=findDay(myy,mmm,mdd)
        uDDName=findDay(uyy,umm,udd)
        
        mmName=mountain.strftime('%b').upper()
        ummName=uuu.strftime('%b').upper()
        
        mgtime="%s %02d%02d %s %02d %s"%(mDDName,mhh,mmn,localTZname,mdd,mmName)
        ugtime="%s %02d%02d %s %02d %s"%(uDDName,uhh,umn,utcTZname,udd,ummName)
        if(verb): 
            print 'gggg: ',mgtime
            print 'uggg: ',ugtime
        
        gtime=ugtime
        if(local):
            gtime=mgtime
            
        return(gtime)


    def PathCreateTimeDtgdiff(self,dtg,path):

        # -- handle broken symbolic link -- return -666.66 -- for gfs2 when /public down
        #
        if(os.path.islink(path) and not(os.path.exists(path))): return(-666.66)
         
        if(not(os.path.exists(path))): return(None)
        timei=os.path.getctime(path)
        ctimei=time.gmtime(timei)
        dtimei=self.Dtg2Timei(dtg)
        dt=self.DeltaTimei(ctimei,dtimei)

        return(dt)


    def PathModifyTime(self,path):

        if(not(os.path.exists(path))): return(None,None,None)
        timei=os.path.getmtime(path)
        ltimei=time.localtime(timei)
        gtimei=time.gmtime(timei)
        dtimei=time.strftime("%Y%m%d%H:%M%S",ltimei)
        gdtimei=time.strftime("%Y%m%d%H:%M%S",gtimei)
        ldtg=dtimei[0:10]
        gdtg=gdtimei[0:10]
        return(dtimei,ldtg,gdtg)

    def PathCreateTime(self,path):

        if(not(os.path.exists(path))): return(None,None,None)
        timei=os.path.getctime(path)
        ltimei=time.localtime(timei)
        gtimei=time.gmtime(timei)
        dtimei=time.strftime("%Y%m%d%H:%M%S",ltimei)
        gdtimei=time.strftime("%Y%m%d%H:%M%S",gtimei)
        ldtg=dtimei[0:10]
        gdtg=gdtimei[0:10]
        return(dtimei,ldtg,gdtg)


    def PathModifyTimei(self,path):

        if(not(os.path.exists(path))): return(None,None)
        timei=os.path.getmtime(path)
        gtimei=time.gmtime(timei)
        gdtimei=time.strftime("%Y%m%d%H:%M%S",gtimei)
        return(gtimei,gdtimei)


    def PathCreateTimei(self,path):

        if(not(os.path.exists(path))): return(None,None)
        timei=os.path.getctime(path)
        gtimei=time.gmtime(timei)
        gdtimei=time.strftime("%Y%m%d%H:%M%S",gtimei)
        return(gtimei,gdtimei)


    def PathModifyTimeDtgdiff(self,dtg,path,tzoff=0):

        if(not(os.path.exists(path))): return(None)
        timei=os.path.getmtime(path)
        ctimei=time.gmtime(timei)
        dtimei=self.Dtg2Timei(dtg)
        dt=self.DeltaTimei(ctimei,dtimei)+tzoff

        return(dt)

    def getCurTimei(self):

        ctimei=time.gmtime(time.time())
        return(ctimei)


    def PathModifyTimeCurdiff(self,path,tzoff=0):

        if(not(os.path.exists(path))): return(None)
        timei=os.path.getmtime(path)
        ptimei=time.gmtime(timei)
        ctimei=time.gmtime(time.time())
        dt=self.DeltaTimei(ptimei,ctimei)+tzoff

        return(dt)

    def PathCreateTimeCurdiff(self,path,tzoff=0):

        if(not(os.path.exists(path))): return(None)
        timei=os.path.getctime(path)
        ptimei=time.gmtime(timei)
        ctimei=time.gmtime(time.time())
        dt=self.DeltaTimei(ptimei,ctimei)+tzoff

        return(dt)

    def GetPathSiz(self,path,pathopt='exit',verb=0):

        if(self.ChkPath(path,pathopt='noexit',verb=verb) != 1):
            siz=None
        else:
            siz=os.path.getsize(path)

        return(siz)

    def getPathSiz(self,path,pathopt='exit',verb=0):

        if(self.ChkPath(path,pathopt='noexit',verb=verb) != 1):
            siz=-999
        else:
            siz=os.path.getsize(path)

        return(siz)

    def getPathNlines(self,path,pathopt='exit',verb=0):

        if(self.ChkPath(path,pathopt='noexit',verb=verb) != 1):
            nlines=-999
        else:
            nlines=int(check_output(['wc', '-l', path]).split()[0])
            
        return(nlines)
    
    def getPathSiz(self,path,pathopt='exit',verb=0):

        if(self.ChkPath(path,pathopt='noexit',verb=verb) != 1):
            siz=-999
        else:
            siz=os.path.getsize(path)

        return(siz)

    def listTxtPath(self,path,ncprint=None):

        if(self.GetPathSiz(path) != None):
            cards=open(path).readlines()
            ncards=len(cards)
            if(ncprint != None):
                ncprint=min(ncprint,ncards)
            else:
                ncprint=ncards
            for n in range(0,ncprint):
                print cards[n][0:-1]



    def GetDirFilesSiz(self,dir,pathopt='exit',mask="*",verb=0):

        if(self.ChkPath(dir,pathopt='noexit',verb=verb) != 1):
            siz=None
        else:
            paths=glob.glob("%s/%s"%(dir,mask))
            siz=0
            for path in paths:
                fsiz=self.GetPathSiz(path)
                if(fsiz != None): siz=siz+fsiz

        return(siz)

    def GetNfilesDir(self,dir,mask="*"):
        files=glob.glob("%s/%s"%(dir,mask))
        return(len(files))

    def ChkDirOld(dir,diropt='verb'):
    
        if(dir == None):
            if(diropt != 'quiet'): print "dir      = None : "
            return(-2)
    
        if not(os.path.isdir(dir)) :
            if(diropt != 'quiet'): print "dir  (not there): ",dir
            if(diropt == 'mk' or diropt == 'mkdir'):
                try:
                    os.system('mkdir -p %s'%(dir))
                except:
                    print 'EEE unable to mkdir: ',dir,' in ChkDir, return -1 ...'
                    return(-1)
                print 'dir     (MADE): ',dir
                return(2)
            else:
                return(0)
        else:
            if(diropt == 'verb'):
                print "dir      (there): ",dir
            return(1)


    def ChkDir(self,ddir,diropt='verb'):
    
        if(ddir == None):
            if(diropt != 'quiet'): print "dir      = None : "
            return(-2)
    
        if not os.path.exists(ddir):
            
            if(diropt != 'quiet'): print "dir  (not there): ",ddir
            if(diropt == 'mk' or diropt == 'mkdir'):
        
                try:
                    os.makedirs(ddir)
                    print 'dir     (MADE): ',ddir
                    return(2)
                    
                except OSError as exception:
                    if exception.errno != errno.EEXIST:
                        raise
                        #print 'EEE unable to mkdir: ',dir,' in ChkDir, return -1 ...'
                        #return(-1)
                    else:
                        print "\nBE CAREFUL! Directory %s already exists." % path
        
            else:
                return(0)
            
        else:
            if(diropt == 'verb'):
                print "dir      (there): ",ddir
            return(1)

    def ChangeDir(self,ddir,verb=1,docurtime=0):

        dtgcurtime=''
        if(docurtime):  dtgcurtime=dtg('curtime')

        try:
            os.chdir(ddir)
            if(verb == 1): print 'cd---> ',ddir,dtgcurtime
            return(1)
        except:
            if(verb != -1): print 'WWW(MF.ChangeDir()) unable to cd to: ',ddir
            return(0)


    def ChkPath(self,path,pathopt='noexit',verb=0):

        if(path == None): return(0)

        if not(os.path.exists(path)) :
            if(verb): print "EEE(ChkPath): path: %s NOT there... "%(path)
            if(pathopt == 'exit'):
                print "EEE(ChkPath): Sayoonara..."
                sys.exit()
            else:
                return(0)
        else:
            return(1)


    def is0618Z(self,dtg):

        hh=dtg[8:10]
        rc=0
        if(hh == '06' or hh == '18'): rc=1
        return(rc)

    def is0012Z(self,dtg):

        hh=dtg[8:10]
        rc=0
        if(hh == '00' or hh == '12'): rc=1
        return(rc)

    def isSynopticHour(self,dtg,dtau=6):

        hh=int(dtg[8:10])
        rc=0
        remainder=hh%dtau
        if(remainder == 0): rc=1
        return(rc,remainder)

    def TimeZoneName(self):

        tz=time.tzname
        tz=tz[time.daylight]
        return(tz)

    def dtg(self,opt="default"):

        tzname=" %s "%(self.TimeZoneName())

        if (opt == "curtime" or opt == "curtimeonly" ):
            t=time.localtime(time.time())
        else:
            t=time.gmtime(time.time())

        yr="%04d" % t[0]
        mo="%02d" % t[1]
        dy="%02d" % t[2]
        hr="%02d" % t[3]
        fhr="%02d" % (int(t[3]/6)*6)
        phr=int(t[3])%6
        mn="%02d" % t[4]
        sc="%02d" % t[5]
        fphr=float(phr)*1.0 + float(mn)/60.0;

        if opt == "default":
            dtg=yr + mo + dy + fhr
        elif opt == "phr":
            dtg="%4.2f"%(fphr)
        elif opt == "fphr":
            dtg=fphr
        elif opt == "dtg.hm":
            dtg=yr + mo + dy + fhr + " " + hr + ":" + mn
        elif opt == "dtg.phm":
            cphr="%02d"%(phr)
            dtg=yr + mo + dy + fhr + " " + cphr + ":" + mn
        elif opt == "dtgmn":
            dtg=yr + mo + dy +  hr + mn
        elif opt == "dtg_ms":
            dtg=yr + mo + dy +  hr + "_%s_%s"%(mn,sc)
        elif opt == "dtg_hms":
            dtg=yr + mo + dy + "_%s_%s_%s"%(hr,mn,sc)
        elif opt == "dtg.hm":
            dtg=yr + mo + dy + fhr + " " + hr + ":" + mn
        elif opt == "dtg.hms":
            dtg=yr + mo + dy +  " " + hr + ":" + mn + ":" + sc
        elif opt == "dtgcurhr":
            dtg=yr + mo + dy + hr
        elif (opt == "timeonly"):
            dtg=hr+":"+mn+":"+sc+ " UTC "
        elif (opt == "time"):
            dtg=hr+":"+mn+":"+sc+ " UTC " + str(t[2]) + " " + mname[mo] + ", " + yr
        elif (opt == "curtime"):
            dtg=hr+":"+mn+":"+sc+ tzname + str(t[2]) + " " + mname[mo] + ", " + yr
        elif (opt == "curtimeonly"):
            dtg=hr+":"+mn+":"+sc+ tzname
        else:
            dtg=yr + mo + dy + fhr + " " + hr + ":" + mn

        return(dtg)

    def dtg2time(self,dtg):

        cdtg=str(dtg)

        yy=int(cdtg[0:4])
        mm=int(cdtg[4:6])
        dd=int(cdtg[6:8])
        hh=int(cdtg[8:10])

        ct=(yy,mm,dd,hh,0,0,0,0,0)
        time=mktime(ct)
        return(time)

    def dtg2YMDH(self,dtg):

        cdtg=str(dtg)

        yy=cdtg[0:4]
        mm=cdtg[4:6]
        dd=cdtg[6:8]
        hh=cdtg[8:10]

        return(yy,mm,dd,hh)
    
    def dtg2ISODateTime(self,dtg):
        (yy,mm,dd,hh)=self.dtg2YMDH(dtg)
        isodate="%s-%s-%s"%(yy,mm,dd)
        isohour="%02d:00:00"%(int(hh))
        return(isodate,isohour)
        


    def DtgDiff(self,dtg1,dtg2):

        dtg1=str(dtg1)
        dtg2=str(dtg2)

        yyyy1=int(dtg1[0:4])
        yyyy2=int(dtg2[0:4])

        offyear=1981
        if(yyyy1%4==0):
            offyear=1980
        if(yyyy2%4==0):
            offyear=1979

        # override leaping if 365 day calendar
        #
        if(self.calendar == '365day'): offyear=1981

        #
        # 20030828 -- fix crossing year if offsetting
        #

        dyyyy=yyyy2-yyyy1

        if(yyyy1 < offyear or yyyy2 < offyear):
            dtg1off=offyear-int(dtg1[0:4])
            dtg1="%04d"%(offyear)+dtg1[4:10]
            dtg2="%04d"%(offyear+dyyyy)+dtg2[4:10]

        t1=self.dtg2time(dtg1)
        t2=self.dtg2time(dtg2)
        nhr=(t2-t1)*self.sec2hr

        return(nhr)

    def DiffDtgHms(self,dtghms1,dtghms2):
        """ diff of dtghms2 (2nd arg) - dtghms1"""
        ymd1=dtghms1.split()[0]
        y1=ymd1[0:4]
        #ndy1=self.nDayYear(y1) -- constant length of year
        ndy1=365.0
        jday1=self.Dtg2JulianDay(ymd1)
        (hh1,mm1,ss1)=dtghms1.split()[1].split(':')
        ymdh1=(float(y1)*float(ndy1) + float(jday1))*24.0 + int(hh1)*1.0 + int(mm1)/60.0 + int(ss1)/3600.0
        #print '11111111111 ',y1,ndy1,ymd1,hh1,mm1,ss1,ymdh1

        ymd2=dtghms2.split()[0]
        y2=ymd2[0:4]
        #ndy2=self.nDayYear(y2)
        ndy2=ndy1
        jday2=self.Dtg2JulianDay(ymd2)
        (hh2,mm2,ss2)=dtghms2.split()[1].split(':')
        
        ymdh2=(float(y2)*float(ndy2) + float(jday2))*24.0 + int(hh2)*1.0 + int(mm2)/60.0 + int(ss2)/3600.0
        #print '22222222222 ',y2,ndy2,ymd2,hh2,mm2,ss2,ymdh2
        diff=ymdh2-ymdh1
        #print 'ddddddddddd ',diff

        return(diff)



    def YearRange(self,byear,eyear=None,inc=1):

        def yearinc(year,inc):
            nyear=int(year)+inc
            return(nyear)

        if(eyear == None):
            eyear=byear

        years=[]

        byear=int(byear)
        eyear=int(eyear)

        year=byear

        while(year<=eyear):
            years.append(year)
            year=yearinc(year,inc)

        return(years)


    def makeDtgsString(self,dtgs,msiz=1024,osiz=132,ndtg=10):
        """ clean up list of dtgs"""

        #card=str(dtgs)[0:msiz].replace(', ','').replace("""''""",' ').replace("""['""",'').replace("""']""",'')
        #
        #if(len(card) > osiz):
        #    card=card[0:osiz]
        #    card=card+'...'



        nend=len(dtgs)
        card='N: %4d  dtgs: '%(nend)
        if(nend == 0): return(card)
        if(len(dtgs) >= ndtg): nend=ndtg/2

        for dtg in dtgs[0:nend]:
            card=card+dtg+' '


        if(len(dtgs) >= ndtg):
            card=card+'... '
            for dtg in dtgs[(len(dtgs)-ndtg/2):]:
                card=card+dtg+' '

        return(card)


    def setDirFromHash(self,ss,n):

        sbdir=''
        for sb in ss[0:len(ss)-n]:
            sbdir="%s/%s"%(sbdir,sb)
        sbdir=sbdir.replace('//','/')

        return(sbdir)



#tttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt
# time
#

    def rhh2hhmm(hh):

        if(hh < 0):
            rhh=abs(hh)
            lt0=1
        else:
            rhh=hh
            lt0=0

        imm=int(rhh*60.0+0.5)
        ihh=imm/60
        imm=imm%60
        if(lt0):
            ohhmm="-%02d:%02d"%(ihh,imm)
        else:
            ohhmm="+%02d:%02d"%(ihh,imm)

        return(ohhmm)


    #uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu
    # utilities

    def loadDictList(self,dict,key,value):
        try:
            dict[key].append(value)
        except:
            dict[key]=[]
            dict[key].append(value)


    def uniqDictList(self,tdict):

        kk=tdict.keys()

        for k in kk:
            tlist=tdict[k]
            tlist=uniq(tlist)
            tdict[k]=tlist
            
        return(tdict)

    def uniqDict2List(self,ddict):
    
        kk1=ddict.keys()
        
        for k1 in kk1:
            kk2=ddict[k1].keys()
            
            for k2 in kk2:
                dlist=ddict[k1][k2]
                dlist=uniq(dlist)
                ddict[k1][k2]=dlist

    def uniqDictDict(self,dict):
        """ uniq a dict of dicts"""
        kk=dict.keys()

        for k in kk:
            dict2=dict[k]
            kk2=dict2.keys()
            self.uniqDictList(dict2)
            dict[k]=dict2
            
        return(dict)



    def addList2DictList(self,dict,key,list):
        try:
            dict[key]=dict[key]+list
        except:
            dict[key]=list


    def appendList(self,list,value):

        try:
            list.append(value)
        except:
            list=[]
            list.append(value)

    def appendDictList(self,dict,key,value):

        try:
            dict[key].append(value)
        except:
            dict[key]=[]
            dict[key].append(value)

    def append2KeyDictList(self,dict,key1,key2,value):

        try:
            dict[key1][key2].append(value)

        except:

            try:
                dict[key1][key2]
            except:
                try:
                    dict[key1]
                except:
                    dict[key1]={}

            dict[key1][key2]=[]
            dict[key1][key2].append(value)

    def set2KeyDictList(self,dict,key1,key2,value):

        try:
            dict[key1][key2]=value

        except:

            try:
                dict[key1][key2]
            except:
                try:
                    dict[key1]
                except:
                    dict[key1]={}

            dict[key1][key2]=value


    def append3KeyDictList(self,dict,key1,key2,key3,value):

        try:
            dict[key1][key2][key3]=value
        except:
            try:
                dict[key1][key2]={}
                dict[key1][key2][key3]=value
            except:
                dict[key1]={}
                dict[key1][key2]={}
                dict[key1][key2][key3]=value



    def append2TupleKeyDictList(self,dict,key1,key2,value):

        try:
            dict[key1,key2].append(value)
        except:
            dict[key1,key2]=[]
            dict[key1,key2].append(value)


    def append3TupleKeyDictList(self,dict,key1,key2,key3,value):

        try:
            dict[key1,key2,key3].append(value)

        except:
            dict[key1,key2,key3]=[]
            dict[key1,key2,key3].append(value)



    def DictTr(self,dic):
        dict={}
        kk=dic.keys()
        for k in kk:
            val=dic[k]
            try:
                dict[val].append(k)
            except:
                dict[val]=[]
                dict[val].append(k)

        return(dict)

    def DictAdd(self,dic1,dic2,priority=2):
        dic={}
        kk1=dic1.keys()
        kk2=dic2.keys()
        kk=kk1+kk2
        kk.sort()
        kk=self.uniq(kk)

        for k in kk:

            hk1=dic1.has_key(k)
            hk2=dic2.has_key(k)

            if(hk1 and hk2):
                if(priority == 2):
                    dic[k]=dic2[k]
                else:
                    dic[k]=dic1[k]

            elif(hk1 and not(hk2)):
                dic[k]=dic1[k]
            elif(not(hk1) and hk2):
                dic[k]=dic2[k]
            else:
                print 'EEE DicAdd'
                sys.exit()

        return(dic)


    def uniqDict(self,dict):
        tt={}
        for kk in dict.keys():
            dd=dict[kk]
            dd=self.uniq(dd)
            tt[kk]=dd
        return(tt)

    def Dic2list(self,dic,ne):
        kk=dic.keys()
        kk.sort()

        list=[]
        for k in kk:
            list.append(dic[k][ne])

        return(list)


    def List2Dict(self,dic,list,ne):

        kk=dic.keys()
        kk.sort()

        for i in range(0,len(kk)):
            dic[kk[i]][ne]=list[i]

        return

    def List2String(self,ilist):

        ostring='\n'.join(ilist)
        ostring=ostring+'\n'
        return(ostring)
    
    def setList2String(self,ilist):
                
        lstring=''
        
        for n in range(0,len(ilist)):
            im=ilist[n]
            lstring=lstring+'%s'%(im)
            if(n < len(ilist)-1):
                lstring=lstring+','
            if(n > 0):
                lstring=lstring+' '
        return(lstring)
                

    def PrintDict(self,dict,name='dict'):

        cards=[]
        kk=dict.keys()
        kk.sort()
        nh=len(dict)

        # -- case of empty dict
        #
        if(len(kk) == 0):
            print 'WWW MF.PrintDict dict={} ... return cards=[]'
            return(cards)

        if(isinstance(kk[0],tuple)):   nk=len(kk[0])
        else:                          nk=1

        card="%s %d %d"%(name,nk,nh)
        cards.append(card)

        for k in kk:
            card=''
            if(isinstance(k,tuple)):
                for n in k:
                    card=card+' '+n
            else:
                card=card+' '+k
            card=card+' : '
            for n in dict[k]:
                card=card+' '+str(n)
            cards.append(card)

        return(cards)



    def WriteString2File(self,string,path,verb=0,warnonly=1):

        try:
            c=open(path,'w')
        except:
            print "EEE unable to open (MF.WriteString2File): %s"%(path)
            if(not(warnonly)): sys.exit()
            return

        if(verb): print "CCC creating path: %s"%(path)
        c.writelines(string)
        c.close()
        return


    def WriteList2File(self,list,path,verb=0,warnonly=1):

        try:
            c=open(path,'w')
        except:
            print "EEE unable to open path(MF.WriteList2File): %s"%(path)
            if(not(warnonly)): sys.exit()
            return

        if(verb): print "CCC creating path: %s"%(path)
        for card in list:
            rcard=card.rstrip()
            if(verb): print rcard
            rcard=rcard+'\n'
            c.writelines(rcard)
        c.close()
        return


    def WriteList2Path(self,dlist,path,append=0,verb=0,warnonly=1):

        try:
            if(append):
                c=open(path,'a')
            else:
                c=open(path,'w')
        except:
            print "EEE unable to open path(MF.WriteList2File): %s"%(path)
            if(not(warnonly)): sys.exit()
            return

        if(verb): print "CCC creating path: %s"%(path)
        for card in dlist:
            if(verb): print card
            card=card.rstrip()+'\n'
            c.writelines(card)
        c.close()
        return

    def WriteString2Path(self,string,path,verb=0,warnonly=1):

        self.WriteString2File(string,path,verb=verb)

        return


    def WriteHash2File(self,hash,path,verb=0):

        keys=hash.keys()
        keys.sort()

        O=open(path,'w')
        for key in keys:
            O.writelines(hash[key]+'\n')

        O.close()



    def ReadFile2List(self,path,verb=0):

        try:
            list=open(path,'r').readlines()
        except:
            print "EEE(ReadFile2List) unable to open path: %s"%(path)
            return(None)

        return(list)


    def ReadFile2String(self,path,verb=0):

        string=''
        try:
            list=open(path,'r').readlines()
        except:
            print "EEE(ReadFile2String) unable to open path: %s"%(path)
            return(string)

        for tt in list:
            if(verb): print tt
            string=string+str(tt)
        return(string)


    def WriteCtl(self,ctl,ctlpath,verb=0):

        try:
            c=open(ctlpath,'w')
        except:
            print "EEE unable to open: %s"%(ctlpath)
            sys.exit()

        if(verb): print "CCCC creating .ctl: %s"%(ctlpath)
        c.writelines(ctl)
        c.close()
        return


    def PrintList(self,list,verb=0):

        for card in list:
            print card


    def sumList(self,list):
        if(list == None):
            sum=None
        else:
            sum=0.0
            for l in list:
                sum=sum+float(l)
        return(sum)


    # --- fundamentals
    #

    def uniq(self,list):
        weirdtest='asdasdfasdfasdfasdf'
        #
        # sort before length check for case of two
        #
        list.sort()
        rlist=[]

        if(len(list) > 2):
            test=list[1]
            test=weirdtest
        elif(len(list) == 0):
            return(rlist)
        else:
            test=list[0]

        if(test != weirdtest):
            rlist.append(test)

        for l in list:
            #if(repr(l) != repr(test)):
            if(l != test):
                rlist.append(l)
                test=l
        return(rlist)


    def find(self,mystr,pattern):
        rc=0
        if(mystr.find(pattern) != -1): rc=1
        return(rc)



    def h2hm(self,age):

        fh=int(age)*1.0
        im=int( (age-fh)*60.0+0.5 )
        if(im == 60):
            fh=fh+1.0
            im=0

        cage="%4.0f:%02d"%(fh,im)
        return(cage)


    def min2minsec(self,min):

        fm=int(min)*1.0
        im=int( (min-fm)*60.0+0.5 )
        if(im == 60):
            fm=fm+1.0
            im=0

        cmin="%4.0f:%02d"%(fm,im)
        return(cmin)



    def runcmdLog(self,cmd,ropt='',quiet=0,printCmd='runcmdLog'):

        if(ropt == 'norun'):
            print "CCC(%s): %s"%(printCmd,cmd)
            return([])
        else:
            if(not(quiet)): print "CCC(%s): %s"%(printCmd,cmd)
            p=Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
            output = p.stdout.read()
            lines=output.split('\n')

        return(lines)


    def runcmdLogOutput(self,cmd,ropt='',quiet=0):

        if(ropt == 'norun' or not(quiet)): print "CCC(runcmdLog): %s"%(cmd)

        if(ropt == 'norun'):
            return([])
        else:
            p=Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
            output = p.stdout.read()

        return(output)



    def runcmd(self,command,logpath='straightrun',lsopt=''):

        if(logpath == ''):
            logpath='straightrun'

        if(logpath == 'straightrun' or logpath == 'norun'):
            if(lsopt != 'q'): print "CCC: %s"%command
            if(logpath != 'norun'): os.system(command)
            return

        if(logpath == 'quiet'):

            tt=command.split()
            mycmd=tt[0]
            myarg=''
            if(len(tt) > 1):
                for t1 in tt[1:]:
                    myarg="%s %s"%(myarg,t1)

            #p=Popen([mycmd,myarg], stdout=PIPE)
            #(o,e)=p.communicate()

            rc=os.popen(command).readlines()
            return(rc)

        global LF

        #
        # output to log file (append and add title line)
        #

        if(logpath != 'nologpath'):

            log=getCommandOutput2(command)

            lout="\nTTT: %s  :: CCC: %s\n\n"%(dtg6 ('curtime'),command)
            lout=lout+log

            if(not(os.path.exists(logpath))):
                try:
                    LF=open(logpath,'a')
                    LF.writelines(lout)
                    LF.flush()
                except:
                    print 'EEE(runcmd): unable to open logpath: %s'%(logpath)
                    return
            else:
                try:
                    LF.writelines(lout)
                    LF.flush()
                except:
                    try:
                        LF=open(logpath,'a')
                        LF.writelines(lout)
                        LF.flush()
                    except:
                        LF.writelines(lout)
                        LF.flush()
                        print 'EEE(runcmd): unable to write to logpath: %s'%(logpath)
                        return

        #
        # output to terminal
        #

        else:

            log=getCommandOutput2(command)

            print "CCC(log): %s\n"%command
            print log

        return

    def runcmdRetry(self,cmd,ropt='',nTry=0,nTryMax=3,trySleep=5,
                    errorString='error',printCmd='runcmdRetry'):

        rsyncOK=1
        rc=0
        output=self.runcmdLog(cmd,ropt,printCmd=printCmd)
        for o in output:
            print o
            if(find(o,errorString)): rsyncOK=0

        if(rsyncOK == 0): 
            nTry=1
        elif(rsyncOK):
            rc=1
            return(rc)

        while(nTry <= nTryMax):
            rsyncOK=1
            print
            print "IIIIIIII--------------------------retry cmd:",cmd, "ntry: ",nTry,' nTryMax: ',nTryMax
            print
            time.sleep(trySleep)  

            output=self.runcmdLog(cmd,ropt,printCmd=printCmd)
            for o in output:
                print o
                if(find(o,errorString)): rsyncOK=0

            if(rsyncOK):
                nTry=nTryMax+1
                rc=1
            else:
                nTry=nTry+1
                rc=0

        return(rc)



    def get0012fromDtgs(self,dtgs):

        odtgs=[]
        for dtg in dtgs:
            hh=int(dtg[8:10])
            if(hh == 12 or hh == 0): odtgs.append(dtg)

        return(odtgs)



    def chkIfJobIsRunningOld(self,job,jobopt=None,killjob=1,verb=1,incron=0,nminWait=10,timesleep=5):

        """20120209 -- set killjob=1, if both hit it at the same time, will be stuck"""

        curpid=os.getpid()


        def isRunning(job,jobopt,killjob):

            pids=LsPids()

            rc=0
            for pid in pids:
                cpid=pid[0]
                prc=str(pid[2])
                jobchk=find(prc,job)

                if(jobopt != None):  joboptchk=find(prc,jobopt)
                else:                joboptchk=1

                if(jobchk and joboptchk and cpid != curpid):
                    #if(incron and not(find(prc,'tcsh'))): continue
                    # -- bypass any proc with tcsh -- means in cron(?)
                    ctime=dtg('curtime')
                    if(find(prc,'tcsh') or find(prc,'/bin/sh -c')): continue
                    print 'isRunning...cpid:',cpid,'curpid: ',curpid,'prc: ',prc,'aaaaaaaaaaaaafter tcsh check',killjob
                    rc=rc+1

                    if(killjob):
                        print 'KKKKKKKKKKK killing this job since a previous instance is already running....'
                        cmd="kill %s"%(curpid)
                        runcmd(cmd,'')

            return(rc)

        timesleepmax=nminWait*60
        nmaxsleep=(timesleepmax/timesleep)+1

        rc=0
        osname=os.name

        if(not(find(osname,'posix'))):
            print 'WWW chkIfJobIsRunning is not supported on this OS: ',osname,' rc=0 (file not open)'
            return(rc)

        # -- check if *TWO* or more instances running, the first is the current, but that is checked above...
        if(nminWait > 0 and isRunning(job,jobopt,killjob) >= 1):
            nsleep=0
            while(nsleep < (nmaxsleep-1) and isRunning(job,jobopt,killjob) > 1 ):
                print 'SSSleeping in chkIfJobIsRunning nsleep: ',nsleep,' total sleeptime: ',nsleep*timesleep
                time.sleep(timesleep)
                nsleep=nsleep+1
                if(nsleep == (nmaxsleep-1)):
                    print '!!!! -- waited nminWait: ',nminWait
                    print 'EEEE'
                    print 'EEEE chkIfJobIsRunning...job:',job,'jobopt:',jobopt,'still running...'
                    print 'EEEE'
                    print '!!!! -- sayoonara'
                    sys.exit()

            rc=0

        else:
            rc=isRunning(job,jobopt,killjob)
            if(verb): print 'chkIfJobIsRunning rc: ',rc

        return(rc)


    def whoIsRunningNew(self,job,jobopt=None,killjob=0,rcPid=0):
        """ 
20210624 -- better version of isRunning because of switch to bash from tcsh
looks for all instances of the job first to set the code

"""
        cpidOut=-999
        rc=0

        runPids=findPyPids(job)
        nrunPids=len(runPids)
        
        for runp in runPids:
            print runp
            
        # -- if only one return 0 to not cycle
        #
        if(nrunPids == 1):
            (cpid,opid,prc,ptime)= runPids[0]
            return(0)
        
        if(nrunPids > 1):

            jobchk=1
            (curpid,opid,curprc,ptime)=runPids[-1]

            for (cpid,opid,prc,ptime) in runPids:
            
                if(jobopt != None):
                    try:
                        prcjobopt=prc.split()[2:]
                    except:
                        prcjobopt=None

                    if(prcjobopt != None):
                        prcjoboptS=''
                        for pp in prcjobopt:
                            prcjoboptS='%s %s'%(prcjoboptS,pp)

                        if(joboptchkType == 'find'): 
                            joboptchk=find(prcjoboptS,jobopt)
                        else:
                            joboptchk=(prcjoboptS == jobopt)
                else:
                    joboptchk=1
                    
                print 'jjjjjjjjjjjjjjjj',prc,cpid,curpid
                if(jobchk and joboptchk and cpid != curpid):

                    ctime=dtg('curtime')
                    print 'M.chkIfJobIsRunning.isRunning...curpid: ',curpid,'cpid: ',cpid,' prc: ',prc,'job: ',job,'jobopt: ',jobopt
                    cpidOut=cpid
                    rc=rc+1

                    kropt='quiet'
                    kropt='norun'
                    kropt=''
                    # -- do the killing inside whoIsRunning
                    #
                    if(killjob == 1):
                        print 'M.chkIfJobIsRunning KKKKK killing this job since a previous instance is already running....curpid: ',curpid,' job,jobopt ',job,jobopt
                        cmd="kill %s"%(curpid)
                        runcmd(cmd,kropt)
                    elif(killjob == -1):
                        print 'M.chkIfJobIsRunning OOOOO killing previous instance: ',cpid,'vice this one: ',curpid
                        cmd="kill %s"%(cpid)
                        runcmd(cmd,kropt)

        if(rc > 0 and rcPid): rc=cpidOut
        
        return(rc)




    def chkRunning(self,pyfile,setJobopt=None,strictChkIfRunning=0,verb=0,killjob=0,
                   timesleep=5,nminWait=5):
        
        """ big and complete check
"""
    # -- get command line vars, except -N
        pyfileopt=''
        for s in sys.argv[1:]:
            if(s != '-N'):
                pyfileopt='%s %s'%(pyfileopt,s)
    
        jobopt=pyfileopt.split()[0]
        # -- if very sctrict check -- any instance of pyfile
        if(strictChkIfRunning): jobopt=None
        
        if(setJobopt != None): jobopt=setJobopt
        
        if(verb): self.sTimer('chkIfJobIsRunning pyfile: %s jobopt: %s killjob: %s'%(pyfile,jobopt,killjob))
        rc=self.chkIfJobIsRunning(pyfile,jobopt=jobopt,killjob=killjob,verb=verb,nminWait=nminWait,
                                  timesleep=timesleep)
        if(verb): self.dTimer('chkIfJobIsRunning pyfile: %s jobopt: %s killjob: %s'%(pyfile,jobopt,killjob))
        
        return(rc)



    def chkIfJobIsRunning(self,job,jobopt=None,killjob=1,verb=0,incron=0,
                          nminWait=10,timesleep=5,rcPid=0,
                          # -- two types of joboptchk finding the jobopt string in prc or must be equal to jobopt
                          joboptchkType='find'):

        """20120209 -- set killjob=1, if both hit it at the same time, will be stuck"""

        curpid=os.getpid()

        def isRunning(job,jobopt,killjob,rcPid=0):

            pids=LsPids()
            cpidOut=-999

            pids=uniq(pids)
            pids.sort()

            rc=0
            for pid in pids:
                cpid=pid[0]
                prc=str(pid[2]).strip()

                # -- uninteresting procs
                #
                if(find(prc,'[') and find(prc,']') or find(prc,'/dev/tty') or find(prc,'-tcsh') or find(prc,'-bash') or
                   find(prc,'/usr') or find(prc,'vmhgfs') or
                   find(prc,'sbin') or find(prc,'automount') or find(prc,'crond') or find(prc,'sshd')): continue

                jobchk=find(prc,job)

                if(verb): print 'M.chkIfJobIsRunning() jobchk ',jobchk,'prc:',prc,'job: ',job,jobopt
                if(jobopt != None):

                    # -- 20120326 new/better logic to check if exact job running
                    # -- 20131127 -- even better checks whole cmd line arg
                    #
                    if(jobchk):
                        try:
                            prcjobopt=prc.split()[2:]
                        except:
                            prcjobopt=None

                        if(prcjobopt != None):
                            prcjoboptS=''
                            for pp in prcjobopt:
                                prcjoboptS='%s %s'%(prcjoboptS,pp)

                        if(joboptchkType == 'find'): 
                            joboptchk=find(prcjoboptS,jobopt)
                        else:
                            joboptchk=(prcjoboptS == jobopt)

                else:
                    joboptchk=1
                    

                if(jobchk and joboptchk and cpid != curpid):
                    #if(incron and not(find(prc,'tcsh'))): continue
                    # -- bypass any proc with tcsh -- means in cron(?)
                    ctime=dtg('curtime')
                    if(find(prc,'tcsh') or find(prc,'/bin/sh -c')): continue
                    print 'M.chkIfJobIsRunning.isRunning...curpid: ',curpid,'cpid, prc: ',cpid,prc,' job,jobopt',job,jobopt
                    cpidOut=cpid
                    rc=rc+1

                    if(killjob == 1):
                        print 'M.chkIfJobIsRunning KKKKK killing this job since a previous instance is already running....curpid: ',curpid,' job,jobopt ',job,jobopt
                        cmd="kill %s"%(curpid)
                        runcmd(cmd,'quiet')
                    elif(killjob == -1):
                        print 'M.chkIfJobIsRunning OOOOO killing previous instance: ',cpid,'vice this one: ',curpid
                        cmd="kill %s"%(cpid)
                        runcmd(cmd,'quiet')

            if(rc > 0 and rcPid): rc=cpidOut
            return(rc)



        def whoIsRunning(job,jobopt,killjob,rcPid=0):
            """ 
20210624 -- better version of isRunning because of switch to bash from tcsh
looks for all instances of the job first to set the code

"""

            pids=LsPids()
            cpidOut=-999

            pids=uniq(pids)
            pids.sort()
            
            runPids=[]
            # -- rc is the number of jobs
            rc=0
            for pid in pids:
                cpid=pid[0]
                prc=str(pid[2]).strip()
                # -- look for non cron jobs
                if(find(prc,job)):
                    if(find(prc,'cron')): continue
                    runPids.append((prc,cpid))

            nrunPids=len(runPids)
            
            # -- if only one return 0 to not cycle
            #
            if(nrunPids == 1):
                (prc,cpid)= runPids[0]
                return(0)
                
            if(nrunPids > 1):

                jobchk=1
                (curprc,curpid)=runPids[-1]

                for (prc,cpid) in runPids:
                
                    if(jobopt != None):
                        try:
                            prcjobopt=prc.split()[2:]
                        except:
                            prcjobopt=None
    
                        if(prcjobopt != None):
                            prcjoboptS=''
                            for pp in prcjobopt:
                                prcjoboptS='%s %s'%(prcjoboptS,pp)
    
                            if(joboptchkType == 'find'): 
                                joboptchk=find(prcjoboptS,jobopt)
                            else:
                                joboptchk=(prcjoboptS == jobopt)
                    else:
                        joboptchk=1
                        
                
                    if(jobchk and joboptchk and cpid != curpid):

                        ctime=dtg('curtime')
                        print 'M.chkIfJobIsRunning.isRunning...curpid: ',curpid,'cpid: ',cpid,' prc: ',prc,'job: ',job,'jobopt: ',jobopt
                        cpidOut=cpid
                        rc=rc+1
    
                        # -- do the killing inside whoIsRunning
                        #
                        if(killjob == 1):
                            print 'M.chkIfJobIsRunning KKKKK killing this job since a previous instance is already running....curpid: ',curpid,' job,jobopt ',job,jobopt
                            cmd="kill %s"%(curpid)
                            runcmd(cmd,'quiet')
                        elif(killjob == -1):
                            print 'M.chkIfJobIsRunning OOOOO killing previous instance: ',cpid,'vice this one: ',curpid
                            cmd="kill %s"%(cpid)
                            runcmd(cmd,'quiet')

            if(rc > 0 and rcPid): rc=cpidOut
            
            return(rc)


        timesleepmax=nminWait*60
        nmaxsleep=(timesleepmax/timesleep)+1

        rc=0
        osname=os.name

        if(not(find(osname,'posix'))):
            print 'WWW M.chkIfJobIsRunning is not supported on this OS: ',osname,' rc=0 (file not open)'
            return(rc)

        # -- check if *TWO* or more instances running, the first is the current, but that is checked above...
        #
        rc=whoIsRunning(job,jobopt,killjob,rcPid=rcPid)
        if(verb): print '111111111111111111111111111 rc whoIsRunning: ',rc,'job: ',job,'jobopt: ',jobopt,' killjob: ',killjob
        
        # -- only cycle if not killjob...
        #
        if(nminWait > 0 and not(killjob) and rc >= 1 ):
            nsleep=0
            rc=whoIsRunning(job,jobopt,killjob,rcPid=0)
            if(verb): print '22222222222222222222222222222222222222 rc whoIsRunning: ',rc
            print 'M.chkIfJobIsRunning -- cycling rc: ',rc,' curtime: ',dtg('curtime')
            while(nsleep < (nmaxsleep-1) and rc >= 1 ):
                print 'SSSleeping in chkIfJobIsRunning nsleep: ',nsleep,' total sleeptime: ',nsleep*timesleep,' job,jobopt: ',job,jobopt
                time.sleep(timesleep)
                nsleep=nsleep+1
                if(nsleep == (nmaxsleep-1)):
                    print '!!!! -- waited nminWait: ',nminWait
                    print 'EEEE'
                    print 'EEEE chkIfJobIsRunning...job:',job,'jobopt:',jobopt,'still running...'
                    print 'EEEE'
                    print '!!!! -- sayoonara'
                    sys.exit()

                rc=isRunning(job,jobopt,killjob,rcPid=0)
                print 'M.chkIfJobIsRunning -- cycling rc: ',rc,' curtime: ',dtg('curtime')

            rc=0


        return(rc)




    def chkIfFileIsOpen(self,path,verb=0,nminWait=10,timesleep=5):

        def isOpen(path,verb=0):

            if(not(self.GetPathSiz(path) > 0)):
                print 'WWW in chkIfFileIsOpen: ',path,' does not exist or is 0 length'
                return(0)

            rc=0
            openpids=[]
            cmd="lsof %s"%(path)
            lines=self.runcmdLog(cmd)
            if(len(lines[0]) > 0):

                if(verb):
                    olines=lines[1:-1]
                    olines=uniq(olines)
                    for line in olines:
                        pid=line.split()[1]
                        openpids.append(pid)
                        print 'chkIfFileIsOpen: ',line

                rc=1

            return(rc,openpids)

        timesleepmax=nminWait*60
        nmaxsleep=(timesleepmax/timesleep)+1

        rc=0
        osname=os.name

        if(not(find(osname,'posix'))):
            print 'WWW chkIfFileIsOpen is not supported on this OS: ',osname,' rc=0 (file not open)'
            return(rc)

        if(nminWait > 0 and isOpen(path,verb=verb) ):
            nsleep=0
            while(nsleep < (nmaxsleep-1) and isOpen(path,verb=verb) ):
                print 'SSSleeping in chkIfFileIsOpen nsleep: ',nsleep,' total sleeptime: ',nsleep*timesleep
                time.sleep(timesleep)
                nsleep=nsleep+1
                if(nsleep == (nmaxsleep-1)):
                    print '!!!! -- waited nminWait: ',nminWait
                    print 'EEEE'
                    print 'EEEE chkIfFileIsOpen...path: ',path,'still open...'
                    print 'EEEE'
                    print '!!!! -- sayoonara'
                    sys.exit()

            rc=0

        else:
            rc=isOpen(path,verb=verb)
            if(verb): print 'chkIfFileIsOpen rc: ',rc

        return(rc)
    
    def loopCmd2(self,cmd,nLoop=5,sLoop=5,ropt='',verb=0):
        rc=runcmd2(cmd,ropt=ropt)
        if(ropt != 'norun' and verb): print '0000-loopCmd2-rc: ',rc
    
        if(rc < 0): 
            print 'EEEE rsync error GGGEEETTTIING INVentory...retry for %d times sleeping %d seconds..'%(nLoop,sLoop)
            for n in range(0,nLoop):
                sleep(sLoop)
                rc=runcmd2(cmd,ropt='')
                if(ropt != 'norun'): print '0000-runcmd2-rc: ',rc
                if(rc >= 0): 
                    return(rc)
        
        if(rc < 0):
            print 'bailing in loopCmd: ',cmd,'nLoop: ',nLoop,' sLoop: ',sLoop
            sys.exit()
        else:
            return(rc)


class DataSet(MFbase):

    from mfbase import ptmpBaseDir
    
    def __init__(self,
                 name='test',
                 version='0.1',
                 dtype='hash',
                 bdir=ptmpBaseDir,
                 unlink=0,
                 verb=0,
                 ):

        self.name=name
        self.version=version
        self.dtype=dtype
        self.bdir=bdir
        self.pyppath="%s/%s.pyp"%(self.bdir,self.name)
        if(unlink):
            try:
                os.unlink(self.pyppath)
            except:
                print 'WWW M.DataSet -- failed to unlink: ',self.pyppath
                
        self.data={}
        self.verb=verb

    def getPyp(self):

        if(self.verb):
            print 'M.DataSet(getPyp): pyppath: ',self.pyppath

        if(os.path.exists(self.pyppath)):
            if(self.verb):  print 'M.DataSet(getPyp): pyppath: ',self.pyppath
            try:
                PS=open(self.pyppath)
                FR=pickle.load(PS)
                PS.close()
                return(FR)
            except:
                print 'WWW M.DataSet.getPyp() error opening: ',self.pyppath,' returning None'
                return(None)

        else:
            return(None)


    def putPyp(self,override=0):


        if(ChkDir(self.bdir,'mk') == -1): sys.exit()

        if(override and os.path.exists(self.pyppath)):
            os.unlink(self.pyppath)
            self.curtime=[]


        if(not(hasattr(self,'curtime'))):
            self.curtime=[]

        self.curtime.append(dtg('dtg.phm'))

        try:
            if(self.verb):  print 'M.DataSet(putPyp): pyppath: ',self.pyppath
            PS=open(self.pyppath,'w')
            pickle.dump(self,PS)
            PS.close()
        except:
            print 'EEEEE unable to pickle.dump: ',self.pyppath
            sys.exit()


    def getData(self):

        return(self.data)



    def putData(self,key,value,verb=1,override=0):

        if(not(hasattr(self,'data'))):
            print 'IIII making data'
            self.data={}

        try:
            haskey=self.data.has_key(key)
        except:
            haskey=0

        try:
            lkey=len(self.data[key])
        except:
            lkey=0


        if(not(haskey) or override or ( lkey != len(value)) ):
            print 'PPPPP adding value to data[key]'
            self.data[key]=value

        else:
            if(verb):  print 'data for key: ',key,' already there'



class DataSets(DataSet):

    from mfbase import ptmpBaseDir

    def __init__(self,bdir=ptmpBaseDir,name='datasets',dtype='model',version='0.1',verb=0,backup=0,unlink=0,
                 unlinkWithRm=0,
                 docp1st=0,
                 doDSsWrite=0,
                 dowriteback=True,
                 doFileLock=0,
                 doMkdir=1,
                 warn=0,
                 chkifopen=0,nminWait=10):

        self.bdir=bdir
        self.name=name
        self.version=version
        self.dtype=dtype
        self.verb=verb
        self.docp1st=docp1st


        if(doDSsWrite and doMkdir):
            if(ChkDir(bdir,'mk') == -1): 
                print 'M.Datasets - cannot mkdir bdir: ',bdir,'bailing...'
                sys.exit()
        else:
            if(not(ChkDir(bdir,'quiet'))):
                print 'M.Datasets - doDSsWrite==0 bdir: ',bdir,'not there, bailing...'
                sys.exit()
                

        path=os.path.join(bdir,name)
        if(os.path.exists(path) and backup):
            cmd="cp %s %s.SAV"%(path,path)
            runcmd(cmd,'')
        elif(os.path.exists(path) and unlink):
            try:
                if(unlinkWithRm):
                    print 'III(M.DataSets rm -v): ',path
                    runcmd("rm -v %s"%(path),'')
                else:
                    # -- use .os to rm...
                    print 'III(M.DataSets unlinking): ',path
                    os.unlink(path)
            except:
                print 'III(M.DataSets unlinking): ',path,' failed because...'


        self.path=path
        self.pathCP=None

        from WxMAP2 import W2adminuSer,W2currentuSer,W2adminuSers

        if(self.docp1st):
            curpid=os.getpid()
            pathCP="%s-%d"%(path,curpid)
            cmd="cp %s %s"%(path,pathCP)
            runcmd(cmd,'')
            path=pathCP
            self.pathCP=pathCP
            print "III M.Dataset.__init__() docp1st from: %s to: %s"%(self.path,self.pathCP) 

        if(chkifopen):
            rc=MF.chkIfFileIsOpen(path,nminWait=nminWait,verb=verb)

        isDSsThere=os.path.exists(path)

        if(not(isDSsThere) and not(doDSsWrite)):
            if(warn): print 'WWW M.Dataset.__init_() -- path: ',path,' not there do not create shelve...doDSsWrite = 0'
            return

        if( ( (W2currentuSer == W2adminuSer) or (W2currentuSer in W2adminuSers) )  and doDSsWrite):

            if(doFileLock):
                self.db=sopen(path,flag='c',writeback=dowriteback)
            else:
                self.db=shelve.open(path,writeback=dowriteback)

        else:
            self.db=shelve.open(path,'r')

        if(verb): print 'DataSets.dbpath: ',path
        self.dbpath=path

    def putDataSet(self,dataset,key,
                   unlinkException=0,
                   verb=0,
                   doDbSync=0,
                   ):

        if(not(hasattr(dataset,'curdtghms'))):
            dataset.curdtghms=[]

        dataset.curdtghms.append(dtg('dtg.hms'))

        if(not(hasattr(self,'putKeys'))): self.putKeys=[]
        self.putKeys.append(key)

        try:
            self.db[key]=dataset
            if(doDbSync): self.db.sync()
            if(verb): print 'PPP putDataSet    putting key: ',key,'   to: %s/%s  dbsync: %d'%(self.bdir,self.name,doDbSync)
            return(0)
        except:
            if(unlinkException):
                print 'WWW killing ppath: ',self.dbpath,' on open/dump exception in putDataSet'
                os.unlink(self.dbpath)
            print 'PPP EEE(M.putDataSet() error in putting key: ',key,'   to: %s/%s'%(self.bdir,self.name)
            print 'PPP WWW press!'
            return(-1)


    def closeDataSet(self,verb=0,warn=0):
        if(hasattr(self,'db')):
            #self.db.sync()  -- not needed; done before close in shelve.py
            self.db.close()
            if(verb):
                print 'M.DataSets.closeDataSet() -- success'
        else:
            if(warn):
                print 'M.DataSets.closeDataSet() -- failed'

    def syncDataSet(self):
        if(hasattr(self,'db')):
            self.db.sync()     


    def getDataSet(self,key,override=0,verb=0,warn=1):

        if(override): return(None)

        try:
            self.db.has_key(key)
        except:
            if(warn): print 'EEE bad dataset in DataSets.getDataSet()...return None key: ',key
            return(None)

        if(self.db.has_key(key)):

            # return None if problem getting pyp from db...
            #pyp=self.db[key]
            #return(pyp)
            try:
                pyp=self.db[key]
                if(self.verb or verb): print 'GGG DataSets.getDataSet() getting key: ',key,' in: %s/%s'%(self.bdir,self.name)
            except:
                if(self.verb or verb): print 'EEE DataSets.getDataSet()     got key: ',key,' problem with unpickling in: %s/%s'%(self.bdir,self.name)
                pyp=None
            return(pyp)
        else:
            if(self.verb or verb): print 'GGG  DataSets.getDataSet()  NNNOOO key: ',key,' in: %s/%s'%(self.bdir,self.name)
            return(None)

    def lsKeys(self):

        kk=self.db.keys()
        kk.sort()
        for k in kk:
            print 'key: ',k

    def getKeys(self):

        kk=self.db.keys()
        kk.sort()
        return(kk)


#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# runGrads

class runGrads(MFutils):


    gradscmd='''grads -Hlc'''


    def __init__(self,files,gsprc='',verb=0,filetype=''):

        if(type(files) != ListType): files=[files]

        print 'files: ',files
        gs="""function main(args)
# prelims:

rc=gsfallow('on')
rc=const()"""

        gaopencmd='open'
        if(filetype == 'xdf'): gaopencmd='xdfopen'
        if(filetype == 'sdf'): gaopencmd='sdfopen'

        for file in files:
            gs="""%s
print 'opening: %s'
'%s %s'
"""%(gs,file,gaopencmd,file)

        gs="""%s
%s
"""%(gs,gsprc)


        gspath='/tmp/runGrads.gs'
        self.WriteString2File(gs,gspath)
        cmd='''%s "%s" -g 1024x768-30'''%(self.gradscmd,gspath)
        os.system(cmd)







#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# cmdline

class CmdLine(MFutils):

    def __init__(self,argv=sys.argv):

        self.argv=argv

        self.argopts={
            'dtgopt': 'no default',
            'model': 'no default',
        }

        self.options={
            'override':['O',0,1,'override'],
            'verb':['V',0,1,'verb=1 is verbose'],
            'ropt':['N','','norun',' norun is norun'],
            'source':['S:','rtfim','a','source'],
        }

        self.defaults={
            'zy0x1w2':0,
            'zy0x1w2y3':'test'
        }

        self.purpose='''
purpose -- to boldly go, where no man has gone before!'''

        self.examples='''
%s test
'''

    def initDoc(self):

        argdoc="%s "

        optdoc='''
plain args:'''
        for n in range(1,len(self.argopts)+1):
            key=self.argopts[n][0]
            val=self.argopts[n][1]
            argdoc="%s %s"%(argdoc,key)
            optdoc=optdoc+'''
  %-20s - %s'''%(key,val)



        argdoc=argdoc+' ['
        optdoc=optdoc+'''

switches:'''
        kk=self.options.keys()
        kk.sort()
        for k in kk:
            oo=self.options[k]
            argdoc="%s -%s"%(argdoc,oo[0][0])
            optdoc=optdoc+'''
  -%1s :: %s=[%s] %s'''%(oo[0][0],k,oo[1],oo[3])


        argdoc=argdoc+' ]'

        exampledoc="""
Example(s):%s"""%(self.examples)

        purposedoc="""
Purpose:%s"""%(self.purpose)

        self.__doc__="""%s
%s
%s
%s
"""%(argdoc,optdoc,purposedoc,exampledoc)



    def initFlagOpts(self):

        self.flagOpts=''
        vv=self.options.values()
        for v in vv:
            self.flagOpts=self.flagOpts+v[0]


    def initArgOpts(self):

        narg=len(self.argopts)

        if(narg == 0):
            estr="self.istart=%d"%(narg+1)
            exec(estr)
            return

        for n in range(1,narg+1):

            key=self.argopts[n][0]
            val=self.argopts[n][1]

            if(n == 1):
                estr="self.%s=self.argv[%d]"%(key,n)
                exec(estr)
                estr="self.istart=%d"%(n+1)
                exec(estr)
            else:
                exec("if(self.narg > %d): self.%s=self.argv[%d]"%(n-1,key,n))
                exec("self.istart=%d"%(n+1))


    def getFlagOpts(self):

        self.foptions={}
        for o, a in self.opts:
            for k in self.options.keys():
                oo=self.options[k]
                if(o == "-%s"%(oo[0][0])):
                    if(oo[2] == 'a'):
                        self.foptions[k]=a
                    elif(oo[2] == 'i'):
                        self.foptions[k]=int(a)
                    elif(oo[2] == 'f'):
                        self.foptions[k]=float(a)
                    else:
                        self.foptions[k]=oo[2]

        for k in self.options.keys():
            if(not(self.foptions.has_key(k))):
                self.foptions[k]=self.options[k][1]


    def setFlagOpts(self):

        self.estrFlag=''
        for k in self.foptions.keys():
            if(type(self.foptions[k]) == StringType):
                estr="%s='%s'"%(k,self.foptions[k])
            elif(type(self.foptions[k]) == IntType):
                estr="%s=%d"%(k,self.foptions[k])
            elif(type(self.foptions[k]) == FloatType):
                estr="%s=%g"%(k,self.foptions[k])
            elif(self.foptions[k] == None):
                estr="%s=None"%(k)
            else:
                print 'EEE invalid option in ',__class__
                sys.exit()
            estrcl="self.%s"%(estr)
            exec(estrcl)
            self.estrFlag="%s%s\n"""%(self.estrFlag,estr)


    def setArgOpts(self):

        self.estrArg=''
        istart=1
        for n in range(1,len(self.argopts)+1):
            key=self.argopts[n][0]
            try:
                exec("kk=self.%s"%(key))
            except:
                print "!!!!"
                print "!!!!EEE CmdLine.setArgOpts: need to set the plain arg n: ",n,' key: ',key,' !!!!'
                print "!!!!"
                usage(self.__doc__,self.pyfile,self.curdtg,self.curtime)
                sys.exit()
            estr="%s='%s'"%(key,kk)
            estrcl="self.%s"%(estr)
            exec(estrcl)
            self.estrArg="%s%s\n"""%(self.estrArg,estr)


    def setDefaults(self):

        self.estrDefaults=''
        try:
            self.defaults.keys()
        except:
            return
        for k in self.defaults.keys():
            if(type(self.defaults[k]) == StringType):
                estr="%s='%s'"%(k,self.defaults[k])
            elif(type(self.defaults[k]) == IntType):
                estr="%s=%d"%(k,self.defaults[k])
            elif(type(self.defaults[k]) == FloatType):
                estr="%s=%g"%(k,self.defaults[k])
            elif(self.defaults[k] == None):
                estr="%s=None"%(k)
            else:
                print 'EEE invalid option in ',__class__
                sys.exit()
            estrcl="self.%s"%(estr)
            exec(estrcl)
            self.estrDefaults="%s%s\n"""%(self.estrDefaults,estr)

    def CmdLine(self,blankPlainArgs=0):

        self.blankPlainArgs=blankPlainArgs

        self.initFlagOpts()
        self.initDoc()

        self.curpid=os.getpid()
        self.curdtg=dtg()
        self.curphr=dtg('phr')
        self.curdir=os.getcwd()
        self.curyear=self.curdtg[0:4]
        self.curtime=dtg('curtime')

        (self.tttdtg,self.curphr)=dtg_phr_command_prc(self.curdtg) 

        self.pypath=self.argv[0]
        self.abspypath=os.path.abspath(self.pypath)
        (self.pydir,self.pyfile)=os.path.split(self.abspypath)

        self.estrCur="""curdtg='%s'\ncurphr='%s'\ncuryear='%s'\ncurtime='%s'\ncurdir='%s'\n"""%(self.curdtg,
                                                                                                self.curphr,
                                                                                                self.curyear,
                                                                                                self.curtime,
                                                                                                self.curdir,
                                                                                                )

        self.estrCur="""%s\npydir='%s'\npypath='%s'\npyfile='%s'\n"""%(self.estrCur,self.pydir,self.pypath,self.pyfile)

        gspath=os.path.abspath(self.pypath)
        (base,ext)=os.path.splitext(gspath)
        self.gspath=base+'.gs'

        self.narg=len(self.argv)-1

        if(self.narg >= 1 and not(self.blankPlainArgs)):

            self.initArgOpts()

            try:
                (self.opts, self.args) = getopt.getopt(self.argv[self.istart:], self.flagOpts)

            except getopt.GetoptError, e:
                usage(self.__doc__,self.pyfile,self.curdtg,self.curtime)
                print
                print "EEE"
                print """EEE invalid getopt opt error: '%s'"""%(e)
                print "EEE"
                print
                sys.exit(2)

            self.getFlagOpts()
            self.setFlagOpts()
            self.setArgOpts()
            self.setDefaults()
            self.estr=self.estrFlag+self.estrDefaults+self.estrArg+self.estrCur



        # -- 20111023 -- tried allowing blank plain args -- need to rewrite the whole section
        #

        elif(self.blankPlainArgs):


            self.initArgOpts()

            try:
                (self.opts, self.args) = getopt.getopt(self.argv[self.istart:], self.flagOpts)

            except getopt.GetoptError:
                usage(self.__doc__,self.pyfile,self.curdtg,self.curtime)
                print "EEE invalid getopt opt"
                sys.exit(2)


            self.getFlagOpts()
            self.setFlagOpts()
            self.setArgOpts()
            self.setDefaults()
            self.nargsFlag=len(self.opts)

            print '0000000000000000000 ',self.narg,self.nargsFlag
            print '1111111111111111111 ',self.estrArg
            print '2222222222222222222 ',self.opts,self.args
            print '3333333333333333333 ',self.nargsFlag,self.estrFlag,self
            print '4444444444444444444 ',self.estrCur
            print '5555555555555555555 ',self.estrDefaults
            self.estr=self.estrFlag+self.estrDefaults+self.estrArg+self.estrCur


        else:
            usage(self.__doc__,self.pyfile,self.curdtg,self.curtime)
            sys.exit(1)


    
class LsDiagFile(MFutils):
    
    sfcLevel='surf'
    model='era5'

    stmVarNameByIndex={

        1:'latitude',
        2:'longitude',
        3:'max_wind',
        4:'rms',
        5:'min_slp',
        6:'shr_mag',
        7:'shr_dir',
        8:'stm_spd',
        9:'stm_hdg',
        10:'sst',
        11:'ohc',
        12:'tpw',
        13:'land',
        14:'850tang',
        15:'850vort',
        16:'200dvrg',
    }


    customVarNameByIndex={
        1:'ADECK  VMAX (KT)',
        2:'DIAG   VMAX (KT)',
        #3:'ADECK  PMIN (MB)',
        3:'precip',             # -- use psl into jtdiag table
        4:'DIAG   PMIN (MB)',
        5:'sstanom',
        6:'precip-actual',
        7:'PR  ASYM/TOT (%)',
        8:'TOTSHR MAG  (KT)',
        9:'SHR/TOTSHR   (%)',
        10:'SHR ASYM/TOT (%)',
        11:'CPS  B(AROCLINC)',
        12:'CPS   VTHERM(LO)',
        13:'CPS   VTHERM(HI)',
        14:'POCI        (MB)',
        15:'ROCI        (KM)',
        16:'R34mean     (KM)',
        17:'R50mean     (KM)',
        18:'R64mean     (KM)',
    }


    def __init__(self,dtg,
                 lsdiagpath,
                 verb=0,
                 dobail=0,
                 quiet=1,
                 ):

        self.dtg=dtg
        self.lsdiagpath=lsdiagpath
        self.sbtProdDir=sbtProdDir
        self.verb=verb
        self.dobail=dobail

        self.year=dtg[0:4]
        
        wdir=sbtProdDir
        dtgdir="%s/%s"%(self.year,dtg)
        urldir="%s/%s"%(dtgdir,self.model)
        pltdir="%s/%s"%(wdir,urldir)
        
        self.pltdir=pltdir
        self.tbdir=tsbdbdir
        self.tdir="%s/%s/%s/%s"%(self.tbdir,self.year,dtg,self.model)
        
        
    
    def parseDiag(self,stmid,dobail=1,verb=0):
        """ parse output from lsdiag.x
        """


        def makekey(label):
            tt=label.lower().split()
            nlabel=tt[0]
            ne=-1
            if(nlabel == 'cps'): ne=0
            for n in range(1,len(tt)+ne):
                nlabel="%s_%s"%(nlabel,tt[n])

            nlabel=nlabel.replace(')','')
            nlabel=nlabel.replace('(','')

            return(nlabel)

        lsdiagpath=self.lsdiagpath

        # -- check if SHEM storm
        #
        stmIsShem=0
        if(isShemBasinStm(stmid)): stmIsShem=1
        
        rc=1
        # -- stm vars
        #
        self.stmData={}
        self.stmDataVars={}
        self.cstmData={}
        self.stmLabels={}
        
        # -- custom vars
        #
        self.customData={}
        self.ccustomData={}
        self.customLabels={}

        # -- snd vars
        #
        self.sndData={}
        self.sndDataVar={}
        self.sndPlevs=[]
        self.sndKeys=[]
        self.csndData={}
        self.sndLabels={}
        
        self.diagVals={}
        self.diagTypes={}
        self.diaguRls={}
        self.diagKeys=[]
        self.diagFilenames={}

        self.diagTaus=[]
        self.urlData={}


        self.nstmvars=16
        self.nsndvars=5

        self.curstmid=stmid


        gotstm=0
        gotusr=0
        gotsnd=0
        try:
            cards=open(lsdiagpath).readlines()
        except:
            print """WWW TCDiag.parseDiag couldn't read file: %s"""%(lsdiagpath)
            return(0)

        if(len(cards) == 0):
            print """WWW TCDiag.parseDiag file: %s is 0 length"""%(lsdiagpath)
            return(0)

        for n in range(0,len(cards)):
            if(gotstm and gotusr and gotsnd): break
            card=cards[n]
            if(n == 0 and find(card,'*')):
                tt=card.split()
                aid=tt[1]
                dtg=tt[2]

            if(n == 1 and find(card,'*')):
                tt=card.split()
                stm2id=tt[1]
                stmname=tt[2]

            if(find(card,'STORM') and gotstm == 0):
                gotstm=1
                n=n+1
                card=cards[n]
                if(find(card,'NTIME')):
                    tt=card.split()
                    ntau=int(tt[1])
                    n=n+1
                    card=cards[n]
                    label=card[0:16]
                    label=label.replace('/','_')
                    tt=card[16:].split()
                    for i in range(0,ntau):
                        self.diagTaus.append(int(tt[i]))

                    if(self.verb): print 'self.diagTaus: ',self.diagTaus


                for i in range(0,self.nstmvars):
                    n=n+1
                    card=cards[n]
                    label=card[0:16]
                    label=label.replace('/','_')
                    tt=card[16:].split()
                    for j in range(0,ntau):
                        tau=self.diagTaus[j]
                        if(find(card,'LAT') or find(card,'LON')):
                            val=float(tt[j])
                        else:
                            # -- convert rel vort to cyclonic vort
                            #
                            ival=int(tt[j])
                            if(find(label,'850VORT') and stmIsShem): ival=-1*ival
                            val=ival
                        self.stmData[tau,i+1]=val
                        self.cstmData[tau,i+1]=tt[j]
                        self.stmLabels[i+1]=label

            n=n+1
            card=cards[n]
            if(find(card,'CUSTOM') and gotusr == 0):
                gotusr=1
                n=n+1
                card=cards[n]
                self.ncustomvars=int(card.split()[1])
                n=n+1
                for i in range(0,self.ncustomvars):
                    n=n+1
                    card=cards[n]
                    label=card[0:16]
                    label=label.replace('/','_')
                    tt=card[16:].split()
                    for j in range(0,ntau):
                        tau=self.diagTaus[j]
                        val=int(tt[j])
                        self.customData[tau,i+1]=val
                        self.ccustomData[tau,i+1]=tt[j]
                        self.customLabels[i+1]=label

            n=n+1
            card=cards[n]
            if(find(card,'SOUNDING') and gotsnd == 0):
                gotsnd=1
                n=n+1
                card=cards[n]
                self.nlevs=int(card.split()[1])
                n=n+1
                for i in range(0,self.nlevs):
                    for ii in range(0,self.nsndvars):
                        n=n+1
                        card=cards[n]
                        label=card[0:16]
                        label=label.replace('/','_')
                        tt=card[16:].split()

                        var=label.split()[0].split('_')[0]
                        var=var.lower()

                        plev=label.split()[0].split('_')[-1]
                        plev=plev.lower()
                        if(plev == self.sfcLevel):
                            ilev=plev
                        else:
                            ilev=int(plev)

                        self.sndPlevs.append(plev)
                        for j in range(0,ntau):
                            tau=self.diagTaus[j]
                            val=int(tt[j])
                            self.sndDataVar[tau,var,ilev]=val
                            self.sndData[tau,ii+1,i+1]=val
                            self.csndData[tau,ii+1,i+1]=tt[j]
                            self.sndLabels[ii+1,i+1]=label

                self.sndPlevs=uniq(self.sndPlevs)

        if(self.verb > 1):

            for i in range(0,self.nlevs):
                for ii in range(0,self.nsndvars):
                    for j in range(0,ntau):
                        tau=self.diagTaus[j]
                        print 'ssss(parseDiag) ',tau,self.csndData[tau,ii+1,i+1],self.sndData[tau,ii+1,i+1]





        #ppp -- glob for fields plots to set urlData
        #

        pltpaths=[]
        tpltpaths=glob.glob("%s/*.png"%(self.pltdir))

        for tp in tpltpaths:
            if(not(find(tp,'trkplt')) and not(find(tp,'bm.'))): pltpaths.append(tp)

        for p in pltpaths:
            (dir,file)=os.path.split(p)
            tt=file.split('.')
            pltkey=tt[0]
            pltstm="%s.%s"%(tt[1],tt[2])
            plttau=int(tt[-2])

            # -- match the stmid to plot
            #
            if(pltstm == stmid):
                urlpath="%s/%s/%s/%s"%(self.year,self.dtg,self.model,file)
                MF.set2KeyDictList(self.urlData,plttau,pltkey,urlpath)


        #lll -- load diagVals,diagKeys,diagFilenames
        # storm

        if(self.verb): print
        for i in range(1,self.nstmvars+1):
            for j in range(0,ntau):
                tau=self.diagTaus[j]
                val=self.stmData[tau,i]
                cval=self.cstmData[tau,i]
                label=self.stmLabels[i]

                if(tau == self.diagTaus[0] or len(self.diagTaus) == 1):
                    cstmkey=makekey(label)
                    if(not(cstmkey in self.diagKeys)):
                        self.diagKeys.append(cstmkey)
                    self.diagFilenames[cstmkey]="%s.%s"%(cstmkey,stmid)

                if(j == 0 and self.verb > 1):
                    print 'ssstttmmmmm %2d     %-15s %6.0f'%(i,cstmkey,val)

                MF.set2KeyDictList(self.diagVals,tau,cstmkey,cval)
                MF.set2KeyDictList(self.diagTypes,tau,cstmkey,'storm')

                try:
                    MF.set2KeyDictList(self.diaguRls,tau,cstmkey,self.urlData[tau][cstmkey])
                    if(self.verb): print 'sssssssssssssssssssss setting diaguRLs tau, cstmkeky: ',tau,cstmkey,self.urlData[tau][cstmkey]
                except:
                    MF.set2KeyDictList(self.diaguRls,tau,cstmkey,'None')


        #llllllllllllllllllllllllllllllllllllllllllllllllll -- load diagVals,diagKeys,diagFilenames
        # custom

        if(self.verb): print
        for i in range(1,self.ncustomvars+1):
            for j in range(0,ntau):
                tau=self.diagTaus[j]
                val=self.customData[tau,i]
                cval=self.ccustomData[tau,i]
                label=self.customLabels[i]

                if(tau == self.diagTaus[0] or len(self.diagTaus) == 1):
                    ccustomkey=makekey(label)
                    if(not(ccustomkey in self.diagKeys)):
                        self.diagKeys.append(ccustomkey)
                    self.diagFilenames[ccustomkey]="%s.%s"%(ccustomkey,stmid)

                if(j == 0 and self.verb > 1):
                    print 'ccccccccccc %2d     %-15s %6.0f'%(i,ccustomkey,val)

                MF.set2KeyDictList(self.diagVals,tau,ccustomkey,cval)
                MF.set2KeyDictList(self.diagTypes,tau,ccustomkey,'custom')

                try:
                    MF.set2KeyDictList(self.diaguRls,tau,ccustomkey,self.urlData[tau][ccustomkey])
                    if(self.verb): print 'sssssssssssssssssssss setting diaguRLs tau, ccustomkey: ',tau,ccustomkey,self.urlData[tau][ccustomkey]
                except:
                    MF.set2KeyDictList(self.diaguRls,tau,ccustomkey,'None')

        #llllllllllllllllllllllllllllllllllllllllllllllllll -- load diagVals,diagKeys,diagFilenames
        # sounding

        if(self.verb): print
        for i in range(1,self.nlevs+1):
            for ii in range(1,self.nsndvars+1):
                for j in range(0,ntau):
                    tau=self.diagTaus[j]
                    val=self.sndData[tau,ii,i]
                    cval=self.csndData[tau,ii,i]
                    label=self.sndLabels[ii,i]
                    if(tau == self.diagTaus[0] or len(self.diagTaus) == 1):
                        csndkey=makekey(label)
                        if(not(csndkey in self.diagKeys)):
                            self.diagKeys.append(csndkey)
                        self.diagFilenames[csndkey]="%s.%s"%(csndkey,stmid)

                    MF.set2KeyDictList(self.diagVals,tau,csndkey,cval)
                    MF.set2KeyDictList(self.diagTypes,tau,csndkey,'sounding')

                    if(j == 0 and self.verb > 1):
                        print 'sssdddnnngg %2d %2d  %-15s %6.0f'%(ii,i,csndkey,val)

                    try:
                        MF.set2KeyDictList(self.diaguRls,tau,csndkey,self.urlData[tau][csndkey])
                        if(self.verb): print 'sssssssssssssssssssss setting diaguRLs tau, csndkey: ',tau,csndkey,self.urlData[tau][csndkey]
                    except:
                        MF.set2KeyDictList(self.diaguRls,tau,csndkey,'None')

        if(self.verb): print
        for kk in self.diagKeys:
            card=kk
            for tau in self.diagTaus:
                card="%15s %5s"%(card,self.diagVals[tau][kk])
            if(self.verb): print 'parseDiag:',card

        # -- set the taus
        #
        self.taus=self.diagTaus

        return(rc)




class Mdeck3(MFutils):
    

    def __init__(self,
                 tbdir=None,
                 oyearOpt=None,
                 verb=0,
                 doclean=0,
                 stmdtg=None,
                 basinopt=None,
                 doBT=0,
                 doWorkingBT=0,
                 quiet=1,
                 doSumOnly=0,
                 ):
        

        if(not(quiet)): self.sTimer('md3-init')
        self.verb=verb
        self.doBT=doBT
        
        if(tbdir == None):
            tbdir=sbtSrcDir
            tbdir=sbtVerDir
            tbdir=sbtVerDirDat

        self.tbdir=tbdir
        
        if(oyearOpt == None):
            oyearOpt='%s-%s'%(bm3year,em3year)
            
        oyearOpt="%s"%(oyearOpt)
        self.oyearOpt=oyearOpt

        # -- (allCvsPath) = md3 track cards with data by storm and dtg
        # -- (sumCvsPath) = md3 storm summary cards 
        #
        rc=self.getCvsYearPaths(doBT=doBT)
        (allCvsPath,sumCvsPath)=rc

        # -- get hashes with storm summary and names
        #
        stmSum={}
        tcNamesHash={}
        scards=open(sumCvsPath).readlines()
        for scard in scards[1:]:
            #print scard[0:-1]
            tt=scard.split(',')
            stmid=tt[0]
            ss=stmid.split(".")
            year=ss[1]
            b3id=ss[0]
            tccode=tt[1]
            tcdev=tt[2]
            name=tt[3]
            tcNamesHash[(year,b3id)]=name
            stmSum[stmid]=tt
            
        self.stmSum=stmSum
        self.tcNamesHash=tcNamesHash
        
        stmMetaMd3={}
        stmMetaMd3Card={}
        
        if(not(doSumOnly)):
            dtgMd3={}
            stmMd3={}
            
            # -- get the md3 track
            #
            acards=open(allCvsPath).readlines()
            #print 'aaa',allCvsPath
            for acard in acards[1:]:
                # -- the last entry has '\n' skip
                tt=acard.split(',')
                dtg=tt[0]
                stmid=tt[1]
                MF.appendDictList(dtgMd3, dtg, stmid)
                MF.appendDictList(stmMd3, stmid, tt[0:-1])
            

            dtgMd3=MF.uniqDict(dtgMd3)
            md3dtgs=dtgMd3.keys()
            md3dtgs.sort()
            self.md3dtgs=md3dtgs
            self.dtgMd3=dtgMd3
            md3stmids=stmMd3.keys()
            md3stmids.sort()
            self.md3stmids=md3stmids
            self.stmMd3=stmMd3


        # -- get the summary cards with stmid meta data
        #
        acards=open(sumCvsPath).readlines()
        for acard in acards[1:]:
            #print 'sss',acard
            tt=acard.split(',')
            stmid=tt[0]
            #print 'sss',stmid,tt[-1]
            # skip the last entry which is always '\n'
            stmMetaMd3[stmid]=tt[0:-1]
            stmMetaMd3Card[stmid]=acard[0:-1]

        # -- decorate
        #
        self.stmMetaMd3=stmMetaMd3
        self.stmMetaMd3Card=stmMetaMd3Card
        
        if(not(quiet)): self.dTimer('md3-init')

    def getMd3Stmids(self,stmopt,yearopt=None,dobt=0,dofilt9x=0,verb=0):
        
        # -- like tcnames hash
        #
        tcnames=self.tcNamesHash.keys()
    
        def getBnum1and2(bnum1,bnum2):
            
            try:
                bnum1=int(bnum1)
            except:
                bnum1=str(bnum1)
     
            try:
                bnum2=int(bnum2)
            except:
                bnum2=str(bnum2)
                
            return(bnum1,bnum2)
     
        
        # -- get years
        #
        def getyears(yyy):
        
            if(yyy == 'cur'):
                curdtg=dtg()
                yyy=curdtg[0:4]
        
            years=[]
            n1=0
            n2=0
        
            tt0=yyy.split('-')
            tt1=yyy.split(',')
        
            if(len(tt1) > 1):
                for tt in tt1:
                    yyyy=add2000(tt)
                    years.append(yyyy)
                return(years)
        
            if(len(tt0) > 1):
                y1=tt0[0]
                y2=tt0[1]
                yyyy1=add2000(y1)
                yyyy2=add2000(y2)
        
                if(len(yyyy1) != 4 or len(yyyy2) != 4):
                    print 'EEEE getyears tt:',tt
                    return(None)
        
                else:
                    n1=int(yyyy1)
                    n2=int(yyyy2)
                    for n in range(n1,n2+1):
                        years.append(str(n))
        
            else:
                if(len(yyy) <= 2): yyy=add2000(yyy)
                years=[yyy]
        
            return(years)
        
        
        # -- get stmids by filtering from master list
        #
        def getstmids(sss,year,dos3id=0,dofilt9x=dofilt9x):
        
            sids=[]
            n1=0
            n2=0
            tt=sss.split('-')
            
            if(len(tt) > 1):
                
                if(len(tt[0]) != 2 or len(tt[1]) != 3):
                    print 'EEEE getstmids tt:',tt
                    return(None)
        
                else:
                    n1=int(tt[0])
                    n2=int(tt[1][0:2])
                    bid=tt[1][2].upper()
        
                    for n in range(n1,n2+1):
                        sss="%02d%1s"%(n,bid)
                        sid="%s.%s"%(sss,year)
                        sid=getstmids(sss,year,dos3id=1)
                        sids.append(sid[0])
                        
        
            elif(len(sss) == 1 or dos3id):
        
                doChkNum=0
                doChk9x=0
    
                if(dos3id and len(sss) == 3):
                    
                    bchk=sss[-1].upper()
                    bnum=sss[0:2]
                    bnum1=sss[0]
                    bnum2=sss[1]
                    
                    try:
                        bnum=int(bnum)
                        if(bnum >= 1 and bnum <=70):
                            bnum="%02d"%(bnum)
                            doChkNum=1
                        elif(bnum >= 90):
                            doChkNum=0
                        else:
                            print 'WWW -- invalid bnum in getstmids'
                            sys.exit()
                    except:
                        bnum=str(bnum)
    
    
                    (bnum1,bnum2)=getBnum1and2(bnum1, bnum2)
    
                    if(type(bnum1) is StringType or 
                       (type(bnum1) is IntType and (bnum1 >= 0 and bnum2 <=9)) or
                       (type(bnum2) is StringType and bnum2 == 'X')
                       ):
                        doChk9x=1
                        
                    #print 'aaaaaaa',bchk,bnum,type(bnum),bnum1,type(bnum1),bnum2,type(bnum2),doChkNum,doChk9x
                        
                else:
                    bchk=sss.upper()
                    
        
                for tcname in tcnames:
                    # -- improved subbasin checking...
                    #
                    tcyear=tcname[0]
                    tcb3id=tcname[1].upper()
                    tcstmid="%s.%s"%(tcb3id,tcyear)
                    tcnum=tcb3id[0:2]
                    tcbnum1=tcnum[0]
                    tcbnum2=tcnum[1]
                    (tcbnum1,tcbnum2)=getBnum1and2(tcbnum1,tcbnum2)
                    
                    
                    tc9X=tcb3id[1]
                    tcsubbasin=tcb3id[2:3]
                    
                    chk0=(tcyear == year)
                    chk1=(tcsubbasin == bchk)
                    chk2=0
                    chk3=0
                    if(bchk == 'H'): chk3=(isShemBasinStm(tcsubbasin) and isShemBasinStm(bchk))
                    if(bchk == 'I'): chk2=(isIOBasinStm(tcsubbasin) and isIOBasinStm(bchk))
                    
                    # -- first check year only
                    #
                    if(chk0):
                        
                        if(doChkNum): 
                            chknum=(str(bnum) == tcnum)
                            chkb=((chk1 or chk2 or chk3) and chknum)
                            
                        elif(doChk9x):
                            
                            chk90=(type(bnum1) is IntType and bnum1 == 9 and type(tcbnum1) is StringType)
    
                            chk91=(type(bnum1) is StringType and type(tcbnum1) is StringType and
                                   (bnum1 == tcbnum1))
                            chk92=(type(bnum2) is IntType and type(tcbnum2) is IntType and
                                   (bnum2 == tcbnum2))
                            
                            chk93=(type(bnum1) is IntType and bnum1 == 9 and 
                                   type(bnum2) is StringType and bnum2 == 'X' and
                                   not(IsNN(tcstmid)))
                            
                            chk9a=(chk90 and chk92) 
                            chk9b=(chk91 and chk92)
                            chk9c=(chk93)
                            chkb=((chk1 or chk2 or chk3) and (chk9a or chk9b or chk9c) )
            
                        else:
                            chkb=(chk1 or chk2 or chk3)
                        
                        if(chkb):
                            sid="%s.%s"%(tcname[1],tcname[0])
                            sids.append(sid)
                        else:
                            sid=None
                        
        
            else:
                print 'EEEE getstmids sss:',sss
                return(None)
        
        
            sids.sort()
            osids=sids
            if(dobt):
                osids=[]
                for sid in sids:
                    if(IsNN(sid)): osids.append(sid)
                    
            return(osids)
    
        # -- mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
        #
        
        curdtg=dtg()
        curyear=curdtg[0:4]
        
    
        # -- defaults
        #
        if(stmopt == None):
        
            sopt='w,e,c,l,i,a,b,p,s'
            if(yearopt == None):
                yopt='cur'
            else:
                yopt=yearopt
            years=getyears(yopt)
        
        # -- by stmopt
        #
        elif(stmopt != None and stmopt != 'all'):
            
            ttt=stmopt.split('-')
            ttc=stmopt.split(',')
            tt=stmopt.split('.')
            
            #print 'sssssssssssssss',stmopt,len(ttt),len(ttc),len(tt)
            
            if(len(tt) == 1 and len(ttt) == 1 and len(ttc) == 1):
                if(len(tt[0]) == 3):
                    stmid=tt[0][2]
                elif(len(tt[0]) != 1):
                    print 'tcVM.MakeStmList() EEEE bad stm3id: tt:',tt,'ttt: ',ttt,'ttc: ',ttc,'stmopt: ',stmopt
                    sys.exit()
                else:
                    stmid=tt[0]
        
                if(isShemBasinStm(stmid)):
                    stmyear=getShemYear(curdtg)
                else:
                    stmyear=curyear
        
                if(isIOBasinStm(stmid)):
                    stmyear=curyear
                    
                stmyear=add2000(stmyear)
        
                stmopt=stmopt+'.'+stmyear
                tt=stmopt.split('.')
                
            # -- stm spanning using current year
            #
            elif(len(ttt) > 1 and len(ttc) == 1 and len(tt) == 1):
                stmids=getstmids(stmopt,curyear,dos3id=1,dofilt9x=dofilt9x)
                return(stmids)
        
            # -- list of individual stmid (sss.y)
            #
            if(len(ttc) > 1):
        
                stmids=[]
                for stmopt in ttc:
                    stmids=stmids+self.getMd3Stmids(stmopt,self.tcNamesHash,dobt=dobt,dofilt9x=dofilt9x,
                                              verb=verb)
        
                return(stmids)
        
        
            if(len(ttc) > 1 and len(tt) > 2):
        
                stmids=[]
        
                for stmid in ttc:
                    ss1=stmid.split('.')
                    if(len(ss1) != 2):
                        print 'EEE invalid individual stm: ',stmid
                        sys.exit()
        
                    sid=ss1[0]
                    yid=ss1[1]
                    if(len(yid) >= 1): yid=add2000(yid)
                    rc=getstmids(sid,yid,dofilt9x)
                    stmids=stmids+rc
        
                return(stmids)
        
            sopt=tt[0]
            yopt=tt[1]
            years=getyears(yopt)
        
        else:
        
            sopt='w,e,c,l,i,a,b,p,s'
            if(yearopt == None):
                yopt='cur'
            else:
                yopt=yearopt
            years=getyears(yopt)
        
        
        if(verb):
            print 'getMd3Stmids sopt: ',sopt
            print 'getMd3Stmids yopt: ',yopt,years
        
        
        stmids=[]
        
        for year in years:
        
            sopt=sopt.upper()
            ss=sopt.split(',')
            
            if(len(ss) > 1):
                for sss in ss:
                    rc=getstmids(sss,year,dofilt9x=dofilt9x)
                    if(rc != None):
                        stmids=stmids+rc
        
            else:
                stmopt="%s.%s"%(sopt,year)
                rc=getstmids(sopt,year,dos3id=1,dofilt9x=dofilt9x)
                if(rc != None):
                    stmids=stmids+rc
        
        #  -- filter out 9X
        #
        if(dofilt9x):
            nstmids=[]
            for stmid in stmids:
                num=int(stmid[0:2])
                if(num < 80):
                    nstmids.append(stmid)
        
            stmids=nstmids
        
        
        if(verb):
            for stmid in stmids:
                print 'getMd3Stmids stmid: ',stmid
        
        return(stmids)
    
    def getCvsYearPaths(self,doBT=0):
        """
not sure about this...MRG has BT .csv has working best track
always use all-BT because m-md3-all-csv.py does a merge process
that generates of -MRG.txt where the working is updated with BT
        """
        if(doBT == -1):
            allCvsPath="%s/all-md3-%s.csv"%(self.tbdir,self.oyearOpt)
            sumCvsPath="%s/sum-md3-%s.csv"%(self.tbdir,self.oyearOpt)
        else:
            allCvsPath="%s/all-md3-%s-MRG.csv"%(self.tbdir,self.oyearOpt)
            sumCvsPath="%s/sum-md3-%s-MRG.csv"%(self.tbdir,self.oyearOpt)
    
        return(allCvsPath,sumCvsPath)

    
    def getCvsYearOptPaths(self,tbdir,oyearOpt,headAll,headSum):
        
        
        allCvsPath=allCvsPathBT=sumCvsPath=sumCvsPathBT=None
        
        allCvsPath="%s/all-md3-%s.csv"%(self.tbdir,oyearOpt)
        allCvsPathBT="%s/all-md3-%s-BT.csv"%(self.tbdir,oyearOpt)
        sumCvsPath="%s/sum-md3-%s.csv"%(self.tbdir,oyearOpt)
        sumCvsPathBT="%s/sum-md3-%s-BT.csv"%(self.tbdir,oyearOpt)
            
        return(allCvsPath,allCvsPathBT,sumCvsPath,sumCvsPathBT)
    
    def getBasin4b1id(self,b1id):
        ib1id=b1id.lower()
        if(ib1id == 'l'):
            basin='lant'
        elif(ib1id == 'w'):
            basin='wpac'
        elif(ib1id == 'e' or ib1id == 'c'):
            basin='epac'
        elif(ib1id == 'i' or ib1id == 'b' or ib1id == 'a'):
            basin='io'
        elif(ib1id == 'h' or ib1id == 's' or ib1id == 'p'):
            basin='shem'
        else:
            print 'EEE in getBasin4b1id b1id: ',b1id
            sys.exit()
            
            
        return(basin)
            
    
    def parseStmSumCard(self,card):
        
        tt=card.split(",")
        tstmid=tt[0]
        sname=tt[3]
        bdtg=tt[9]
        edtg=tt[10]
        stm9x=tt[22]
        t2gen=tt[23]
        dtggen=tt[24].strip()
        rc=(tstmid,bdtg,edtg,sname,stm9x,t2gen,dtggen)
        return(rc)
        
    
    def getTcData(self,year,basin):
        
        if(basin =='shem'):
            stmopt='h.%s'%(year)
            tD=TcData(stmopt=stmopt)
        elif(basin =='io'):
            stmopt='i.%s'%(year)
            tD=TcData(stmopt=stmopt)
        elif(basin =='epac'):
            stmopt='c.%s,e.%s'%(year,year)
            tD=TcData(stmopt=stmopt)
        elif(basin =='lant'):
            stmopt='l.%s'%(year)
            tD=TcData(stmopt=stmopt)
        elif(basin =='wpac'):
            stmopt='w.%s'%(year)
            tD=TcData(stmopt=stmopt)
        return(tD)
    
    def getMd3path(self,tstmid):
        
        rc=getStmParams(tstmid)
        stm3id="%s%s"%(rc[0],rc[1])
        stm3id=stm3id.upper()
        
        tyear=rc[2]
        tmask="%s/%s/*/%s*"%(sbtSrcDir,tyear,stm3id)
        odirs=glob.glob("%s"%(tmask))
        if(len(odirs) == 1):
            sdir=odirs[0]
        else:
            print 'EEE -- finding sdir in getMd3path for sbtSrcDir: ',sbtSrcDir,' tstmid: ',tstmid,'sayounara'
            sys.exit()
    
        if(IsNN(tstmid)):
            md3mask="%s/*-%s-md3-BT.txt"%(sdir,tyear)
            md3paths=glob.glob(md3mask)
        else:
            md3mask="%s/*-%s-md3.txt"%(sdir,tyear)
            md3paths=glob.glob(md3mask)
            
        if(len(md3paths) == 1):
            md3path=md3paths[0]
        else:
            print 'EEE -- finding md3path in getMd3Spath for sbtSrcDir: ',sbtSrcDir,' tstmid: ',tstmid,'sayounara'
            sys.exit()
            
        return(md3path)
        
    
    
    def getTstmidsSum(self,year,basin,spath,ropt='norun',doBTonly=0,verb=0):
        
        (ddir,ffile)=os.path.split(spath)
        cards=open(spath).readlines()
        
        basinStm={}
        allStm={}
        for card in cards:
            
            if(verb):
                n=0
                tt=card.split(',')
                for n in range(0,len(tt)):
                    print 'n: %2d'%(n),tt[n]
            
            rc=parseStmSumCard(card)
            (tstmid,bdtg,edtg,sname,stm9x,t2gen,dtggen)=rc
            
            # -- option to do BT only
            #
            if(doBTonly and not(IsNN(stm1id))):
                continue
    
            basinStm[rc[0]]=(bdtg,edtg,sname,stm9x,t2gen,dtggen)
            
        bstmids=basinStm.keys()
        for bstmid in bstmids:
            allStm[bstmid]=basinStm[bstmid]
            
    
        return(allStm)    
    
    
    def getMd3Stmids4dtg(self,dtg,dobt=0,verb=0,warn=0):
        
        try:
            stmids=self.dtgMd3[dtg]
        except:
            if(warn): print 'WWW no md3 stms for dtg: ',dtg
            stmids=[]
            return(stmids)

        ostmids=stmids
        
        if(dobt):
            ostmids=[]
            for stmid in stmids:
                if(IsNN(stmid)): ostmids.append(stmid)
                
        return(ostmids)
        
    def getMd3StmMeta(self,stmid,doprint=0):

        #n 0 30w.2019
        #n 1 TY
        #n 2 NN
        #n 3 PHANFONE
        #n 4 105
        #n 5 7.2
        #n 6 12.0
        #n 7 9.9
        #n 8 131.6
        #n 9 2019121718
        #n 10 2019122918
        #n 11 4.4
        #n 12 15.5
        #n 13 110.8
        #n 14 158.5
        #n 15 6.5
        #n 16 7.3
        #n 17 6
        #n 18 0
        #n 19 4
        #n 20 ddRI
        #n 21 9X
        #n 22 z0w
        #n 23 96
        #n 24 2019122118
        
        sm=self.stmMetaMd3[stmid]
        # -- parse
        #
        livestatus=' '
        sstmid=sm[0]
        (stm,yyyy)=sstmid.split('.')
        tctype=sm[1]
        stmDev=sm[2]
        sname=sm[3]
        ovmax=str(sm[4])
        tclife=float(sm[5])
        stmlife=float(sm[6])
        latb=float(sm[7])
        lonb=float(sm[8])
        bdtg=sm[9]
        edtg=sm[10]
        latmn=float(sm[11])
        latmx=float(sm[12])
        lonmn=float(sm[13])
        lonmx=float(sm[14])
        stcd=float(sm[15])
        oACE=float(sm[16])
        nRI=int(sm[17])
        nED=int(sm[18])
        nRW=int(sm[19])
        RIstatus=sm[20]
        if(RIstatus == 'NaN'): RIstatus='    '
        stm9xtype=sm[21]
        stm9x=sm[22]
        stm9x="%s: %s"%(stm9xtype,stm9x.upper())
        
        if(sm[23] != 'NaN'):
            timeGen=int(sm[23])
        else:
            timeGen=0
            
        timeGen="tG:%3d"%(timeGen)
        ogendtg=sm[24].strip()
        if(ogendtg == 'NaN'): ogendtg=''
        
        stm=stm.upper()
        
        ocard="%s %s%1s %3s %-10s :%3s :%4.1f;%4.1f :%5.1f %5.1f : %s<->%s :%5.1f<->%-5.1f :%5.1f<->%-5.1f :%4.1f :%4.1f :%2d:%2d:%2d:%s :%s %s %s"%\
            (yyyy,stm,livestatus,tctype,sname[0:9],ovmax,tclife,stmlife,latb,lonb,bdtg[4:],edtg[4:],
             latmn,latmx,lonmn,lonmx,
             stcd,oACE,
             nRI,nED,nRW,
             RIstatus,timeGen,stm9x,ogendtg)

        rc=(yyyy,stm,livestatus,tctype,sname,ovmax,tclife,stmlife,latb,lonb,bdtg,edtg,
            latmn,latmx,lonmn,lonmx,
            stcd,oACE,
            nRI,nED,nRW,
            RIstatus,timeGen,stm9x,ogendtg)
        
        ocard=ocard[0:-1]
        if(doprint): 
            print ocard
            
        return(rc,ocard)

        
    
    def getMd3track(self,stmid,dobt=0,undef=-999.,verb=0,domiss=0):
        
        #mkFloat=self.mkFloat
        
        #n:  0 2019122118
        #n:  1 30w.2019
        #n:  2 PHANFONE
        #n:  3 TY
        #n:  4 NN
        #n:  5 6.4
        #n:  6 139.9
        #n:  7 30
        #n:  8 1002
        #n:  9 293
        #n: 10 14
        #n: 11 293
        #n: 12 14
        #n: 13 NaN
        #n: 14 NaN
        #n: 15 NaN
        #n: 16 NaN
        #n: 17 NaN
        #n: 18 NaN
        #n: 19 NaN
        #n: 20 NaN
        #n: 21 NaN
        #n: 22 NaN
        #n: 23 TD
        #n: 24 WN
        #n: 25 B  dirtype
        #n: 26 B  posttype
        #n: 27 140
        #n: 28 1006
        #n: 29 NaN
        #n: 30 S
        #n: 31 30
        #n: 32 RCB
             
        m3trk={}
        stmid=stmid.lower()

        try:
            smeta=self.stmMetaMd3[stmid]
        except:
            #print 'EEE in getMd3track for: ',stmid
            return(0,m3trk)
            
            
        m3trk={}
        stmcards=self.stmMd3[stmid]

        if(IsNN(stmid)):
            # --smeta[-1] has the type of gendtg
            smkey=len(smeta)
            stmid9x="%s.%s"%(smeta[-4],stmid.split('.')[-1])
            stmcards9x=self.stmMd3[stmid9x]
            stmcards=stmcards+stmcards9x
            
        for mm in stmcards:

            rc=parseMd3Card(mm,dobt=dobt,verb=verb)
            if(rc == None):continue

            (dtg,rlat,rlon,vmax,pmin,tdir,tspd,r34m,r50m,
             tcstate,warn,
             roci,poci,alf,
             depth,eyedia,tdo,ostmid,ostmname,r34,r50)=rc
            if(verb):
                print 'rrrrr',dtg,rlat,rlon,vmax,pmin,tdir,tspd,r34m,r50m,tcstate,warn,roci,poci
            m3trk[dtg]=(rlat,rlon,vmax,pmin,tdir,tspd,r34m,r50m,tcstate,warn,roci,poci,alf,depth,eyedia,tdo,ostmid,ostmname,r34,r50)
            
        def interpM3trk(m1,m2,f1,f2):
            
            def dointerp(v1,v2,f1,f2):
                if(v1 != undef and v1 != undef): vi=v1*f1+v2*f2
                if(v1 != undef and v2 == undef): vi=v1
                if(v2 != undef and v1 == undef): vi=v2
                if(v1 == undef and v2 == undef): vi=undef
                
                return(vi)
                
                
            (rlat1,rlon1,vmax1,pmin1,tdir1,tspd1,r34m1,r50m1,tcstate1,warn1,roci1,poci1,alf1,depth1,eyedia1,tdo1,ostmid1,ostmname1,r341,r501)=m1
            (rlat2,rlon2,vmax2,pmin2,tdir2,tspd2,r34m2,r50m2,tcstate2,warn2,roci2,poci2,alf2,depth2,eyedia2,tdo2,ostmid2,ostmname2,r342,r502)=m2
            
            rlati=rlat1*f1+rlat2*f2
            rloni=rlon1*f1+rlon2*f2
            vmaxi=dointerp(vmax1,vmax2,f1,f2)
            pmini=dointerp(pmin1,pmin2,f1,f2)
            tdiri=dointerp(tdir1,tdir2,f1,f2)
            tspdi=dointerp(tspd1,tspd2,f1,f2)
            r34mi=dointerp(r34m1,r34m2,f1,f2)
            r50mi=dointerp(r50m1,r50m2,f1,f2)
            tcstatei=tcstate1
            warni=warn1
            rocii=dointerp(roci1,roci2,f1,f2)
            pocii=dointerp(poci1,poci2,f1,f2)
            alfi=dointerp(alf1,alf2,f1,f2)
            depthi=depth1
            eyediai=eyedia1
            tdoi=tdo1
            ostmidi=ostmid1
            ostmnamei=ostmname1
            r34i=r341
            r50i=r501
            
            mi=(rlati,rloni,vmaxi,pmini,tdiri,tspdi,r34mi,r50mi,tcstatei,warni,rocii,pocii,alfi,depthi,eyediai,tdoi,ostmidi,ostmnamei,r34i,r50i)
            return(mi)
            
        # -- check if we need to interpolate for missing dtgs
        #
        idtgs=m3trk.keys()
        idtgs.sort()
        fdtgs=dtgrange(idtgs[0],idtgs[-1],6)
        li=len(idtgs)
        lf=len(fdtgs)
        
        # -- we do need to interpolate... can handle 12 and 18 gaps
        
        if(li != lf):

            mdtgs=[]
            if(verb): print 'li lf',stmid,li,lf
            for n in range(0,lf):
                fdtg=fdtgs[n]
                try:
                    m3i=m3trk[fdtg]
                except:
                    
                    dtg1=fdtgs[n-1]
                    indx=idtgs.index(dtg1)
                    dtg2=idtgs[indx+1]
                    
                    if(verb): print 'have to interpolate...',fdtg,'dtg1 2',dtg1,dtg2
                    # -- do the interpolation here...
                    #
                    dtgib=dtginc(dtg1,+6)
                    dtgie=dtginc(dtg2,-6)
                    dtgis=dtgrange(dtgib, dtgie)
                    iden=dtgdiff(dtg1, dtg2)
                    if(iden > 36.0):
                        print'EEE big iterp interval for stmid',stmid,dtg1,dtg2,iden
                        sys.exit()
                    m1=m3trk[dtg1]
                    m2=m3trk[dtg2]

                    for dtgi in dtgis:

                        inum1=dtgdiff(dtg1, dtgi)
                        inum2=dtgdiff(dtgi,dtg2)

                        f1=inum2/iden
                        f2=inum1/iden
                    
                        if(verb): print 'interp for dtg',dtg1,dtgi,dtg2,inum1,inum2,f1,f2
                        m3trk[dtgi]=interpM3trk(m1,m2,f1,f2)
                        mdtgs.append(dtgi)
                        n=n+1
                    n=n+1
                    
                    
                    
            if(domiss): return(None,mdtgs)
            return(1,m3trk)
            
        return(1,m3trk)
            
    def getMd3tracks(self,stmids,dobt=0,undef=-999.,verb=0):
        m3trks={}
        for stmid in stmids:
            (rc,m3trk)=self.getMd3track(stmid,dobt=dobt)
            m3trks[stmid]=m3trk
        return(m3trks)
    
    def getMd3StmDtgs4Stmopt(self,stmopt,syear=None,dobt=0,undef=-999.,verb=0):
        stmopts=getStmopts(stmopt)
        
        m3dtgs=[]
        for stmopt in stmopts:
            tstmids=self.getMd3Stmids(stmopt)
            for stmid in tstmids:
                (rc,m3trk)=self.getMd3track(stmid,dobt=dobt)
                if(rc):
                    m3dtgs=m3dtgs+m3trk.keys()
                    
        m3dtgs=uniq(m3dtgs)
        if(syear != None):
            om3dtgs=[]
            for m3dtg in m3dtgs:
                if(m3dtg[0:4] == syear):
                    om3dtgs.append(m3dtg)
                    
            m3dtgs=om3dtgs
        
        return(m3dtgs)
    
    
    def getTstmidsSumOLD(self,year,basin,spath,ropt='norun',doBTonly=0):
        
        (ddir,ffile)=os.path.split(spath)
        cards=open(spath).readlines()
        tstmids=[]
        
        for card in cards:
            tt=card.split(":")
            stm3id=tt[0].split()[1]
            stm1id="%s.%s"%(stm3id,year)
            
            # -- option to do BT only
            #
            if(doBTonly and not(IsNN(stm1id))):
                continue
    
            tstmids.append(stm1id)
    
        return(tstmids)    
    
    
    
    def getTstmidsByYearBasin(self,years,basins,stbdir):
        
        tstmids=[]
        for year in years:
            tdir="%s/%s"%(stbdir,year)
            MF.ChkDir(tdir,'mk')
            
            for basin in basins:
                spath="%s/stm-%s-%s.txt"%(tdir,basin,year)
                tstmids=tstmids+getTstmidsSum(year,basin,spath)
        
        return(tstmids)        
    
    def makeTCvCard(self,stmid,dtg,trk,verb=0):
    
            # -- set rmax to None

            rmax=None
            (rlat,rlon,vmax,pmin,tdir,tspd,r34m,r50m,
             tcstate,warn,roci,poci,alf,depth,eyedia,tdo,ostmid,ostmname,r34,r50)=trk[dtg]
            (clat,clon)=Rlatlon2Clatlon(rlat,rlon,dozero=1)
    
            carqvmax=vmax*knots2ms
            if(carqvmax > 0.0):
                vitvmax="%02d"%(nint(carqvmax))
            else:
                carqvmax=-9
                vitvmax="%02d"%(carqvmax)
    
    
            if(poci != None and poci != undef):
                carqpoci=poci
                vitpoci="%04d"%(nint(carqpoci))
            else:
                carqpoci=-999.
                vitpoci="%04d"%(carqpoci)
    
    
            if(roci != None and roci != undef):
                carqroci=roci*nm2km
                vitroci="%04d"%(nint(carqroci))
            else:
                carqroci=-999
                vitroci="%04d"%(carqroci)
    
            if(rmax != None):
                carqrmax=rmax*nm2km
                vitrmax="%03d"%(nint(carqrmax))
            else:
                carqrmax=-99
                vitrmax="%03d"%(carqrmax)
    
    
            tcdepth=depth
            if(not(depth == 'S' or depth == 'M' or depth == 'D')): tcdepth='X'
    
            # -- one posit for c7w.07
            #
            if(tdir == undef):
                vitdir='-99'
            else:
                vitdir="%03.0f"%(tdir)
    
            if(tspd == undef):
                vitspd='-99'
            else:
                vitspd="%03.0f"%(tspd*10.0*knots2ms)
    
    
            if(pmin != None and pmin != undef):
                vitpmin="%04d"%int(pmin)
            else:
                pmin=-999
                vitpmin="%04d"%int(pmin)
    
            carqr34ne=r34[0]*nm2km
            carqr34se=r34[1]*nm2km
            carqr34sw=r34[2]*nm2km
            carqr34nw=r34[3]*nm2km
            
            if(carqr34ne > 0.0):
                vitr34ne="%04.0f"%(carqr34ne)
            else:
                r34ne=-999.
                vitr34ne="%04.0f"%(r34ne)
    
            if(carqr34se > 0.0):
                vitr34se="%04.0f"%(carqr34se)
            else:
                r34se=-999.
                vitr34se="%04.0f"%(r34se)
    
            if(carqr34sw > 0.0):
                vitr34sw="%04.0f"%(carqr34sw)
            else:
                r34sw=-999.
                vitr34sw="%04.0f"%(r34sw)
    
            if(carqr34nw > 0.0):
                vitr34nw="%04.0f"%(carqr34nw)
            else:
                r34nw=-999.
                vitr34nw="%04.0f"%(r34nw)
    
            vitdepth=tcdepth
    
            # MFTC 97S UNKNOWN   20100415 1200 083S 1017E 130 007 1010 -999 -999 08 -99 -999 -999 -999 -999 X
    
            stm3id=stmid.split('.')[0].upper()
            tcvitalscard="%4s %3s %-9s %8s %04d %s %s %s %s %s %s %s %s %s %s %s %s %s %s"%\
                (tcVcenterid,stm3id,ostmname[0:9],
                 dtg[0:8],int(dtg[8:10])*100,
                 clat,clon,
                 vitdir,vitspd,
                 vitpmin,
                 vitpoci,vitroci,
                 vitvmax,vitrmax,
                 vitr34ne,vitr34se,vitr34sw,vitr34nw,
                 vitdepth)
    
            if(verb): print tcvitalscard
            return(tcvitalscard)
    
    
    def makeTCvCards(self,stmids,dtg,trks,override=0,verb=0,filename='tcvitals',tcvPath=None):

        cards=''
        for stmid in stmids:
            cards=cards+self.makeTCvCard(stmid,dtg,trks[stmid])+'\n'

        if(verb): 
            print
            for card in cards.split('\n'):
                if(len(card) > 1): print card

        if(tcvPath != None):
            tcvpath=tcvPath
            rc=MF.WriteString2File(cards,tcvPath,verb=verb)
            return(cards,tcvpath)
        else:
            tcvpath="%s/%s.%s.txt"%(TcVitalsDatDir,filename,dtg)
            return(cards,tcvpath)


# -- CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCc
#


class Trkdata(MFbase):

    def __init__(self,
                 rlat,
                 rlon,
                 vmax,
                 pmin=undef,
                 dir=undef,
                 spd=undef,
                 tccode='XX',
                 wncode='XX',
                 trkdir=undef,
                 trkspd=undef,
                 dirtype='X',
                 b1id='X',
                 tdo='XXX',
                 ntrk=0,
                 ndtgs=0,
                 r34m=undef,
                 r50m=undef,
                 r34=undef,
                 r50=undef,
                 alf=undef,
                 depth='X',
                 poci=undef,
                 roci=undef,
                 rmax=undef,
                 ):


        self.undef=undef
        self.rlat=rlat
        self.rlon=rlon
        self.vmax=vmax
        self.pmin=pmin
        self.dir=dir
        self.spd=spd
        self.tccode=tccode
        self.wncode=wncode
        self.trkdir=trkdir
        self.trkdir=trkspd
        self.dirtype=dirtype
        self.b1id=b1id
        self.tdo=tdo
        self.ntrk=ntrk
        self.ndtgs=ndtgs
        self.r34=r34
        self.r50=r50
        self.r34m=r34m
        self.r50m=r50m
        self.alf=alf
        self.depth=depth
        self.poci=poci
        self.roci=roci
        self.rmax=rmax


    def gettrk(self):

        trk=(self.rlat,self.rlon,self.vmax,self.pmin,
             self.dir,self.spd,
             self.tccode,self.wncode,
             self.trkdir,self.trkspd,self.dirtype,
             self.b1id,self.tdo,self.ntrk,self.ndtgs,
             self.r34m,self.r50m,self.alf,self.sname,
             self.r34,self.r50,self.depth,
             )

        return(trk)


    def getposit(self):

        posit=(self.rlat,self.rlon,self.vmax,self.pmin,
               self.dir,self.spd,self.tccode,
               )
        return(posit)

class ADutils(MFutils):


    def Smth121(self,data,npass=0):

        nd=len(data)

        if(npass == 0):
            tdata=copy.deepcopy(data)
            return(tdata)

        odata=copy.deepcopy(data)
        tdata=copy.deepcopy(data)

        for n in range(0,npass+1):

            for i in range(0,nd):
                if(i == 0 or i == nd-1):
                    tdata[i]=odata[i]
                else:
                    tdata[i]=0.25*odata[i-1]+0.5*odata[i]+0.25*odata[i+1]

            for i in range(0,nd):
                odata[i]=tdata[i]

        return(tdata)




    def FcTrackInterpFill(self,itrk,dtx=3,npass=0,dovmaxSmth=0,verb=0,idtmax=6,doExtrap=1):

        """
----------------------------------------------------------------------
 routine to smooth input track in lat,lon
 doextrap -- extrap from last point using previous motion to add
 taus  -- similar to nhc_interp.f except done on INuPT to rumterp
----------------------------------------------------------------------
"""
        itaus=itrk.keys()
        itaus.sort()

        btau=itaus[0]

        deftrk={}
        mottrk={}

        jtrk={}

        #  -- check for extra vars
        #
        
        doextra1=0
        doextra2=0
        dor34s=0
        dor50s=0
        dor64s=0
        
        for tau in itaus:

            if(type(tau) is IntType and int(tau)%idtmax != 0): continue

            flat=itrk[tau][0]
            flon=itrk[tau][1]
            fvmax=itrk[tau][2]
            itrkLen=len(itrk[tau])
            
            try:
                fpmin=itrk[tau][3]
            except:
                fpmin=-9999.
                
            # -- detect new BT2 with dir,speed,'TC' and 'NW' in -2 and -1 position
            #
            if(itrkLen == 5):
                fextra1=itrk[tau][-2]
                if(fextra1 != None and not( ( (type(fextra1) is StringType) and len(fextra1) == 2 ) ) ): doextra1=1
            
            if(itrkLen == 6):
                fextra2=itrk[tau][-1]
                if(fextra2 != None and not( ( (type(fextra2) is StringType) and len(fextra2) == 2 ) ) ): doextra2=1
                
        for tau in itaus:

            # -- filter out non 6 h trackers -- hwrf now hoursly 0-9 h, otherwise 3-h
            #    assumed tau was an integer for check --- not true for BT which is DTG
            # -- only do check if int -- assumes dtg are always 6 h
            # -- 20190910 -- add exception 
            if(type(tau) is IntType and int(tau)%idtmax != 0): 
                print 'WWW-ADutils-FcTrackInterpFill -- skipping tau: ',tau
                continue

            flat=itrk[tau][0]
            flon=itrk[tau][1]
            fvmax=itrk[tau][2]
            itrkLen=len(itrk[tau])

            try:
                fvmax=itrk[tau][2]
            except:
                fvmax=-9999.
            if(fvmax == None or fvmax == 0.0): fvmax=-9999.
            
            
            try:
                fpmin=itrk[tau][3]
            except:
                fpmin=-9999.
            if(fpmin == None or fpmin == 0.0): fpmin=-9999.

            
            # -- if itrkLen == 7 then will deal is have the three radii
            #
            if(itrkLen == 7):
                try:
                    fr34s=itrk[tau][4]
                except:
                    fr34s=None
                    
                try:
                    fr50s=itrk[tau][5]
                except:
                    fr50s=None
                    
                try:
                    fr64s=itrk[tau][6]
                except:
                    fr64s=None
                    

            try:
                fextra1=itrk[tau][-2]
            except:
                fextra1=-9999.
                
            if(fextra1 == None): fextra1=-9999.

            try:
                fextra2=itrk[tau][-1]
            except:
                fextra2=-9999.
                
            if(fextra2 == None): fextra2=-9999.

            # -- bounds check on latitude
            #
            if(flat < 85.0 and flat > -85.0):
                
                deftrk[tau]=[flat,flon,fvmax,fpmin]
                
                if(doextra1):
                    deftrk[tau]=[flat,flon,fvmax,fpmin,fextra1]
                    
                if(doextra2):
                    deftrk[tau]=[flat,flon,fvmax,fpmin,fextra1,fextra2]
              
                # -- wind radii
                #
                if(itrkLen == 7):
                    deftrk[tau]=[flat,flon,fvmax,fpmin,fr34s,fr50s,fr64s]
                    
                    

        deftaus=deftrk.keys()
        deftaus=deftrk.keys()
        deftaus.sort()

        ntaus=len(deftaus)

        etau=0
        if(ntaus>1): etau=deftaus[ntaus-1]


        #
        # bail if no forecasts
        #
        if(etau == 0):

            #
            # case of initial position only, return for phr=0...
            #
            try:
                jtrk[etau]=deftrk[etau]
            except:
                jtrk[etau]=[]
            return(jtrk,deftaus)

        #
        # get motion of defined track
        #

        for i in range(0,ntaus):

            tau=deftaus[i]

            i0=i
            ip1=i+1

            if(ntaus > 1):

                if(i0 < ntaus-1):
                    i0=i
                    ip1=i+1

                elif(i0 == ntaus-1):
                    i0=i-1
                    ip1=i

                try:
                    dtau=deftaus[ip1]-deftaus[i0]
                except:
                    dtau=dtgdiff(deftaus[i0],deftaus[ip1])

            else:

                dtau=0.0

            
            if(dtau == 0.0):
                edir=270.0
                espd=0.0
                dvmax=0.0
                dpmin=0.0
                dextra1=0.0
                dextra2=0.0

            else:

                tau0=deftaus[i0]
                tau1=deftaus[ip1]

                flat0=deftrk[tau0][0]
                flon0=deftrk[tau0][1]
                fvmax0=deftrk[tau0][2]
                fpmin0=deftrk[tau0][3]
                
                if(doextra1):
                    fextra10=deftrk[tau0][4]
                    fextra11=deftrk[tau1][4]

                if(doextra2):
                    fextra20=deftrk[tau0][5]
                    fextra21=deftrk[tau1][5]
                    
                # -- wind radii
                #
                if(itrkLen == 7):
                    
                    fr34s0=deftrk[tau0][4]
                    fr34s1=deftrk[tau1][4]
                    
                    fr50s0=deftrk[tau0][5]
                    fr50s1=deftrk[tau1][5]

                    fr64s0=deftrk[tau0][6]
                    fr64s1=deftrk[tau1][6]
                    

                flat1=deftrk[tau1][0]
                flon1=deftrk[tau1][1]
                fvmax1=deftrk[tau1][2]
                fpmin1=deftrk[tau1][3]

                # -- 20190910 -- test for both vmax and pmin, if undef then set to 0.0 or persistence
                #
                if(fvmax1 > 0.0 and fvmax0 > 0.0 ):
                    dvmax=fvmax1-fvmax0
                else:
                    dvmax=0.0
                    
                if(fpmin1 > 0.0 and fpmin0 > 0.0):
                    dpmin=fpmin1-fpmin0
                else:
                    dpmin=0.0
                
                if(doextra1):
                    dextra1=fextra11-fextra10
                
                if(doextra2):
                    dextra2=fextra21-fextra20

                (course,speed,eiu,eiv)=rumhdsp(flat0,flon0,flat1,flon1,dtau)

            #
            # use penultimate motion for end motion
            # set vmax/pmin change to 0.0
            #

            if(i == ip1):
                otau=deftaus[ip1]
                dvmax=0.0
                dpmin=0.0
                if(doextra1): dextra1=0.0
                if(doextra2): dextra2=0.0

            else:
                otau=deftaus[i0]

            mottrk[otau]=[course,speed,dvmax,dpmin]
            if(doextra1):
                mottrk[otau]=[course,speed,dvmax,dpmin,dextra1]
            if(doextra2):
                mottrk[otau]=[course,speed,dvmax,dpmin,dextra1,dextra2]
                
            # -- wind radii --  assume no change in wind radii in the tau interval -- set to beginning
            #
            if(itrkLen == 7):
                mottrk[otau]=[course,speed,dvmax,dpmin,fr34s0,fr50s0,fr64s0]
                

        taus=mottrk.keys()
        taus.sort()
        
        'ffffffffffffffffffffffff',mottrk

        # -- only go out +dtx(3) h at the end for the smoother only
        # -- final extrap after bias corr + smoothing
        #
        
        etau=taus[-1]
        
        if(doExtrap):
            try:    
                etaux=etau+dtx
            except:
                etaux=dtginc(etau,dtx)
        else:
            etaux=etau
            

        try:
            otaus=range(btau,etaux+1,dtx)
        except:
            otaus=dtgrange(btau,dtginc(etaux,1),dtx)

        nt=len(taus)

        n=0
        tau0=taus[n]
        if(nt >= 1): tau1=taus[n+1]

        
        # -- rhumb-line interpolation ""rumterp" to the dtx track (0,3,6,9,12), nhc_interpfcst.f uses linear
        #

        for otau in otaus:

            if(otau == tau0):
                dtau=0

            # -- otau  is beyond the bounding interval
            #

            elif(otau >= tau1):

                atend=0

                # -- increment to set the interval so that otau is equal to tau0 or between tao0 and tau1
                #
                n=n+1
                if(n == nt-1):
                    n=n-1
                    atend=1

                tau0=taus[n]

                #ssssssssssssssssssssssssssssssssssssssssssssssssss -- special treatment

                # -- dtx > delta of deftrk, e.g., deftrk is 3 h from RAP and target is 6 h
                #

                if(tau0 < otau):
                    while(tau0 < otau):
                        n=n+1

                        # -- check if beyond def trk
                        #
                        if(n > nt-1):
                            tau0=taus[-1]
                            n=nt-1
                            break
                        else:
                            tau0=taus[n]

                    # -- check if at end
                    #
                    if(n == nt-1):
                        n=n-1
                        atend=1


                    # -- case where tau0 = otau
                    #
                    if(tau0 == otau): dtau=0

                #ssssssssssssssssssssssssssssssssssssssssssssssssss -- special treatment

                if(nt >= 1): tau1=taus[n+1]

                dtau=0
                #
                # correct handling of extrap point
                #
                if(atend and doExtrap):
                    tau0=tau1
                    tau1=otaus[-1]
                    try:
                        dtau=otau-tau0
                    except:
                        dtau=dtgdiff(tau0,otau)


            else:
                try:
                    dtau=otau-tau0
                except:
                    dtau=dtgdiff(tau0,otau)

            rlat0=deftrk[tau0][0]
            rlon0=deftrk[tau0][1]
            vmax0=deftrk[tau0][2]
            pmin0=deftrk[tau0][3]
            if(doextra1): extra10=deftrk[tau0][4]
            if(doextra2): extra20=deftrk[tau0][5]

            course=mottrk[tau0][0]
            speed=mottrk[tau0][1]
            dvmax=mottrk[tau0][2]
            dpmin=mottrk[tau0][3]
            if(doextra1): dextra1=mottrk[tau0][4]
            if(doextra2): dextra2=mottrk[tau0][5]
            
            # -- wind radii at beginning of interval
            #
            if(itrkLen == 7):
                r34sI=mottrk[tau0][4]
                r50sI=mottrk[tau0][5]
                r64sI=mottrk[tau0][6]

            if(dtau > 0):
                (rlat1,rlon1)=rumltlg(course,speed,dtau,rlat0,rlon0)
                try:
                    dt=float((tau1-tau0))
                except:
                    dt=dtgdiff(tau0,tau1)

                vfact=float(dtau)/dt
                vmax1=vmax0+vfact*dvmax
                pmin1=pmin0+vfact*dpmin
                if(doextra1): extra11=extra10+vfact*dextra1
                if(doextra2): extra21=extra20+vfact*dextra2
                
                # -- do radius interp here -- set to tau0 for now -- use fr??s0 and fr??s1
                #
                if(itrkLen == 7):
                    r34sI=mottrk[tau0][4]
                    r50sI=mottrk[tau0][5]
                    r64sI=mottrk[tau0][6]
                
            else:
                rlat1=rlat0
                rlon1=rlon0
                vmax1=vmax0
                pmin1=pmin0
                if(doextra1): extra11=extra10
                if(doextra2): extra21=extra20
                vfact=0.0
                
                # -- wind radii for dtau = 0
                #
                if(itrkLen == 7):
                    r34sI=mottrk[tau0][4]
                    r50sI=mottrk[tau0][5]
                    r64sI=mottrk[tau0][6]

            #
            # make sure
            #

            jtrk[otau]=[rlat1,rlon1,vmax1,pmin1]

            if(doextra1):
                jtrk[otau]=[rlat1,rlon1,vmax1,pmin1,extra11]
                
            if(doextra2):
                jtrk[otau]=[rlat1,rlon1,vmax1,pmin1,extra11,extra21]
            
            # -- wind radii -- the 'interpolated' from above
            #
            if(itrkLen == 7):
                jtrk[otau]=[rlat1,rlon1,vmax1,pmin1,r34sI,r50sI,r64sI]

        rlats=self.Dic2list(jtrk,0)
        srlats=self.Smth121(rlats,npass)

        rlons=self.Dic2list(jtrk,1)
        srlons=self.Smth121(rlons,npass)

        vmaxs=self.Dic2list(jtrk,2)
        if(dovmaxSmth):
            svmaxs=self.Smth121(vmaxs,npass)
        else:
            svmaxs=vmaxs

        pmins=self.Dic2list(jtrk,3)
        spmins=self.Smth121(pmins,npass)

        if(doextra1):
            extra1s=self.Dic2list(jtrk,4)
            sextra1s=self.Smth121(extra1s,npass)

        if(doextra2):
            extra2s=self.Dic2list(jtrk,5)
            sextra2s=self.Smth121(extra2s,npass)

        self.List2Dict(jtrk,srlats,0)
        self.List2Dict(jtrk,srlons,1)
        self.List2Dict(jtrk,svmaxs,2)
        self.List2Dict(jtrk,spmins,3)
        if(doextra1): self.List2Dict(jtrk,sextra1s,4)
        if(doextra2): self.List2Dict(jtrk,sextra2s,5)

        return(jtrk,deftaus)



    #bbbbbbbbbbbbbbbbbbbcccccccccccccccccccccccccccccc
    #
    # bias correct and 3-h interp track from above 
    #
    #bbbbbbbbbbbbbbbbbbbcccccccccccccccccccccccccccccc

    def BiasCorrFcTrackInterpFill(self,jtrk,itrk,deftaus,phr,dtx,
                                  btlat,btlon,btdir,btspd,btvmax,
                                  model,dtg,stm3id,
                                  latlontaucut=0.0,latlontaumin=120.0,latloncorrmin=1.0,  # for lat/lon ghmi
                                  
                                  # -- 20190904 -- can duplicate hwfi with hwfr06 with the older and more
                                  #    standard? setup...
                                  
                                  #latlontaucut=0.0,latlontaumin=24.0,latloncorrmin=0.0,  # for modern models with better small tau errors
                                  vmaxtaucut=0.0,vmaxtaumin=24.0,vmaxcorrmin=200.0,     # bad to make blow up if vmaxCorrScheme not set correctly
                                  dopc=1,vmaxmin=20.0,vmaxCorrScheme='global',verb=0):


        #------------------------------------------------------------------------------------

        def PersistCorr(tau,lat0,lon0,course,speed,
                        latfc,lonfc,
                        pctauend=12,pcmin=0.33):

            (latp,lonp)=rumltlg(course,speed,tau,lat0,lon0)

            if(tau <= pctauend):
                pcorr=pcmin+(1.0-(float(tau)/pctauend))*(1.0-pcmin)
                latpc=(1.0-pcorr)*latfc + pcorr*latp
                lonpc=(1.0-pcorr)*lonfc + pcorr*lonp
                #print 'vvvvvvvvv------------------ ',tau,pcmin,pcorr,' lat: ',latfc,latp,latpc,' lon: ',lonfc,lonp,lonpc
            return(latpc,lonpc)


        # hard-wired from nhc_interp.f for dt=3
        #

        def fiextrap(t,a,b,c):
            x=(2.0*a + t*(4.0*b - c - 3.0*a + t*(c - 2.0*b + a)))/2.0
            return(x)


        def setfvmaxoffact(tau,atend,
                           vmaxtaumin,vmaxtaucut,vmaxcorrmin):

            ftau=float(tau)
            if(vmaxtaumin  > 0.0):

                if((ftau >= vmaxtaucut and ftau <= vmaxtaumin) ):
                    fvmaxofffact=((vmaxtaumin-ftau)/(vmaxtaumin-vmaxtaucut))*(1.0-vmaxcorrmin) + vmaxcorrmin

                elif(ftau > vmaxtaumin or atend):
                    fvmaxofffact=vmaxcorrmin

                elif((ftau < 0) or (ftau >= 0 and ftau < vmaxtaucut) ):
                    fvmaxofffact=1.0

                else:
                    print 'EEEEEEEEEEEEEEEE setfvmaxoffact error'
                    sys.exit()


            else:
                fvmaxofffact=1.0

            if(fvmaxofffact < 0.0): fvmaxofffact=0.0
            if(vmaxtaumin == 0.0):  fvmaxofffact=1.0

            return(fvmaxofffact)



        if(vmaxCorrScheme == 'global'):
            vmaxtaucut=0.0
            vmaxtaumin=72.0
            vmaxcorrmin=0.0
        elif(vmaxCorrScheme == 'lame' or vmaxCorrScheme == 'limited'):
            vmaxtaucut=0.0
            vmaxtaumin=24.0
            vmaxcorrmin=0.0



        #------------------------------------------------------------------------------------


        itaus=itrk.keys()
        itaus.sort()

        otrk=copy.deepcopy(itrk)

        taus=jtrk.keys()
        taus.sort()

        #
        #
        #
        try:
            latoff=btlat-jtrk[phr][0]
            lonoff=btlon-jtrk[phr][1]
            fvmaxoff=btvmax-jtrk[phr][2]

        except:
            print 'WWWWW no jtrk for: ',stm3id,'  dtg: ',dtg,'  phr: ',phr
            return(otrk)



        #print 'OO11111 latoff,lonoff %02f %5.1f %5.1f %6.1f %6.1f :: %6.1f %6.1f '%(phr,btlat,jtrk[phr][0],btlon,jtrk[phr][1],latoff,lonoff)

        if(verb > 2):
            itaus=itrk.keys()
            itaus.sort()
            for tau in itaus:
                # ['2008061806', 9.5, 132.1, 21.0, 0.0, 42.3, 0.100001, 42.3, -16.3001, -38.9, -29.6, 30.0, [-999, -999, -999, -999], [-999, -999, -999, -999]]
                print 'III tau: %03d'%(tau)," %5.1f %6.1f %3.0f"%(itrk[tau][0],itrk[tau][1],itrk[tau][2])
            for tau in taus:
                print 'JJJ tau: %03d'%(tau)," %5.1f %6.1f %3.0f"%(jtrk[tau][0],jtrk[tau][1],jtrk[tau][2])



        jtrknopc={}

        for tau in taus:

            atend=0
            if(tau == taus[-1]): atend=1

            vmoff=0.0
            dtau=tau-phr

            vmoff=setfvmaxoffact(dtau,atend,
                                 vmaxtaumin,vmaxtaucut,vmaxcorrmin)

            factlloff=setfvmaxoffact(dtau,atend,
                                     latlontaumin,latlontaucut,latloncorrmin)
            latbc=jtrk[tau][0]+latoff*factlloff
            lonbc=jtrk[tau][1]+lonoff*factlloff
            vmaxbc=jtrk[tau][2]+fvmaxoff*vmoff

            # -- undef
            #
            if(jtrk[tau][2] <= 0.0):
                vmaxbc=0.0

            jtrknopc[tau]=[latbc,lonbc,vmaxbc]

            latcur=loncur=-999.
            if(dtau >= 3 and dtau <= 12 and dopc):
                (latpc,lonpc)=PersistCorr(dtau,btlat,btlon,btdir,btspd,
                                          latbc,lonbc
                                          )
                latbc=latpc
                lonbc=lonpc

            jtrk[tau][0]=latbc
            jtrk[tau][1]=lonbc
            jtrk[tau][2]=vmaxbc

        # --do the extrap
        #

        xtaus=range(taus[-1],taus[-1]+phr,dtx)

        try:
            etaum1=taus[-2]
        except:
            etaum1=taus[0]


        for xtau in xtaus:
            tm2=xtau-3*dtx
            tm1=xtau-2*dtx
            tm0=xtau-dtx
            jtrknopc[xtau]=[0,0,0]
            jtrk[xtau]=[0,0,0,[],[]]
            for j in range(0,3):
                a=jtrk[tm2][j]
                b=jtrk[tm1][j]
                c=jtrk[tm0][j]
                jtrk[xtau][j]=fiextrap(3,a,b,c)

                try:
                    if(j == 0 and verb):  print 'try',xtau
                except:
                    if(j == 0 and verb): print 'except',xtau
                    jtrk[xtau]=jtrk[taus[-1]]
                    jtrk[xtau][j]=fiextrap(3,a,b,c)

                jtrknopc[xtau][j]=jtrk[xtau][j]

            # -- set radii constant from etau -> last xtau
            #
            #for j in range(3,5):
            #    jtrk[xtau][j]=jtrk[etaum1][j]


        taus=jtrk.keys()
        taus.sort()

        if(verb > 2):
            for tau in taus:
                print 'FFF tau: %03d'%(tau)," lat: %5.1f PC: %5.1f  lon: %6.1f PC: %6.1f"%(jtrk[tau][0],jtrknopc[tau][0],
                                                                                           jtrk[tau][1],jtrknopc[tau][1])

        # -- put out final track; shift radii to phr from tau=0, i.e., do not interpolate but assume forecast unchanged
        #
        if(verb):
            print 'model: ',model,' dtg: ',dtg,' stm3id: ',stm3id,' phr: ',phr,\
                  ' btdir/spd: ',btdir,btspd,' offset: ',latoff,lonoff,'bt lat/lon/vmax: ',btlat,btlon,btvmax

        # -- relabel/recenter 
        #
        for tau in deftaus:
            
            otrk[tau][0]=jtrk[tau+phr][0]
            otrk[tau][1]=jtrk[tau+phr][1]

            # -- make sure intensity does not fall below vmaxmin
            #
            ovmax=jtrk[tau+phr][2]
            if(ovmax < vmaxmin):
                ovmax=vmaxmin
            otrk[tau][2]=ovmax

            # -- do not use interpolated radii; assume the forecast is the constant  
            #
            #otrk[tau][12]=jtrk[tau][3]
            #otrk[tau][13]=jtrk[tau][4]

            if(verb):
                print 'OOO tau: %03d'%(tau)," %5.1f | %6.1f |  %3.0f III:  %5.1f | %6.1f |  %3.0f "%(otrk[tau][0],otrk[tau][1],otrk[tau][2],
                                                                                                     itrk[tau][0],itrk[tau][1],itrk[tau][2]
                                                                                                     )


        return(otrk)
    



class Adeck(ADutils):

    distminHIT=180.0
    distminHIT9X=300.0

    def __init__(self,adeckpathmasks,mD=None,dtgopt=None,taids=None,verb=0,warn=0,doVD=0,
                 skipcarq=1,
                 undef=-9999.,
                 chkb2id=1,
                 mDp1=None,
                 adyear=None,
                 adyearp1=None,
                 dofilt9x=0,
                 prependAid=None,
                 aliases=None,
                 adeckCards=None,
                 ):

        
        #
        # trick to dectect if mask is a list...
        #
        if(type(adeckpathmasks) is ListType):
            adeckpaths=[]
            for adeckpathmask in adeckpathmasks:
                adeckpaths=adeckpaths+glob.glob(adeckpathmask)

        else:
            adeckpaths=glob.glob(adeckpathmasks)

        if(dtgopt != None):
            self.tdtgs=dtgs=dtg_dtgopt_prc(dtgopt,ddtg=6)


        if( (taids != None) and (type(taids) is not(ListType)) ):
            taids=[taids]

        self.mD=mD
        self.mDp1=mDp1

        self.dofilt9x=dofilt9x
        
        self.adyear=adyear
        self.adyearp1=adyearp1

        self.adecks=adeckpaths
        self.dtgopt=dtgopt
        self.taids=taids
        self.verb=verb
        self.warn=warn
        self.skipcarq=skipcarq
        self.undef=undef
        self.chkb2id=chkb2id
        self.aliases=aliases
        self.prependAid=prependAid

        self.initVars()
        if(adeckCards == None):
            self.initAdeckPaths(adeckpaths)
        else:
            self.getCards(adeckCards)
            
        self.initAdeck()

        if(doVD):
            import vdVM
            self.makeVdeck=VD.MakeVdeck
        

    def initVars(self,dob2idchk=0):

        self.dob2idchk=dob2idchk

        self.stm2ids=[]
        self.stm1ids=[]

        self.dtgs=[]
        self.aids=[]

        self.stmdtgs={}
        self.aiddtgs={}
        self.aidstms={}
        self.aidcards={}
        self.aidtaus={}
        self.aidtausStatus={}
        self.aidtrks={}
        self.adeckyears=[]
        self.adeckbasins=[]

    def getCards(self,adeckCards):

        #cards=[]
        #for adeckpath in adeckpaths:
            #(adyear,adbasin)=getAdeckYearBasinFromPath(adeckpath)
            #if(adyear != None):
                #self.adeckyears.append(adyear)
                #self.adeckbasins.append(adbasin)
            
            #try:
                #ttt=open(adeckpath).readlines()
            #except:
                #ttt=None

            #if(cards == None):
                #return
            #else:
                #cards=cards+ttt

        self.cards=adeckCards
        

    def initAdeckPaths(self,adeckpaths):

        cards=[]
        for adeckpath in adeckpaths:
            (adyear,adbasin)=getAdeckYearBasinFromPath(adeckpath)
            if(adyear != None):
                self.adeckyears.append(adyear)
                self.adeckbasins.append(adbasin)
            
            try:
                ttt=open(adeckpath).readlines()
            except:
                ttt=None

            if(cards == None):
                return
            else:
                cards=cards+ttt

        self.cards=cards
        
        self.adeckyears=uniq(self.adeckyears)
        self.adeckbasins=uniq(self.adeckbasins)


    def isValidB2id(self,b2id):

        rc=0
        if(b2id.upper() in Basin2toBasin1.keys()): rc=1
        return(rc)


    def isAidVmaxOnly(self,aid):

        rc=0
        if( aid == None): return(rc)

        if(
            aid.upper() == 'SHF5' or
            aid.upper() == 'SHFR' or
            aid.upper() == 'IVCN' or
            aid.upper() == 'ICON' or
            aid.upper() == 'ST11' or
            aid.upper() == 'ST5D' or
            aid.upper() == 'S5YY' or
            aid.upper() == 'DSHA' or
            aid.upper() == 'DSHN' or
            aid.upper() == 'CCON' or
            aid.upper() == 'DSHW' or
            aid.upper() == 'SHIW' or
            aid.upper() == 'SHIP' or
            aid.upper() == 'S511' or
            aid.upper() == 'S5RI' or
            aid.upper() == 'SHIA' or
            aid.upper() == 'SHIE' or
            aid.upper() == 'SHIN' or
            aid.upper() == 'DSHE' or
# -- 20211028 -- from nhc
            aid.upper() == 'DSNS' or
            aid.upper() == 'SHNS' or
#
            aid.upper() == 'DSHP' or
            aid.upper() == 'CMES' or
            aid.upper() == 'CMSD' or
            aid.upper() == 'SHIU' or
            aid.upper() == 'DSHU' or
            aid.upper() == 'DC30' or
            
            aid.upper() == 'RI20' or
            aid.upper() == 'RI25' or
            aid.upper() == 'RI30' or
            aid.upper() == 'RI35' or
            aid.upper() == 'RI40' or
            aid.upper() == 'RI45' or
            aid.upper() == 'RI55' or
            aid.upper() == 'RI56' or
            aid.upper() == 'RI65' or
            aid.upper() == 'RI70' or
            aid.upper() == 'RIPA' or
            aid.upper() == 'RIDE' or
            aid.upper() == 'RD25' or

            aid.upper() == 'RVCN' or
            aid.upper() == 'RVCX' or
            aid.upper() == 'TVCC' or
            
            aid.upper() == 'IV15' or
            aid.upper() == 'IVCR' or
            aid.upper() == 'LGEM' or
            aid.upper() == 'SPC3' or
            aid.upper() == 'KSF5' or
            aid.upper() == 'KSFR' or
            aid.upper() == 'IVRI' or
            aid.upper() == 'KLGM' or
            aid.upper() == 'KSHP' or
            aid.upper() == 'KDSP' or
            aid.upper() == 'DSHF' or
            aid.upper() == 'CNTR' or
            #aid.upper() == 'PEST' or
            
            aid.upper() == 'TCCN' or
            #aid.upper() == 'SPC3' or
            #aid.upper() == 'SPC3' or
            #aid.upper() == 'SPC3' or
            aid.upper() == 'ICNW' or
            aid.upper() == 'ICNX' or
            aid.upper() == 'RD20' or
            aid.upper() == 'RD30' or
            aid.upper() == 'RD35' or
            aid.upper() == 'RD40' or
            aid.upper() == 'RD45' or
            aid.upper() == 'RD55' or
            aid.upper() == 'RD56' or
            aid.upper() == 'RD65' or
            aid.upper() == 'RD70' or
            aid.upper() == 'FRIA' or
            aid.upper() == 'ICNE' or
            aid.upper() == 'JTWX' or
            
            
            aid.upper() == 'S5XX'

            ): rc=1

        return(rc)




    def makeIposit(self,tt,card,ncards,ntt,verb=0,aid=None,ipositPrev=None):

        def tt2rad(tt):
            try:
                rad=(float(tt[13]),float(tt[14]),float(tt[15]),float(tt[16]))
            except:
                print 'error in tt2rad for tt: ',tt
            return(rad)
            
        #WP, 22, 2014112912, 03, FIM9, 108, 119N, 1385E,  77,  985, XX,  64, NEQ,   95,   69,    0,   85,
        #0    1           2   3     4    5     6      7    8     9  10   11   12    13    14    15    16
        # --------- get tau and lat/lons, vmax, p,in
        #
        try:
            tau=tt[5].strip()
            itau=int(tau)

            # -- basic sanity check, if alat=alon=0, and vmax is not there... noload
            #
            clat=tt[6].strip()
            clon=tt[7].strip()
        except:
            if(self.warn): print 'WWW gooned up card, failed tau,clat,clon: %6i'%(ncards),' card: ',card[0:-1],ntt
            return(None,None)

        try:     vmax=float(tt[8])
        except:  vmax=self.undef
        
        if(vmax == 0):
            vmax=self.undef

        try:
            (alat,alon)=Clatlon2Rlatlon(clat,clon)
        except:
            # -- set  blank clat,clon to 0.0 for next check
            #
            if(clat == '' and clon == ''):
                alat=0.0
                alon=0.0
            else:
                if(self.warn): print 'WWW gooned up clat,clon: %6i'%(ncards),'clat,clon: ',clat,clon,'card: ',card[0:-1],'ntt: ',ntt
                return(None,None)

        if((alat == 0.0 and (alon == 0.0 or alon == 360.0)) and not(self.isAidVmaxOnly(aid)) ):
            if(self.warn): print 'WWW(Adeck.makeIpost): 0N 0W NOLOAD aid: ',aid,'isVmaxOnly: ',self.isAidVmaxOnly(aid),'card: ',card[:-1]
            return(None,None)

        #if(alat == 0.0 and (alon == 0.0 or alon == 360.0) and vmax == 0.0):
        #    if(verb): print '0N 0W Vmax0 NOLOAD : ',card[:-1]
        #    return(None,None)

        try:      pmin=float(tt[9])
        except:   pmin=self.undef
        if(pmin == 0.0): pmin=self.undef

        # -- pull r34 by default if ipositPrev == None
        #
        if(ipositPrev == None):
            
            r34=None
            r50=None
            r64=None

            #r34=(self.undef,self.undef,self.undef,self.undef)
            #r50=(self.undef,self.undef,self.undef,self.undef)
            #r64=(self.undef,self.undef,self.undef,self.undef)

            try:
                if(len(tt) > 16 and int(tt[11]) == 34 and tt[12].strip() == 'NEQ'): r34=tt2rad(tt)
            except:
                if(self.warn):
                    print 'WWW(Adeck.makeIpost): bad card in getting r34 -- aid: ',aid,'card: ',card[:-1]
                    print 'WWW(Adeck.makeIpost): setting r34/r50/r64 to undef...'
            try:
                if(len(tt) > 16 and int(tt[11]) == 50 and tt[12].strip() == 'NEQ'): r50=tt2rad(tt)
            except:
                if(self.warn):
                    print 'WWW(Adeck.makeIpost): bad card in getting r34 -- aid: ',aid,'card: ',card[:-1]
                    print 'WWW(Adeck.makeIpost): setting r34/r50/r64 to undef...'
                
            try:
                if(len(tt) > 16 and int(tt[11]) == 64 and tt[12].strip() == 'NEQ'): r64=tt2rad(tt)
            except:
                if(self.warn):
                    print 'WWW(Adeck.makeIpost): bad card in getting r34 -- aid: ',aid,'card: ',card[:-1]
                    print 'WWW(Adeck.makeIpost): setting r34/r50/r64 to undef...'
                        
            iposit=(alat,alon,vmax,pmin,r34,r50,r64)

        # -- !!!!!!!! - need to add code class Adeck to pass in previous iposit to check if only updating r50,r64
        #
        else:

            print 'WWWWWWWWWWWWWWWWXXXXXXXXXXXXXXXXXXx - no code to handle passing in prevIposit into Adeck.makeIposit...bye'
            sys.exit()
            r34=(self.undef,self.undef,self.undef,self.undef)
            r50=(self.undef,self.undef,self.undef,self.undef)
            r64=(self.undef,self.undef,self.undef,self.undef)
            
            if(len(tt) > 16):
                if(int(tt[11]) == 34 and tt[12].strip() == 'NEQ'): r34=tt2rad(tt)
                if(int(tt[11]) == 50 and tt[12].strip() == 'NEQ'): r50=tt2rad(tt)
                if(int(tt[11]) == 64 and tt[12].strip() == 'NEQ'): r64=tt2rad(tt)
                
            iposit=(alat,alon,vmax,pmin,r34,r50,r64)

        return(itau,iposit)


    def setDtgNCard(self,tt):
        dtg=tt[2].strip()
        if(len(dtg) != 10):
            return(None)

        return(dtg)



    def makeBidDtg(self,tt,card,maxPrevYearDtgdiff=240.0):

        b2id=tt[0].strip()
        bnum=tt[1].strip()
        bnumi=bnum
        ibnum=bnum

        # check for ** in b2id  -- from rerun of tracker on tacc?
        #
        if(b2id == '**'):
            if(self.dob2idchk):
                print """EEEEEEEEEEE b2id check gives '**', we'll stop in initAdeck, until you mod the code want to just continue"""
                print 'card: ',card
                sys.exit()
            else:
                b2id='XX'

        elif(b2id.isdigit()):
            if(self.warn): print 'WWW --adeck-- gooned up acard: 2-char basin is a number: ',card[:-1],' ...'
            return(None)

        if(not(self.isValidB2id(b2id)) and self.chkb2id):
            if(self.warn): print 'WWW --adeck-- gooned up acard: 2-char basin is NOT standard: ',card[0:-1],' ...'
            return(None)

        #  check for unspecified bnum, e.g., when b2id == '**'
        #
        if(len(bnum) == 2):

            # -- handle new [A-Z][0-9] for 9X
            #
            bnum1=bnum[0].upper()
            if(ord(bnum1) >= 65 and ord(bnum1) <= 90):
                try:
                    bnum=90+int(bnum[1])
                    bnum=str(bnum)
                except:
                    print 'WWW bad acard in makeBidDtg(bad ord(bnum1): ',card[:-1],' bnum not defined...onward...'
                    return(None)

            try:      
                int(bnum)
            except:   
                print 'WWW bad acard in makeBidDtg(non int): ',card[:-1],' bnum not defined...onward...'
                return(None)

        # -- case when 3-char id in the basin id in the 'sink' format
        #
        elif(len(bnum) == 3):
            if(type(bnumi[0]) is str):
                bnumi="9%s"%(bnumi[1:])
            try:
                ibnum=int(bnumi[0:2])
                bnum=bnum[0:2]
            except:
                print 'WWW 333333 bad acard(Adeck): ',bnum,card[:-1],' bnum not defined...onward...'
                return(None)

        elif(len(bnum) >= 4):
            try:
                ibnum=int(bnum[0:2])
                bnum=bnum[0:2]
            except:
                print 'WWW 44444 bad acard: ',bnum,card[:-1],' bnum not defined...onward...'
                return(None)

        # -- case when 1-char id in the basin id in the 'sink' format
        #
        elif(len(bnum) == 1):
            try:
                ibnum=int(bnum[0])
                bnum="%02d"%(ibnum)
                print 'WWW single bnum: ',bnum,'stm2id: ',stm2id
            except:
                print 'WWW 111111 bad bnun in acard: ',bnum,card[:-1],' bnum not defined...onward...'
                return(None)

        # -- blank bnum
        #
        elif(len(bnum) == 0):
            print 'WWW 000000 bad bnum in acard: ',bnum,card[:-1],' bnum 0 length...onward...'
            return(None)

        # -- filter out 8X storms
        #
        if(ibnum >= 80 and ibnum <= 89): return(None)

        # -- check if adeck uses sss.yyyy form of storm id vice standard 2-char stm id
        #

        if(len(bnum.split('.')) == 2):
            bn=bnum.split('.')[0]
            b1=bn[2]
            bn=bn[0:2]
            by=bnum.split('.')[1]
            bnum=bn

        # -- 9999999999999999999999999999999999 filter out 9X
        #
        if(self.dofilt9x and Is9XSnum(bnum)): return(None)
        
        dtg=self.setDtgNCard(tt)
        if(dtg == None):
            print 'WWW Adeck().setDtgNCard bad dtg: ',dtg,card 
            return(None)


        byear=dtg[0:4]
        # -- handle shem...
        #
        stm2id="%s%s.%s"%(b2id,bnumi,byear)
        if(isShemBasinStm(stm2id)):  byear=getShemYear(dtg)
        
        # -- if not an adeck use -- return
        #
        if(not(hasattr(self,'adyear'))):
            #print '11111111111111111111 ',dtg,b2id,bnumi,byear
            return(dtg,b2id,bnumi,byear)
        
        # -- check byear for storms starting in previous year
        #
        if( (self.adyear != None and self.adyearp1 != None) ):

            yeardiffSH=0
            isSH=isShemBasinStm(b2id)
            if(isSH):  yeardiffSH=int(dtg[0:4])-int(self.adyear)

            yeardiff=int(byear)-int(self.adyear)

            if(yeardiff == -1 and not(isSH)):
                prevYearDtgdiff=dtgdiff(dtg,"%4s010100"%(self.adyear[0:4]))
                if(prevYearDtgdiff > maxPrevYearDtgdiff):
                    print 'WWW Adeck().makeBidDtg() !!!!!!!!!!!!!!!!!!!!!! storm dtg < ',self.adyear,' prevYearDtgdiff: %4.0f'%(prevYearDtgdiff),\
                          ' > maxPrevYearDtgdiff: %4.0f'%(maxPrevYearDtgdiff),' card: ',card[0:40],'...press...'
                    return(None)
                else:
                    print 'WWW Adeck().makeBidDtg() storm dtg < ',self.adyear,' set to self.adyear when prevYearDtgdiff: %4.0f'%(prevYearDtgdiff),\
                          ' < maxPrevYearDtgdiff: %4.0f'%(maxPrevYearDtgdiff),' card: ',card[0:40]
                byear=self.adyear
            elif(yeardiffSH < -1):
                print 'EEE  Adeck().makeBidDtg() year diff too big for card: ',card[0:70]
                return(None)
            
        # -- check if byear in the adeckyears implied by the adeckpaths...if not, bail
        #
        if(len(self.adeckyears) > 0 and not(byear in self.adeckyears)): 
            print 'WWW Adeck.makeBidDtg byear of the storm NOT in the year implied by the adeck file name...press...',card[0:48]
            return(None)

        #print 'llllllllllllllllll',dtg,b2id,bnumi,byear
        return(dtg,b2id,bnumi,byear)


    def setAidNCard(self,tt):
        aid=tt[4].strip()
        return(aid)


    def makeAid(self,tt,card):

        aid=self.setAidNCard(tt)
        aid=aid.lower()


        # -- filter out carq
        #
        gotaid=0
        if(self.skipcarq and aid == 'carq'):
            return(gotaid,None,None)

        # -- aliases
        #
        if(self.aliases != None):
            for k in self.aliases.keys():
                if(aid == k):
                    oaid=self.aliases[k].upper()
                    iaid=aid.upper()

                    # -- convert 3-char aid -> 4-char
                    #
                    if(len(aid.upper()) <= 3): iaid="%4s"%(iaid)
                    card=card.replace(iaid,oaid)

                    # -- case where iaid is lowercase in card
                    #
                    card=card.replace(aid,oaid)
                    aid=oaid.lower()


        # --- replace _ with X in aid name
        #
        if(aid.replace('_','X')):
            aid=aid.replace('_','X')

        if(self.taids != None):
            gotaid=0
            for taid in self.taids:
                if(aid == taid):
                    gotaid=1
                    break
        else:
            gotaid=1

        return(gotaid,aid,card)


    def initAdeck(self,skipcarq=1,nlenmin=6,nlenmax=-999,filtHiFreq=1,maxDtau=6,verb=0):

        """  main method that parses the adeck cards and associates 9X storms with real NN storms using
        the mdeck object mD that has dicts and methods to get bt lat/lons

        """
        iposits={}
        
        ncards=1
        for card in self.cards:

            tt=card.split(',')
            ntt=len(tt)
            
            # -- check for blank card
            #
            if(ntt <= 1):
                continue
                
            # -- check for short cards
            #
            if(ntt <= nlenmin):
                print 'WWW short adeck card # ',ncards,card[:-1]
                continue

            #  -- check for long cards -- problem on jet/nccs in io from marchok tracker
            #
            if(nlenmax > 0 and ntt > nlenmax):
                print 'WWW LONG  adeck card # ',ncards,card[:-1]
                continue


            # -- get bid, dtg
            #
            rc=self.makeBidDtg(tt,card)
            if(rc == None): continue
            (dtg,b2id,bnum,byear)=rc

            # -- get aid
            #
            (gotaid,aidin,card)=self.makeAid(tt,card)
            if(hasattr(self,'prependAid')):
                if(self.prependAid != None):
                    aid="%1s%s"%(self.prependAid,aidin)
                else:
                    aid=aidin
            else:
                aid=aidin 
            
            if(self.aliases != None):
                try:
                    aidout=self.aliases[aidin.upper()]
                    card=card.replace(aidin.upper(),aidout,1)
                except:
                    None
            

            if(gotaid == 0): continue

            # -- get posit list
            #
            (itau,iposit)=self.makeIposit(tt,card,ncards,ntt,aid=aid)
            
            
            # -- filter out hi-frequency, e.g., hwrf in 2014 hourly 0-9 then 3 hourly
            #
            if(filtHiFreq and itau != None):
                if(itau%maxDtau != 0): continue
                
                
            if(itau == None): continue


            b2id=basin2Chk(b2id)

            stm2id="%s%s.%s"%(b2id,bnum,byear)
            stm2id=stm2id.lower()

            #######if(self.verb): print 'AAA ',aid,dtg,stm2id,itau
            # -- put correct 2-char basin in the input card
            #
            card=b2id+card[2:]

            # --- make lists and dicts
            #
            self.appendList(self.dtgs,dtg)
            self.appendList(self.stm2ids,stm2id)
            self.appendList(self.aids,aid)

            self.appendDictList(self.stmdtgs,stm2id,dtg)
            self.appendDictList(self.aiddtgs,(aid,stm2id),dtg)
            self.appendDictList(self.aidstms,aid,stm2id)
            self.appendDictList(self.aidtaus,(aid,stm2id,dtg),itau)

            self.append2KeyDictList(self.aidcards,(aid,stm2id),dtg,card)
            #self.append3KeyDictList(self.aidtrks,(aid,stm2id),dtg,itau,iposit)
            self.append3TupleKeyDictList(iposits,(aid,stm2id),dtg,itau,iposit)

            ncards=ncards+1
            
        kk=iposits.keys()
        kk.sort()
        for k in kk:
            k1=k[0]
            k2=k[1]
            k3=k[2]
            posits=iposits[k]
            
            r34Final=r50Final=r64Final=None
            
            if(len(posits) == 1):
                iposit=posits[0]
                if(verb):
                    print '1111111111',k1,k2,k3,'111: ',iposit
                
            elif(len(posits) == 2):
                
                iposit1=posits[0]
                iposit2=posits[1]
                
                r341=iposit1[-3]
                r501=iposit1[-2]
                r641=iposit1[-1]
                
                r342=iposit2[-3]
                r502=iposit2[-2]
                r642=iposit2[-1]
                
                if(verb):
                    print '2222222222',k1,k2,k3,'111: ',iposit1,' 222: ',iposit2
                    print '2222222222 r341:',r341,' r501: ',r501,' r641: ',r641
                    print '2222222222 r342:',r342,' r502: ',r502,' r642: ',r642
                    
                if(r341 != None): r34Final=r341
                if(r342 != None): r34Final=r342
                
                if(r501 != None): r50Final=r501
                if(r502 != None): r50Final=r502
                
                if(r641 != None): r64Final=r641
                if(r642 != None): r64Final=r642

                iposit=list(iposit1)
                iposit[-3]=r34Final
                iposit[-2]=r50Final
                iposit[-1]=r64Final
                iposit=tuple(iposit)

                
            elif(len(posits) == 3):

                iposit1=posits[0]
                iposit2=posits[1]
                iposit3=posits[2]

                r341=iposit1[-3]
                r501=iposit1[-2]
                r641=iposit1[-1]
                
                r342=iposit2[-3]
                r502=iposit2[-2]
                r642=iposit2[-1]
                
                r343=iposit3[-3]
                r503=iposit3[-2]
                r643=iposit3[-1]
                
                if(verb):
                    print '33333333',k1,k2,k3,'111: ',iposit1,' 222: ',iposit2
                    print '33333333 r341:',r341,' r501: ',r501,' r641: ',r641
                    print '33333333 r342:',r342,' r502: ',r502,' r642: ',r642
                    print '33333333 r343:',r343,' r503: ',r503,' r643: ',r643
                    
                if(r341 != None): r34Final=r341
                if(r342 != None): r34Final=r342
                if(r343 != None): r34Final=r343
                
                if(r501 != None): r50Final=r501
                if(r502 != None): r50Final=r502
                if(r503 != None): r50Final=r503
                
                if(r641 != None): r64Final=r641
                if(r642 != None): r64Final=r642
                if(r643 != None): r64Final=r643
                
                iposit=list(iposit1)
                iposit[-3]=r34Final
                iposit[-2]=r50Final
                iposit[-1]=r64Final
                
                iposit=tuple(iposit)
                
            if(verb): print 'FFFFFFFFF ',k1,k2,k3,iposit
            
            self.append3KeyDictList(self.aidtrks,k1,k2,k3,iposit)
                
        # --- uniq
        #

        self.dtgs=self.uniq(self.dtgs)
        self.aids=self.uniq(self.aids)
        self.stm2ids=self.uniq(self.stm2ids)
        self.uniqDictList(self.aidtaus)

        for stm2id in self.stm2ids:
            temp=self.uniq(self.stmdtgs[stm2id])
            self.stmdtgs[stm2id]=temp

        for aid in self.aids:
            for stm2id in self.stm2ids:
                try:
                    temp=self.uniq(self.aiddtgs[aid,stm2id])
                    self.aiddtgs[aid,stm2id]=temp
                except:
                    iok=0

        for aid in self.aids:
            self.aidstms[aid]=self.uniq(self.aidstms[aid])


        for stm2id in self.stm2ids:
            self.stm1ids.append(stm2idTostm1id(stm2id))

        self.dtgs.reverse()
        self.aids.sort()

        self.naids=len(self.aids)
        self.ndtgs=len(self.dtgs)

    #eeeeeeeeeeeeeeeee end of initAdeck methed




    def relabelAidcards(self,warn=1):

        for (aid,stm2id) in self.aiddtgs.keys():
            dtgs=self.aiddtgs[aid,stm2id]
            snum=int(stm2id[2:4])
            for dtg in dtgs:
                acards=self.aidcards[aid,stm2id][dtg]
                tau0=self.aidtaus[aid,stm2id,dtg][0]
                posit0=self.aidtrks[aid,stm2id][dtg][tau0]

                if(tau0 != 0 and warn):
                    print 'WWW AD.Adeck.relabelAidcards() initial tau for aid: ',aid,' stm2id: ',stm2id,' dtg: ',dtg,' tau0: ',tau0,' posit0: ',posit0,' MISSING'

                if(int(snum) >= 90 and int(snum) <=99):
                    alat=posit0[0]
                    alon=posit0[1]
                    self.relabel9X(stm2id,dtg,alat,alon)
                    if(self.gothit):
                        self.relabelAcards(acards,aid,stm2id,dtg)


    def getAiddtgsFromAidcards(self,tag=''):

        aiddtgs={}
        kk=self.aidcards.keys()
        kk.sort()
        for k in kk:
            (aid,stm2id)=k
            bnum=int(stm2id[2:4])
            if(bnum >= 80): continue
            kkk=self.aidcards[k]
            dtgs=kkk.keys()
            dtgs.sort()
            aiddtgs[k]=dtgs

        return(aiddtgs)


    def cmpAiddtgs(self,Bdtgs,Adtgs):
        astms=Adtgs.keys()
        bstms=Bdtgs.keys()

        allstms=astms+bstms
        allstms=self.uniq(allstms)

        for stm in allstms:
            try:    bds=Bdtgs[stm]
            except: bds=[]

            try:    ads=Adtgs[stm]
            except: ads=[]

            try:    aldtg=ads[-1]
            except: aldtg='None      '

            try:    bldtg=bds[-1]
            except: bldtg=' --None--  '

            print 'Stm: ',stm,"Before: %3d  After: %3d   Bldtg: %s  Aldtg: %s "%(len(bds),len(ads),bldtg,aldtg)



    def lsAidcards(self,tag='',dtgopt=None,warn=0):

        if(dtgopt != None):
            dtgs=dtg_dtgopt_prc(dtgopt,ddtg=6)

        # -- new method to print the cards
        #
        if(hasattr(self,'acards')):
            
            kk=self.acards.keys()
            kk.sort()
    
            for k in kk:
                if(dtgopt == None or (dtgopt != None and  k in dtgs) ):
                    print
                    print 'bdtg: ',k,' aid: ',self.aid
                    cc=self.acards[k]
                    for c in cc:
                        print c[:-1]

        elif( (hasattr(self,'aidcards') and self.aidcards != None) and 
              (hasattr(self,'aiddtgs') and self.aiddtgs != None)
              ):

            # -- older form
            kk=self.aidcards.keys()
    
            for (aid,stm2id) in kk:
                bnum=int(stm2id[2:4])
                if(bnum >= 80): continue
                dtgs=self.aiddtgs[aid,stm2id]
                snum=stm2id[2:4]
                for dtg in dtgs:
                    print
                    print 'bdtg: ',dtg,' aid: ',self.taid
                    acards=self.aidcards[aid,stm2id][dtg]
                    for acard in acards:
                        print acard[0:156],'...'
                    #taus=self.aidtaus[aid,stm2id,dtg]
                    #posits=self.aidtrks[aid,stm2id][dtg]
                    
        else:
            if(warn):
                print   
                print 'IIIIIIIII' 
                print 'IIIIIIIIIIIIIII adCL.Adeck.lsAidcards -- no acards in newer AD for ',self.taid
                print 'IIIIIIIII' 
                


    def relabel9X(self,stm2id,dtg,alat,alon,verb=0):

        try:
            #tcs=self.mD.stm2dtg[dtg]
            tcs=self.mD.getTC2idsFromDtg(dtg,dofilt9x=1)
        except:
            print 'WWW no tcs for stm2id: ',stm2id,' for dtg: ',dtg
            self.gothit=0
            self.nstm2id=stm2id
            return


        stms=tcs.keys()

        distmin=1e20
        gothit=0
        for stm in stms:
            tt=tcs[stm]
            blat=tt[0]
            blon=tt[1]
            dist=gc_dist(blat,blon,alat,alon)
            if(dist < distmin):
                distmin=dist
                stm2idmin=stm

            if(verb): print 'RRRRRRRR ',stm2id,stm,dtg,alat,alon,blat,blon,dist,self.distminHIT,self.distminHIT9X
            if(distmin < self.distminHIT or
               (stm2id[2] == '9' and (distmin < self.distminHIT9X)) ):
                gothit=1


        if(gothit):
            if(verb): print 'HHHHHHHHHHH(relabel9X) ','stm2id: ',stm2id,' ==> nstm2id: ',stm2idmin," distmin: %6.2f"%(distmin),' dtg: ',dtg

        else:
            gohit=0
            stm2idmin=stm2id
            if(self.warn):
                print 'WWW in AD: could not find storm for stm2id: ',stm2id,' do not set here... ',alat,alon,dtg

        self.gothit=gothit
        self.nstm2id=stm2idmin



    def relabelAcards(self,acards,aid,stm2id,dtg):

        isnum=stm2id[2:4]

        ob2id=stm2id[0:2].upper()
        osnum=self.nstm2id[2:4]

        ostmid="%s, %s, "%(ob2id,osnum)

        #print '---------------------------------------------: ',ostmid,self.nstm2id,len(acards)

        ocards=[]
        for card in acards:
            istmid="%s, %s, "%(card[0:2],isnum)
            ncard=card.replace(istmid,ostmid)
            ocards.append(ncard)

        for ocard in ocards:
            self.append2KeyDictList(self.aidcards,(aid,self.nstm2id),dtg,ocard)


    def getAidTrk(self):


        try:
            ats=self.ats
        except:
            ats={}


        if(len(ats) == 0):
            AT=AidTrk()
            if(hasattr(self,'taid')):
                AT.aid=self.taid
            else:
                AT.aid='undef'
            return(AT)

        trks=ats

        dtgs=trks.keys()
        dtgs.sort()

        AT=AidTrk(dtgs,trks)

        if(hasattr(self,'taid')):
            AT.aid=self.taid
        else:
            AT.aid='undef'

        if(hasattr(self,'tstmid')):
            AT.stmid=self.tstmid
        else:
            AT.stmid='undef'

        return(AT)


    def getBestTrk(self):

        from tcCL import BestTrk
        
        try:
            btcs=self.bts
        except:
            btcs=None

        if(btcs != None):
            dtgs=btcs.keys()
            BT=BestTrk(dtgs,btcs)
            if(hasattr(self,'tstmid')):
                BT.stmid=self.tstmid
            else:
                BT.stmid='undef'
        else:
            BT=BestTrk()
            BT.stmid='undef'

        return(BT)



    def GetAidTrks(self,aid,stm2id=None,stm1id=None,verb=0):


        if(stm2id == None and stm1id != None): stm2id=stm1idTostm2id(stm1id)
        if(stm1id == None and stm2id != None): stm1id=stm2idTostm1id(stm2id)

        try:
            trks=self.aidtrks[aid,stm2id]
        except:
            trks={}


        if(len(trks) == 0):
            AT=AidTrk()
            AT.aid=aid
            AT.stmid=stm1id
            return(AT)

        dtgs=trks.keys()
        dtgs.sort()

        AT=AidTrk(dtgs,trks)
        AT.aid=aid
        AT.stmid=stm1id

        return(AT)


    def getBestTrks(self,stm1id):


        try:
            btcs=self.bts
        except:
            btcs=None

        if(btcs != None):
            dtgs=btcs.keys()
            BT=BestTrk(dtgs,btcs)
            BT.stmid=stm1id
        else:
            BT=BestTrk()

        return(BT)



    def GetAidStmids(self,taid):

        stmids=[]

        try:
            stm2ids=self.aidstms[taid]
        except:
            stm2ids=[]

        for tstm in stm2ids:
            stm1id=self.getAidStm1idFromStm2id(taid,tstm)
            if(stm1id != None):
                stmids.append(stm1id)

        stmids=self.uniq(stmids)

        return(stmids)


    def GetAidCards(self,aid,stm1id):

        try:
            stm2ids=self.stm1ids[stm1id.lower()]
        except:
            stm2id=stm1idTostm2id(stm1id.lower())
            stm2ids=[stm2id]

        stm2ids.sort()

        allcards={}

        for stm2id in stm2ids:
            try:
                acards=self.aidcards[aid,stm2id]
            except:
                acards={}

            allcards=self.DictAdd(allcards,acards,priority=1)

        return(allcards)



    def GetEaids(self,model,dtg=None,ncepSource='adeck',verb=0):

        iaids=self.aids
        eaids=[]
        if(model == 'esrl'):
            for iaid in iaids:
                if(verb): print 'iaid ',iaid
                if( (iaid[0:2].upper() == 'F8' and iaid[2:4].isdigit()) or iaid[0:4].upper() == 'F8EM' ):
                    eaids.append(iaid)

        elif((model == 'ncep' or model == 'nhc') and find(ncepSource,'adeck') ):
            for iaid in iaids:
                if(verb): print 'iaid ',iaid
                if( (iaid[0:2].upper() == 'AP' and iaid[2:4].isdigit()) or iaid.upper() == 'AC00'):
                    eaids.append(iaid)

        elif(find(model,'cmc') and ncepSource == 'adeck'):
            for iaid in iaids:
                if(verb): print 'iaid ',iaid
                if( (iaid[0:2].upper() == 'CP' and iaid[2:4].isdigit()) or iaid.upper() == 'CC00'):
                    eaids.append(iaid)

        else:
            for iaid in iaids:
                if(verb): print 'iaid ',iaid
                if(iaid != 'ecmt' and iaid != 'ecfx' and iaid != 'edet' and iaid != 'eanl' ):
                    eaids.append(iaid)

        eaids.sort()

        self.ensembleAids=eaids

        return(eaids)


    def GetDetaid(self,model,dtg,ncepSource='adeck',verb=0):

        iaids=self.aids

        if(model == 'esrl'):
            daid=None
            sdaids=['f9em','f8em']
            for iaid in iaids:
                for sdaid in sdaids:
                    if(iaid == sdaid):
                        daid=sdaid

        elif(model == 'ncep' and find(ncepSource,'adeck') ):
            daid=None
            sdaids=['avno','avni']
            for iaid in iaids:
                for sdaid in sdaids:
                    if(iaid == sdaid):
                        daid=sdaid

        elif(model == 'ukmo'):
            daid=None
            sdaids=['ukm','egrr']
            for iaid in iaids:
                for sdaid in sdaids:
                    if(iaid == sdaid):
                        daid=sdaid


        elif(model == 'cmc' and ncepSource == 'adeck'):
            daid=None
            sdaids=['cmc']
            for iaid in iaids:
                for sdaid in sdaids:
                    if(iaid == sdaid):
                        daid=sdaid

        else:
            daid='edet'

        self.deterministicAid=daid
        return(daid)



    def writeAcards(self,taids=None,tstms=None,
                    tdir='/tmp',
                    odtgs=None,
                    dowrite=0,
                    tag=None,
                    aliases=None,
                    verb=0):

        if(taids == None):
            taids=self.aids
        if(tstms == None):
            tstms=self.stm2ids


        def corrVmaxPmin(card):

            tt=card.split(',')
            vmax=tt[8]
            pmin=tt[9]

            if(vmax == ' ***'): tt[8]='    '
            if(pmin == '  -99'): tt[9]='     '

            ocard=''
            for n in range(0,len(tt)):
                t1=tt[n]
                if(n == len(tt)-1):
                    ocard="%s%s"%(ocard,t1)
                else:
                    ocard="%s%s,"%(ocard,t1)

            return(ocard)



        cards=[]

        for tstm in tstms:

            if(tag != None):  cards=[]

            for taid in taids:

                otaid=taid
                if(aliases != None):
                    for (iname,oname) in aliases:
                        if(taid.upper() == iname.upper()): otaid=oname.upper()

                acards=self.aidcards[taid,tstm]

                dtgs=acards.keys()
                dtgs.sort()

                for dtg in dtgs:
                    acds=acards[dtg]
                    for acd in acds:

                        acd=corrVmaxPmin(acd)
                        # the b2id in the adeck card is NOT changed, just the stm2id
                        # do the conversion here
                        #
                        b2id=acd[0:2]
                        b2id=basin2Chk(b2id)
                        acd=b2id+acd[2:]
                        if(aliases != None):
                            acd=acd.replace(taid.upper(),otaid)
                        if(verb): print acd[0:-1]
                        cards.append(acd)

                stm2id=tstm

                if(tag == None):
                    fpath="%s/a%s_%s.dat"%(tdir,stm2id.replace('.',''),otaid.lower())
                    MF.WriteList2File(cards,fpath,verb=1)

            if(tag != None):
                fpath="%s/a%s_%s.dat"%(tdir,stm2id.replace('.',''),tag)
                MF.WriteList2File(cards,fpath,verb=1)


class AdeckFromCards(Adeck):
    
    distminHIT=180.0
    distminHIT9X=300.0

    def __init__(self,acards,
                 mD=None,
                 dtgopt=None,
                 taids=None,
                 verb=0,warn=1,doVD=0,
                 skipcarq=1,
                 undef=-9999.,
                 chkb2id=1,
                 mDp1=None,
                 adyear=None,
                 adyearp1=None,
                 dofilt9x=0,
                 prependAid=None,
                 aliases=None):

        

        self.dofilt9x=dofilt9x
        
        self.adyear=adyear
        self.adyearp1=adyearp1

        self.cards=acards
        self.dtgopt=dtgopt
        self.taids=taids
        self.verb=verb
        self.warn=warn
        self.skipcarq=skipcarq
        self.undef=undef
        self.chkb2id=chkb2id
        self.aliases=aliases
        self.prependAid=prependAid

        self.initVars()
        self.initAdeck()


    def initVars(self,dob2idchk=0):

        self.dob2idchk=dob2idchk

        self.stm2ids=[]
        self.stm1ids=[]

        self.dtgs=[]
        self.aids=[]

        self.stmdtgs={}
        self.aiddtgs={}
        self.aidstms={}
        self.aidcards={}
        self.aidtaus={}
        self.aidtrks={}
        self.adeckyears=[]
        self.adeckbasins=[]



#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc -- Adeck
# main classes
#


class MDdataset(MFbase):

    undef=-999.
    
    def __init__(self,dtgs,stm2id):

        self.dtgs=dtgs
        self.stm2id=stm2id
        self.stm1id=stm2idTostm1id(stm2id)
        
        self.cq00={}
        self.cq12={}
        self.cq24={}
        self.best={}
        self.wrng={}
        self.of00={}
        self.of03={}
        self.of12={}
        self.of24={}


    def setMDtrk(self,verb=0,docq00=1,btonly=0,only6h=1,useVmax4TcCode=1,
                 dob1idSet=0):

        # -- look for breaks in the dtg
        #
        self.dtgs=self.chkDtgBreaks(self.dtgs,verb=verb)
        
        dtgs=self.dtgs
        dtgs.sort()

        ndtgs=len(dtgs)

        if(only6h):
            dtgs=[]
            for dtg in self.dtgs:
                ihmod=int(dtg[8:10])%6
                if(ihmod == 0):
                    dtgs.append(dtg)
            self.dtgs=dtgs

        self.trk={}
        self.btdtgs=[]

        # -- check to make sure there is eighter carq0 or bt0
        #
        
        idtgs=[]
        for dtg in dtgs:
            c0=None
            try:     c0=self.cq00[dtg]
            except:  None
            bt=None
            try:     bt=self.best[dtg]
            except:  None

            if(c0 == None and bt== None):
                print 'WWWW no c0 or bt for stmid: ',self.stm1id,' dtg: ',dtg
            else:
                idtgs.append(dtg)

        dtgs=idtgs
        self.dtgs=idtgs

        dtgs.sort()
        self.dtgs.sort()
        ndtgs=len(self.dtgs)

        # -- get btdtgs
        #

        for dtg in dtgs:
            
            bt=None
            try:     bt=self.best[dtg]
            except:  None

            if(bt == None): continue
            self.btdtgs.append(dtg)

            
        if(btonly):
            dtgs=self.btdtgs
            ndtgs=len(dtgs)
            self.dtgs=dtgs

        # -- get b1id

        b1ids=[]
        b1id=None
        sname=None
        
        for dtg in dtgs:

            c0=None
            try:     c0=self.cq00[dtg]
            except:  None

            
            if(c0 == None): continue
            if(hasattr(c0,'b1id')):
                if(c0.b1id != c0.undef): 
                    b1id=c0.b1id
                    b1ids.append(b1id)

        # -- check for case where beginning b1d in the carq card is different from the end
        #
        if(dob1idSet):
            if(len(b1ids) == 1): 
                b1id=b1ids[0]
            
            elif(len(b1ids) > 1):
                bb1id=b1ids[0]
                # -- check for multiple  b1ids in the CARQ, e.g., wpac -> IO
                for tb1 in b1ids[1:]:
                    if(tb1 != bb1id):
                        print
                        print
                        for x in range(0,5):
                            print 'WWWW---- b1id changes for stm1id: ',self.stm1id,'... use the first one: ',bb1id
                        print
                        print
                        break
                    
                b1id=bb1id
                    
            

                        

        ntrk=0
        for dtg in dtgs:

            c0=None
            try:     c0=self.cq00[dtg]
            except:  None

            c12=None
            try:     c12=self.cq12[dtg]
            except:  None

            c24=None
            try:     c24=self.cq24[dtg]
            except:  None

            bt=None
            try:     bt=self.best[dtg]
            except:  None

            o0=None
            try:     o0=self.of00[dtg]
            except:  None

            o12=None
            try:     o12=self.of12[dtg]
            except:  None

            o24=None
            try:     o24=self.of24[dtg]
            except:  None

            w0=None
            try:     w0=self.wrng[dtg]
            except:  None

            lf=rlat=rlon=vmax=pmin=spd=dir=tccode=r34m=r50m=sname=None
            clf=crlat=crlon=cvmax=cpmin=cspd=cdir=ctccode=cr34m=cr50m=csname=None
            blf=brlat=brlon=bvmax=bpmin=bspd=bdir=btccode=br34m=br50m=bsname=None
            depth=cdepth=bdepth=None
            r34=cr34=br34=r50=cr50=br50=None
            poci=cpoci=bpoci=None
            roci=croci=broci=None
            rmax=crmax=brmax=None


            if(verb):
                print 'DDDDDDD',dtg
                if(c0 != None):
                    print 'CCC000'
                    c0.ls('lat')
                    c0.ls('lon')
                    c0.ls('vmax')
                    
                if(w0 != None):
                    print 'WWW000'
                    c0.ls('lat')
                    c0.ls('lon')
                    c0.ls('vmax')
                    
                if(c12 != None):
                    print 'CCC1212'
                    c12.ls('lat')
                    c12.ls('lon')
                    c12.ls('vmax')
                if(bt != None):
                    print 'BBB000'
                    bt.ls('lat')
                    bt.ls('lon')
                    bt.ls('vmax')
            
                if(o0 != None):
                    print 'OOO000'

                if(o24 != None):
                    print 'OOO2424'

                if(o12 != None):
                    print 'OOO1212'

            if(o0 != None or w0 != None or o12 != None or o24 != None):
                wncode='WN'
                wtccode='TW'
            else:
                wncode='NW'
                wtccode=None
                
            ntrk=ntrk+1
            tdo='---'
            alf=None
            postype='X'
            
            
            if(o0 != None):
                if(hasattr(o0,'tdo')):
                    tdo=o0.tdo

            if(c0 != None):
                crlat=c0.rlat
                crlon=c0.rlon
                if(hasattr(c0,'vmax')): cvmax=c0.vmax
                if(hasattr(c0,'pmin')): cpmin=c0.pmin
                if(hasattr(c0,'dir')):  cdir=c0.dir
                if(hasattr(c0,'spd')):  cspd=c0.spd
                if(hasattr(c0,'r34m')):  cr34m=c0.r34m
                if(hasattr(c0,'r50m')):  cr50m=c0.r50m
                if(hasattr(c0,'tccode')):
                    if(c0.tccode != self.undef): ctccode=c0.tccode
                if(hasattr(c0,'alf')):  clf=c0.alf
                if(hasattr(c0,'sname')):  csname=c0.sname
                if(hasattr(c0,'depth')):  cdepth=c0.depth
                if(hasattr(c0,'r34')):    cr34=c0.r34
                if(hasattr(c0,'r50')):    cr50=c0.r50
                if(hasattr(c0,'poci')):   cpoci=c0.poci
                if(hasattr(c0,'roci')):   croci=c0.roci
                if(hasattr(c0,'rmax')):   crmax=c0.rmax

            crlatm12=crlonm12=None
            if(c12 != None):
                crlatm12=c12.rlat
                crlonm12=c12.rlon
                
            # -- calc CARQ motion from tau-12 to tau using CARQ posits
            #
            if(c0 != None and cdir == None and crlatm12 != None and crlonm12 != None):
                dt=12
                (cdir,cspd,umotion,vmotion)=rumhdsp(crlatm12,crlonm12,crlat,crlon,dt)
                postype='c'
            elif(c0 != None and cdir != None):
                postype='C'

            if(c0 != None and cdir == None):
                postype='b'


            if(bt != None):
                brlat=bt.rlat
                brlon=bt.rlon
                
                if(hasattr(bt,'vmax')): bvmax=bt.vmax
                if(hasattr(bt,'pmin')): bpmin=bt.pmin
                if(hasattr(bt,'dir')): bdir=bt.dir
                if(hasattr(bt,'spd')): bspd=bt.spd
                if(hasattr(bt,'tccode')):
                    if(bt.tccode != self.undef):  btccode=bt.tccode
                if(hasattr(bt,'r34m')):  br34m=bt.r34m
                if(hasattr(bt,'r50m')):  br50m=bt.r50m
                if(hasattr(bt,'alf')):   blf=bt.alf
                if(hasattr(bt,'sname')): bsname=bt.sname
                if(hasattr(bt,'depth')): bdepth=bt.depth
                if(hasattr(bt,'r34')):   br34=bt.r34
                if(hasattr(bt,'r50')):   br50=bt.r50
                if(hasattr(bt,'poci')):  bpoci=bt.poci
                if(hasattr(bt,'roci')):  broci=bt.roci
                if(hasattr(bt,'rmax')):  brmax=bt.rmax



            if(docq00):

                if(crlat != None): rlat=crlat
                if(crlon != None): rlon=crlon
                if(cvmax != None): vmax=cvmax
                if(cpmin != None): pmin=cpmin
                if(cdir  != None): dir=cdir
                if(cspd  != None): spd=cspd
                if(ctccode != None): tccode=ctccode
                if(cr34m   != None): r34m=cr34m
                if(cr34    != None): r34=cr34
                if(cr50m   != None): r50m=cr50m
                if(cr50    != None): r50=cr50
                if(clf     != None): alf=clf
                if(cdepth  != None): depth=cdepth
                if(cpoci   != None): poci=cpoci
                if(croci   != None): roci=croci
                if(crmax   != None): rmax=crmax

                # -- fallback to bt
                #
                if(rlat == None): 
                    rlat=brlat
                if(rlon == None): 
                    rlon=brlon
                    postype='b'
                    
                # -- check if undef too when it's 0 in bdeck -> undef
                #
                if(vmax == None or vmax == self.undef): vmax=bvmax
                if(pmin == None or pmin == self.undef): pmin=bpmin
                if(alf  == None): alf=blf
                if(cdepth == None): depth=bdepth
                if(ctccode == None): tccode=btccode

                if(r34m == None and br34m != None): r34m=br34m
                if(r34  == None and br34  != None): r34=br34
                if(r50  == None and br50  != None): r50=br50
                if(poci == None and bpoci != None): poci=bpoci
                if(roci == None and broci != None): roci=broci
                if(rmax == None and brmax != None): rmax=brmax
                

            if(btonly):
                
                postype='B'
                
                if(brlat   != None): rlat=brlat
                if(brlon   != None): rlon=brlon
                if(bvmax   != None): vmax=bvmax
                if(bpmin   != None): pmin=bpmin
                if(bdir    != None): dir=bdir
                if(bspd    != None): spd=bspd
                if(btccode != None): tccode=btccode
                if(br34m   != None): r34m=br34m
                if(br50m   != None): r50m=br50m
                if(blf     != None): alf=blf
                if(bdepth  != None): depth=bdepth
                if(br34    != None): r34=br34
                if(br50    != None): r50=br50
                if(bpoci   != None): poci=bpoci
                if(broci   != None): roci=broci
                if(brmax   != None): rmax=brmax

                
            if(csname  != None): sname=csname
            if(sname ==  None): sname=bsname

            if(tccode == None and wtccode == None):
                if(not(Is9X(self.stm1id))):
                    if(verb): print """WWW couldn't find tccode in carq or bt; set to 'NT'""",dtg,self.stm1id
                #print """WWW couldn't find tccode in carq or bt; exit and try to figure out what happen""",dtg,self.stm1id
                tccode='NT'
            
            if(wtccode != None and tccode == None):
                tccode=wtccode

            # -- use vmax
            #
            if(useVmax4TcCode and tccode == 'NT'):
                if(vmax != None and IsTcWind(vmax)):
                    tccode='TW'
                else:
                    tccode='NT'
                
            # -- final qc
            #
            if(vmax == None): vmax=-999

            if(verb):
                print 'WWW',dtg,tccode,wncode,wtccode,o0,w0,o12,o24,wncode
                print
            
            self.trk[dtg]=Trkdata(rlat,rlon,vmax,pmin,dir,spd,tccode,wncode,b1id=b1id,tdo=tdo,ntrk=ntrk,ndtgs=ndtgs,
                                  r34m=r34m,r50m=r50m,depth=depth,
                                  r34=r34,r50=r50,poci=poci,roci=roci,
                                  rmax=rmax)

            self.trk[dtg].tdo=tdo
            self.trk[dtg].alf=alf
            self.trk[dtg].sname=sname
            self.trk[dtg].stmid=self.stm1id
            self.trk[dtg].postype=postype


        # -- get prev 12-h track dir/spd
        #
        
        dirspd={}
        for n in range(0,ndtgs):

            dtg=dtgs[n]
            if(n == 0):
                nm1=n
                if(ndtgs > 2):  n0=n+2
                else:           n0=n+1
            elif(n == 1):
                nm1=n-1
                if(ndtgs > 2):  n0=n+1
                else:           n0=n+1
            elif(n == ndtgs-1):
                nm1=n-2
                if(ndtgs > 2):  n0=n
                else:           n0=n
            else:
                nm1=n-2
                n0=n

            if(n0 > ndtgs-1):
                trkdir=self.undef
                trkspd=self.undef
            else:
                
                rlatm1=self.trk[dtgs[nm1]].rlat
                rlonm1=self.trk[dtgs[nm1]].rlon
                rlat0=self.trk[dtgs[n0]].rlat
                rlon0=self.trk[dtgs[n0]].rlon
                
                dt=dtgdiff(dtgs[nm1],dtgs[n0])
                (trkdir,trkspd,umotion,vmotion)=rumhdsp(rlatm1,rlonm1,rlat0,rlon0,dt)
                
            dirspd[dtg]=(trkdir,trkspd)

        self.ndtgs=ndtgs

        # -- look for warning status in shem/io if WN t-1 or t+2
        #

        if(IsIoShemBasin(self.stm2id[0:2])):
            self.interpWarn(dtgs,verb=verb)

        # -- set the bt dir/spd and dirtype
        #
        for dtg in dtgs:
            
            self.trk[dtg].dirtype=self.trk[dtg].postype

            if( (self.trk[dtg].dir == None) or btonly):
                (trkdir,trkspd)=dirspd[dtg]
                if(self.trk[dtg].postype == 'c'):
                    self.trk[dtg].dirtype='b'
                    
                self.trk[dtg].dir=trkdir   
                self.trk[dtg].spd=trkspd    
                
            self.trk[dtg].trkdir=trkdir   
            self.trk[dtg].trkspd=trkspd    


    def chkDtgBreaks(self,dtgs,maxdiff=240,verb=0):

        ndtgs=[]
        dtgs.sort()
        foundbreak=0

        ldtgs=len(dtgs)
        for n in range(len(dtgs)-2,-1,-1):
            dt=dtgdiff(dtgs[n],dtgs[n+1])
            ndtgs.append(dtgs[n+1])
            if(verb): print 'dddd chkDtgBreaks:',n,dtgs[n],dtgs[n+1],dt
            if(dt > maxdiff):
                print 'WWW(tcCL.MDdataset.chkDtgBreaks n: ',n,' dt: ',dt,' dtgs[n]: ',dtgs[n],' dtgs[n+1]: ',dtgs[n+1],' foundbreak=1'
                foundbreak=1
                break

        if(not(foundbreak)): ndtgs=dtgs
        lndtgs=len(ndtgs)
        return(ndtgs)


    def interpWarn(self,odtgs,verb=0):

        ndtgs=len(odtgs)

        firstWN=0
        lastWN=ndtgs
        
        # -- find first and last warning
        #
        for n in range(0,ndtgs):
            wn0=self.trk[odtgs[n]].wncode
            if(wn0 == 'WN'): 
                firstWN=n
                break
            
        for n in range(ndtgs-1,0,-1):
            wn0=self.trk[odtgs[n]].wncode
            if(wn0 == 'WN'): 
                lastWN=n
                break
            
        if(verb): print 'firstWN: ',firstWN,'lastWN: ',lastWN,'ndtgs: ',ndtgs

        for n in range(firstWN,lastWN+1):
            
            if(ndtgs >= 2 and n <= ndtgs-2):
                
                if(n == 0):
                    nm1=n
                    n0=n
                    np1=n+1
                else:
                    nm1=n-1
                    n0=n
                    np1=n+1
                    
                wnm1=self.trk[odtgs[nm1]].wncode
                wn0=self.trk[odtgs[n0]].wncode
                wnp1=self.trk[odtgs[np1]].wncode
                    
                if(verb):
                    print 'nnnnn ',n,odtgs[n],'nm1:',nm1,wnm1,'n0:',n0,wn0,'np1:',np1,wnp1
                
                if( 
                    ( (wn0 == 'NW' and wnp1 == 'WN') or (wn0 == 'NW' and wnm1 == 'WN') )
                    ):

                    # -- don't interp back if first point or last
                    #
                    self.trk[odtgs[n0]].wncode='WN'
                    if(verb): print 'AAAAA ',ndtgs,n,nm1,n0,np1,self.trk[odtgs[n0]].wncode


    def cleanMD(self):

        #try: del self.cq00
        #except: None
        
        #try: del self.cq12
        #except: None
        
        #try: del self.cq24
        #except: None
        
        try: del self.best
        except: None
        
        try: del self.wrng
        except: None
        
        try: del self.of00
        except: None
        
        try: del self.of03
        except: None


    def getMDtrk(self):

        otrk={}
        dtgs=self.trk.keys()
        dtgs.sort()

        for dtg in dtgs:
            otrk[dtg]=self.trk[dtg].gettrk()

        return(otrk,dtgs)
    
    def getMDotrk(self):

        otrk={}
        dtgs=self.trk.keys()
        dtgs.sort()

        for dtg in dtgs:
            otrk[dtg]=self.trk[dtg]

        return(otrk,dtgs)

                
    def lsMDtrk(self,filtTCs=0,doprint=1):


        cards={}
        (otrk,dtgs)=self.getMDtrk()

        for dtg in dtgs:

            (rlat,rlon,vmax,pmin,dir,spd,tccode,wncode,trkdir,trkspd,dirtype,b1id,tdo,
             ntrk,ndtgs,r34m,r50m,alf,sname,r34,r50,depth)=self.trk[dtg].gettrk()
            
            ostmid=self.stm1id
            if(hasattr(self.trk[dtg],'ostmid')): ostmid=self.trk[dtg].ostmid

            gentrk=0
            if(hasattr(self,'gendtgs')):
                if(dtg in self.gendtgs): gentrk=1
            if(rlat != None):
                (clat,clon)=Rlatlon2Clatlon(rlat,rlon,dodec=1)
                if(filtTCs and not(IsTc(tccode))): 
                    card="%s -- not a TC...and filtTCs=1"
                else:
                    card=printTrk(ostmid,dtg,rlat,rlon,vmax,pmin,dir,spd,dirtype,
                                  tdo=tdo,tccode=tccode,wncode=wncode,
                                  ntrk=ntrk,ndtgs=ndtgs,r34m=r34m,r50m=r50m,
                                  alf=alf,sname=sname,gentrk=gentrk,doprint=doprint)
                    
                cards[dtg]=card

        return(cards)
                
                

class MDdeck(Adeck):


    def __init__(self,cards,
                 b2id,bnum,byear,
                 verb=0):

        #from w2 import SetLandFrac
        #from w2 import GetLandFrac

        self.b2id=b2id
        self.bnum=bnum
        self.byear=byear

        self.dofilt9x=0
        
        self.undef=-999
        self.skipcarq=0
        self.chkb2id=1
        self.warn=1
        self.verb=verb

        # -- all cards
        self.cards=cards.split('\n')

        # -- just mdeck related cards
        self.mdcards={}
        
        self.lf=SetLandFrac()
        self.getlf=GetLandFrac

        self.initMDcards()
        self.setMD()


    def initMDcards(self,warn=0,doGenesisCards=1):

        self.curb2id=-999
        self.curbnum=-999
        self.curbyear=-999
        
        for card in self.cards:
            tt=card.split(',')
            # -- scan for genesis nhc cards
            if(find(card,'GENESIS')):
                if(warn): print 'WWW NHC genesis posit...ignore',card
                # -- maybe use?
                if(not(doGenesisCards)): continue
            
            if(len(tt) < 5):
                if(warn): print 'WWW short card in MDdeck.initMDcards: ',card
                continue
            aid=self.setAidNCard(tt)
            if(aid == 'BEST' or
               aid == 'CARQ' or aid == 'WRNG' or aid == 'CNTR' or aid == 'COMS' or
               aid == 'JTWC' or aid == 'OFCL'
               ):
                rc=self.makeBidDtg(tt,card)
                # -- bail for 80-89 storms, etc
                if(rc == None):
                    #print 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa ',rc
                    continue

                else:
                
                    (dtg,b2id,bnum,byear)=rc

                    if(self.chkStm2id() > 0):
                        print 'WWWWWWWWWWWW multiple stmids in this adeck...sayoonara'
                        sys.exit()

                    MF.loadDictList(self.mdcards,dtg,card)

        self.stm2id="%s%s.%s"%(self.b2id,self.bnum,self.byear)


    def chkStm2id(self):
        
        if(self.curb2id != self.b2id): self.curb2id=self.b2id
        if(self.curbnum != self.bnum): self.curbnum=self.bnum
        if(self.curbyear != self.byear): self.curbyear=self.byear

        rc=0
        if(self.curb2id != self.b2id): rc=1
        if(self.curbnum != self.bnum): rc=2
        if(self.curbyear != self.byear): rc=3

        return(rc)
        


    def setMD(self):

        dtgs=self.mdcards.keys()
        dtgs.sort()

        # -- stm2id
        #
        mD=MDdataset(dtgs,self.stm2id)
        
        for dtg in dtgs:
            cards=self.mdcards[dtg]
            
            for card in cards:
                self.ParseABdeckCard(mD,dtg,card)

        self.mD=mD


    def getMDByDtgs(self,dtgs,stm2id):


        # -- stm2id
        #
        mD=MDdataset(dtgs,stm2id)
        
        for dtg in dtgs:
            cards=self.mdcards[dtg]
            for card in cards:
                self.ParseABdeckCard(mD,dtg,card)

        return(mD)


    def getDtgRange(self,mD,nhours=48,diffdtgTol=36.0,ddtg=6,verb=0):
        
        """ adecks can have multiple storms because they are not cleaned like bdecks; look for a break in the dtgs > nhours
        """

        def checkDtgDdtg(dtgs,ddtg):
            chkddtg=ddtg*1.0
            cntDtgs=[]
            ndtgs=len(dtgs)
            # -- case for 1 dtg
            if(ndtgs == 1): 
                ne=1
            else:
                ne=ndtgs-1
                
            for n in range(0,ne):
                dtg0=dtgs[n]
                
                # -- handling 1 dtgs
                if(ndtgs == 1): 
                    dtg1=dtgs[n]
                    cntDtgs.append(dtg1)
                    print 'WWW:MDeck.getDtgRange 11111111111111 dtg -- set cntDtg to this one and return'
                    return(cntDtgs)
                else:
                    dtg1=dtgs[n+1]
                diffdtg=dtgdiff(dtg0,dtg1)
                #print 'n:',n,ndtgs-1,dtg0,dtg1,diffdtg,chkddtg
                if(diffdtg != chkddtg):
                    print 'WWW:MDeck.getDtgRange.checkDtg6h() -- continuity problem n: %02d'%(n+1),' ndtgs: %2d'%(len(dtgs)),'dtg0: ',dtg0,'dtg1: ',dtg1
                    if(n+1 == ndtgs-1):
                        print 'problem at end -- remove dtg: ',dtg1,' by bumping n increment'
                        n=n+1
                    else:
                        # -- we use 18 h because of JTWC SHEM real storm bdecks can have gaps that will be filled in by 9X
                        # -- use 36 h because of JTWC 19W.16 had a 24.0 h gap when the did the renameing of e1w.16 -> 19w.16
                        #
                        if(diffdtg <= diffdtgTol):
                            cntDtgs.append(dtg0)
                        else:
                            print 'problem NOT at end and diffdtg > diffdtgTol ',diffdtgTol,'-- stop!'
                            sys.exit()
                else:
                    cntDtgs.append(dtg0)
                
                if(n == ndtgs-2):
                    cntDtgs.append(dtg1)
                    #print 'fffffffoooooo---finalize: %2d'%(n),dtg1,mD.stm1id
                    
            return(cntDtgs)
                        
        # -- mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
        #
        
        dtgs=mD.dtgs
        mD.uniqStmdtgs={}
        nd=len(dtgs)
        
        # -- check for posits
        #
        if(nd == 0):
            return
        
        bdtg=dtgs[0]
        for n in range(0,nd):
            dtg0=dtgs[n]
            if(n < nd-1):
                dtg1=dtgs[n+1]
            else:
                dtg1=dtg0

            dtgdiff=dtgdiff(dtg0,dtg1)
            if(dtgdiff > nhours or n == nd-1):
                edtg=dtg0
                if(verb): print 'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB: ',n,' bdtg: ',bdtg,' edtg: ',edtg,' dtgdiff: ',dtgdiff

                alldtgs=[]
                for tdtg in dtgrange(bdtg,edtg,ddtg):
                    if(tdtg in dtgs): alldtgs.append(tdtg)
                    
                # -- check continuity of dtgs
                #
                finaldtgs=checkDtgDdtg(alldtgs,ddtg)
                
                # -- if no dtgs do not set the uniqStmdtgs...
                #
                if(len(finaldtgs) > 0):
                    mD.uniqStmdtgs[bdtg]=finaldtgs
                
                # -- set bdtg of next serious to dtg1 with diff > nhours
                #
                bdtg=dtg1

        


    def getDtgRangeNN(self,mD,nhours=48,diffdtgTol=36.0,ddtg=6,verb=0):
        
        """ adecks can have multiple storms because they are not cleaned like bdecks; look for a break in the dtgs > nhours
        """

        def checkDtgDdtg(dtgs,ddtg):
            
            chkddtg=ddtg*1.0
            cntDtgs=[]
            ndtgs=len(dtgs)
            # -- case for 1 dtg
            if(ndtgs == 1): 
                ne=1
            else:
                ne=ndtgs-1
                
            n=0
            while(n < ne):
                dtg0=dtgs[n]
                
                # -- handling 1 dtgs
                if(ndtgs == 1): 
                    dtg1=dtgs[n]
                    cntDtgs.append(dtg1)
                    print 'WWW:MDeck.getDtgRangeNN.checkDtg6h() -- 1111111 dtg -- set cntDtg to this one and return'
                    return(cntDtgs)
                else:
                    dtg1=dtgs[n+1]
                    
                diffdtg=dtgdiff(dtg0,dtg1)
                #print 'n------------------------------:',n,ndtgs-1,dtg0,dtg1,diffdtg,chkddtg
                if(diffdtg != chkddtg):
                    print 'WWW:MDeck.getDtgRangeNN.checkDtg6h() -- continuity problem n: %2d'%(n+1),' ndtgs: %2d'%(len(dtgs)),'dtg0: ',dtg0,'dtg1: ',dtg1,\
                          'diffdtg: ',diffdtg,' stmid: ',mD.stm1id   
                    if(n+1 == ndtgs-1):
                        print
                        print 'WWW:MDeck.getDtgRangeNN.checkDtg6h() -- problem at end -- remove dtg: ',dtg1,' by bumping n increment +2 for stmid: ',mD.stm1id
                        n=n+2
                    else:
                        # -- we use 18 h because of JTWC SHEM real storm bdecks can have gaps that will be filled in by 9X
                        # -- use 36 h because of JTWC 19W.16 had a 24.0 h gap when the did the renameing of e1w.16 -> 19w.16
                        #
                        if(diffdtg <= diffdtgTol):
                            cntDtgs.append(dtg0)
                            n=n+1
                        else:
                            print
                            print 'WWW:MDeck.getDtgRangeNN.checkDtg6h() -- problem NOT at end and diffdtg: ',diffdtg,' > diffdtgTol ',diffdtgTol,(n+1),ndtgs-1
                            if((n+1) <= 3 and ndtgs > 4):
                                print 'WWW:MDeck.getDtgRangeNN.checkDtg6h() -- problem at BEGINNING...toss first dtgs before the break at: ',dtg1,n,ndtgs
                                cntDtgs=[]
                                cntDtgs.append(dtg1)
                                
                            n=n+1
                                
                else:
                    cntDtgs.append(dtg0)
                    n=n+1
                
                if(n == ndtgs-1):
                    #print 'fffffffnnnnnn---finalize: %2d'%(n),dtg1,mD.stm1id
                    cntDtgs.append(dtg1)
                    
            return(cntDtgs)
                        
        # -- mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
        #
        
        dtgs=mD.dtgs
        mD.uniqStmdtgs={}
        nd=len(dtgs)
        
        # -- check for posits
        #
        if(nd == 0):
            return
        
        bdtg=dtgs[0]
        for n in range(0,nd):
            dtg0=dtgs[n]
            if(n < nd-1):
                dtg1=dtgs[n+1]
            else:
                dtg1=dtg0

            dtgdiff=dtgdiff(dtg0,dtg1)
            if(dtgdiff > nhours or n == nd-1):
                edtg=dtg0
                if(verb): print 'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB: %2d'%(n),' bdtg: ',bdtg,' edtg: ',edtg,' dtgdiff: %3.0f'%(dtgdiff),mD.stm1id

                alldtgs=[]
                for tdtg in dtgrange(bdtg,edtg,ddtg):
                    if(tdtg in dtgs): alldtgs.append(tdtg)
                    
                # -- check continuity of dtgs
                #
                finaldtgs=checkDtgDdtg(alldtgs,ddtg)
                
                if(len(finaldtgs) > 0):
                    bdtg=finaldtgs[0]
                    mD.uniqStmdtgs[bdtg]=finaldtgs
                    
                # -- set bdtg for next series
                #
                bdtg=dtg1


    def ParseABdeckCard(self,mD,dtg,adcard):
        """
atcf='''BASIN,CY,YYYYMMDDHH,TECHNUM/MIN,TECH,TAU,LatN/S,LonE/W,VMAX,MSLP,TY,RAD,WINDCODE,RAD1,RAD2,RAD3,RAD4,RADP,RRP,MRD,GUSTS,EYE,SUBREGION,MAXSEAS,INITIALS,DIR,SPEED,STORMNAME,DEPTH,SEAS,SEASCODE,SEAS1,SEAS2,SEAS3,SEAS4,USERDEFINED,userdata'''
ttt=atcf.split(',')
for n in range(0,len(ttt)):
    print '''        # %02d, %s'''%(n,ttt[n])
sys.exit()
"""


        # 00, BASIN
        # 01, CY
        # 02, YYYYMMDDHH
        # 03, TECHNUM/MIN
        # 04, TECH
        # 05, TAU
        # 06, LatN/S
        # 07, LonE/W
        # 08, VMAX
        # 09, MSLP
        # 10, TY
        # 11, RAD
        # 12, WINDCODE
        # 13, RAD1
        # 14, RAD2
        # 15, RAD3
        # 16, RAD4
        # 17, RADP
        # 18, RRP
        # 19, MRD
        # 20, GUSTS
        # 21, EYE
        # 22, SUBREGION
        # 23, MAXSEAS
        # 24, INITIALS
        # 25, DIR
        # 26, SPEED
        # 27, STORMNAME
        # 28, DEPTH
        # 29, SEAS
        # 30, SEASCODE
        # 31, SEAS1
        # 32, SEAS2
        # 33, SEAS3
        # 34, SEAS4
        # 35, USERDEFINED
        # 36, userdata


        undef=-999
        sname=''


        def chkRquad(quad):

            allundef=1
            for q in quad:
                if(q != undef): allundef=0

            return(allundef)
        
        def SC2(tt,nn):
            try:
                ostr=tt[nn].strip()
            except:
                ostr=''
            return(ostr)

        def SC(istr):
            ostr=istr[0:-1].strip()
            return(ostr)

        def setRadiicode(rwind):

            if(not(rwind.isdigit())):
                crcode=undef
                return(crcode)
            rwind=int(rwind)
            
            crcode=undef
            if(rwind == 30):                 crcode='r30'
            if(rwind == 35 or rwind == 34):  crcode='r34'
            if(rwind == 50):                 crcode='r50'
            if(rwind == 100):                crcode='r100'
            if(rwind == 64 or rwind == 65):  crcode='r64'
            return(crcode)


        def setDigit(cvar,nezero=0):
            if(cvar.isdigit() or ('-' in cvar)):
                cvar=int(cvar)
            else:
                cvar=undef
            if(nezero and cvar == 0): cvar=undef
            return(cvar)
            

        def setString(cvar,doalpha=1):
            if(not(cvar.isalpha()) and doalpha or (len(cvar) == 0) ):
                cvar=undef
            if(cvar == 'X'): cvar=undef
            return(cvar)


        def setRadii(mm,rcode,rquad):
            
            if(rcode == 'r30'  and chkRquad(rquad) == 0 ): mm.setR30(rquad)
            if(rcode == 'r34'  and chkRquad(rquad) == 0 ): mm.setR34(rquad)
            if(rcode == 'r50'  and chkRquad(rquad) == 0 ): mm.setR50(rquad)
            if(rcode == 'r64'  and chkRquad(rquad) == 0 ): mm.setR64(rquad)
            if(rcode == 'r100' and chkRquad(rquad) == 0 ): mm.setR100(rquad)



        # -- split the card
        tt=adcard.split(',')
        ntt=len(tt)

            
        if(self.verb):
            print '   ntt: ',ntt,' adcard: ',tt
            #adcard[:-1].strip()
            if(self.verb == 2):
                for i in range(0,ntt):
                    print 'adflds: ',i,tt[i]


        nn=0
        b2id=SC2(tt,nn)                                ; nn=nn+1 # 00
        snum=setDigit(SC2(tt,nn))                      ; nn=nn+1 # 01
        dtg=setString(SC2(tt,nn),doalpha=0)            ; nn=nn+1 # 02
        aidnum=setDigit(SC2(tt,nn))                    ; nn=nn+1 # 03
        aid=setString(SC2(tt,nn))                      ; nn=nn+1 # 04
        tau=setDigit(SC2(tt,nn))                       ; nn=nn+1 # 05
        clat=setString(SC2(tt,nn),doalpha=0)           ; nn=nn+1 # 06
        clon=setString(SC2(tt,nn),doalpha=0)           ; nn=nn+1 # 07
        vmax=setDigit(SC2(tt,nn))                      ; nn=nn+1 # 08
        pmin=setDigit(SC2(tt,nn),nezero=1)             ; nn=nn+1 # 09
        tccode=setString(SC2(tt,nn))                   ; nn=nn+1 # 10
        rcode=setRadiicode(SC2(tt,nn))                 ; nn=nn+1 # 11
        qcode=setString(SC2(tt,nn))                    ; nn=nn+1 # 12
        rne=setDigit(SC2(tt,nn),nezero=1)              ; nn=nn+1 # 13
        rse=setDigit(SC2(tt,nn),nezero=1)              ; nn=nn+1 # 14
        rsw=setDigit(SC2(tt,nn),nezero=1)              ; nn=nn+1 # 15
        rnw=setDigit(SC2(tt,nn),nezero=1)              ; nn=nn+1 # 16
        radii=[rne,rse,rsw,rnw]
        rquad=radii
        
        # -- convert radii to standard quadrants based on qcode
        #
        if(qcode != undef):   rquad=WindRadiiCode2Normal(qcode,radii)

        poci=setDigit(SC2(tt,nn))                      ; nn=nn+1 # 18
        roci=setDigit(SC2(tt,nn))                      ; nn=nn+1 # 19
        rmax=setDigit(SC2(tt,nn))                      ; nn=nn+1 # 20
        gusts=setDigit(SC2(tt,nn))                     ; nn=nn+1 # 20
        deye=setDigit(SC2(tt,nn),nezero=1)             ; nn=nn+1 # 21
        b1id=setString(SC2(tt,nn))                     ; nn=nn+1 # 22
        maxseas=setDigit(SC2(tt,nn))                   ; nn=nn+1 # 23
        tdo=setString(SC2(tt,nn))                      ; nn=nn+1 # 24
        dir=setDigit(SC2(tt,nn))                       ; nn=nn+1 # 25
        spd=setDigit(SC2(tt,nn))                       ; nn=nn+1 # 26
        name=setString(SC2(tt,nn),doalpha=0)           ; nn=nn+1 # 27
        depth=setString(SC2(tt,nn))                    ; nn=nn+1 # 28


        if(clat == undef):
            if(self.verb):
                print 'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW undef clat/clon in ParseABdeckCard ',dtg,snum,b2id
            return

        (rlat,rlon)=Clatlon2Rlatlon(clat,clon)

        # -- check for bad lat/lon
        if(not(rlat >= -90.0 and rlat <= 90.0)):
            print 'BBBBBBBBBBBBBBBBbaaaaaaaaaaaaaaaaddddddddddddd rlat; aid: ',aid,' dtg: ',dtg,' clat/clon: ',clat,clon
            return

        try:
            alf=self.getlf(self.lf,rlat,rlon)
        except:
            print 'ooooooooooooooopppppppppppppppppppppppssssssssssssssssssssssssss: ',rlat,rlon

        # 25W.1986 has a blank JTWC 12 h lat/lon card, if '' then return
        #
        noload=0
        if(clat == undef and self.verb):
            print 'WWWWWWW noload making mdeck from adeck card: ',adcard[:-1]
            noload=1

        abdata=ABdata(rlat,rlon,vmax,pmin,dir,spd,tccode,tdo,poci,roci,rmax,deye,depth,name,b1id,snum,b2id)
        abdata.alf=alf


        if(name != undef and sname != 'NONAME'):
            sname=name

        
        if(aid == 'CARQ' and tau == 0):

            try:
                mm=mD.cq00[dtg]
            except:
                mD.cq00[dtg]=abdata
                mm=mD.cq00[dtg]
                
            setRadii(mm,rcode,rquad)
            mm.sname=sname
            mD.cq00[dtg]=mm

        if(aid == 'BEST'):

            try:
                mm=mD.best[dtg]
            except:
                mD.best[dtg]=abdata
                mm=mD.best[dtg]

            setRadii(mm,rcode,rquad)
            mm.sname=sname
            mD.best[dtg]=mm
            

            if(self.verb): print 'bbbbb',b2id,b1id,snum,dtg,tau,aid,rlat,rlon,vmax,pmin,\
                           rcode,rquad,poci,roci,rmax,gusts,deye,tdo,dir,spd,name,depth
        
            
        if( (aid == 'OFCL' or aid == 'JTWC') and tau == 0):

            try:
                mm=mD.of00[dtg]
            except:
                mD.of00[dtg]=abdata
                mm=mD.of00[dtg]

            setRadii(mm,rcode,rquad)
            mD.of00[dtg]=mm

            
        if( (aid == 'OFCL' or aid == 'JTWC') and tau == 3):

            try:
                mm=mD.of03[dtg]
            except:
                mD.of03[dtg]=abdata
                mm=mD.of03[dtg]
            setRadii(mm,rcode,rquad)
            mD.of03[dtg]=mm

        if( (aid == 'OFCL' or aid == 'JTWC') and tau == 24):

            try:
                mm=mD.of24[dtg]
            except:
                mD.of24[dtg]=abdata
                mm=mD.of24[dtg]
            setRadii(mm,rcode,rquad)
            mD.of24[dtg]=mm

        if( (aid == 'OFCL' or aid == 'JTWC') and tau == 12):

            try:
                mm=mD.of12[dtg]
            except:
                mD.of12[dtg]=abdata
                mm=mD.of12[dtg]
            setRadii(mm,rcode,rquad)
            mD.of12[dtg]=mm

            
        if(aid == 'CARQ' and tau == -12):
            
            try:
                mm=mD.cq12[dtg]
            except:
                mD.cq12[dtg]=abdata
                mm=mD.cq12[dtg]
            setRadii(mm,rcode,rquad)
            mD.cq12[dtg]=mm
        
        if(aid == 'CARQ' and tau == -24):
            
            try:
                mm=mD.cq24[dtg]
            except:
                mD.cq24[dtg]=abdata
                mm=mD.cq24[dtg]
            setRadii(mm,rcode,rquad)
            mD.cq24[dtg]=mm

        if(aid == 'WRNG' and tau == 0):

            try:
                mm=mD.wrng[dtg]
            except:
                mD.wrng[dtg]=abdata
                mm=mD.wrng[dtg]
            setRadii(mm,rcode,rquad)
            mD.wrng[dtg]=mm

        
        return

    def lsBest(self,dtg):

        try:
            print 'BBB: ',dtg,self.mD.best[dtg].ls()
        except:
            print 'BBB(nada)'
            



class MD3trk(MDdataset):

    undef=-999.
    
    def __init__(self,cards,stm1id,stm9xid,dom3=0,basin=None,sname=None,stmDev=None,
                 dobt=0,doPutDSs=0,verb=0):

        # -- input
        #
        
        self.dom3=dom3
        self.verb=verb
        self.cards=cards
        
        (self.itrk,self.idtgs)=self.getTrk4Cards()
        (snum,b1id,year,b2id,stm2id,stm1id)=getStmParams(stm1id)
         
        self.b1id=b1id
        self.snum=snum
        self.syear=year
        self.stm2id=stm2id
        self.ostm2id=stm2id
        self.stm1id=stm1id
        self.stm9xid=stm9xid
        self.basin=basin
        self.sname=sname
        self.stmDev=stmDev

        # -- output
        #
        self.trk={}
        
        # -- make trk and analyze
        #
        rc=self.makeTrkdata(verb=verb)
        rc=self.anlMDtrk()

    def getTrk4Cards(self,verb=0):
        
        undef=self.undef
        cards=self.cards
        itrk={}
        for card in cards:
            tt=card.split(',')
            dtg=tt[0].strip()
            ott=[]
            for t in tt[1:]:
                ott.append(t.strip())
            itrk[dtg]=ott
            
        idtgs=itrk.keys()
        idtgs.sort()
        
        if(self.verb):
            for idtg in idtgs:
                print 'iii',idtg,itrk[idtg]
            
        return(itrk,idtgs)
    
    def getTrkData4Itrk(self,dtg,ntrk,ndtgs,verb=0):
#     01W.2019', '', '11.2', '125.6', '20', '', '183', '9', '195', '8', '', '', '', '', '', '', '', '', '', '', 'NT', 'NW', 'c', 'c', '', '', '0.27', '', '', '', '', '---']   
        #     0   1      2        3     4    5     6    7      8    9   10  11  12  13  14  15  16  17  18  19   20    21    22   23  24  25     26   27  28  29  30    31
        trk=self.itrk[dtg]

        #if(self.verb):
            #for n in range(0,len(trk)):
                #print 'n:',n,trk[n]
            #sys.exit()

        # 33333333333333333333333
        #n: 0 d1w.2019
        #n: 1 9X-D1W
        #n: 2 TD
        #n: 3 NN
        #n: 4 18.0
        #n: 5 128.2
        #n: 6 15
        #n: 7 1010
        #n: 8 270
        #n: 9 6
        #n: 10 270
        #n: 11 6
        #n: 12 NaN
        #n: 13 NaN
        #n: 14 NaN
        #n: 15 NaN
        #n: 16 NaN
        #n: 17 NaN
        #n: 18 NaN
        #n: 19 NaN
        #n: 20 NaN
        #n: 21 NaN
        #n: 22 DB
        #n: 23 NW
        #n: 24 b
        #n: 25 b
        #n: 26 NaN
        #n: 27 NaN
        #n: 28 NaN
        #n: 29 NaN
        #n: 30 NaN
        #n: 31 NaN

        n=0
        stmid=trk[n] ; n=n+1                       # 0
        sname=trk[n] ; n=n+1                       # 1
        
        if(self.dom3): n=4
        
        rlat=float(trk[n]) ; n=n+1                 # 2
        rlon=float(trk[n]) ; n=n+1                 # 3       
        
        if(trk[n] != 'NaN' and trk[n] != '' ): vmax=float(trk[n])       # 4
        else: vmax=undef
        n=n+1

        if(trk[n] != 'NaN' and trk[n] != '' ): pmin=float(trk[n])       # 5
        else: pmin=undef
        n=n+1
        
        if(trk[n] != 'NaN'and trk[n] != '' ): dir=float(trk[n])        # 6
        else: dir=undef
        n=n+1

        if(trk[n] != 'NaN'and trk[n] != '' ): spd=float(trk[n])        # 7
        else: spd=undef
        n=n+1
        
        if(trk[n] != 'NaN' and trk[n] != '' ): trkdir=float(trk[n])     # 8
        else: trkdir=undef
        n=n+1

        if(trk[n] != 'NaN' and trk[n] != '' ): trkspd=float(trk[n])     # 9
        else: trkspd=undef
        n=n+1

        if(trk[n] != 'NaN' and trk[n] != '' ): r34m=float(trk[n])     #10
        else: r34m=undef
        n=n+1

        if(trk[n] != 'NaN' and trk[n] != '' ): r34ne=float(trk[n])     #11
        else: r34ne=undef
        n=n+1

        if(trk[n] != 'NaN' and trk[n] != '' ): r34se=float(trk[n])     #12
        else: r34se=undef
        n=n+1

        if(trk[n] != 'NaN' and trk[n] != '' ): r34sw=float(trk[n])     #13
        else: r34sw=undef
        n=n+1

        if(trk[n] != 'NaN' and trk[n] != '' ): r34nw=float(trk[n])     #14
        else: r34nw=undef
        n=n+1

        if(trk[n] != 'NaN' and trk[n] != '' ): r50m=float(trk[n])      #15
        else: r50m=undef
        n=n+1

        if(trk[n] != 'NaN' and trk[n] != '' ): r50ne=float(trk[n])     #16
        else: r50ne=undef
        n=n+1

        if(trk[n] != 'NaN' and trk[n] != '' ): r50se=float(trk[n])     #17
        else: r50se=undef
        n=n+1

        if(trk[n] != 'NaN' and trk[n] != '' ): r50sw=float(trk[n])     #18
        else: r50sw=undef
        n=n+1

        if(trk[n] != 'NaN' and trk[n] != '' ): r50nw=float(trk[n])     #19
        else: r50nw=undef
        n=n+1

        r34=[r34ne,r34se,r34sw,r34nw]
        r50=[r50ne,r50se,r50sw,r50nw]
        
        tccode=trk[n]     #20
        n=n+1

        wncode=trk[n]     #21
        n=n+1

        dirtype=trk[n]     #22
        n=n+1

        postype=trk[n]     #23
        n=n+1


        if(trk[n] != 'NaN' and trk[n] != '' ): roci=float(trk[n])   #24
        else: roci=undef
        n=n+1

        if(trk[n] != 'NaN' and trk[n] != '' ): poci=float(trk[n])   #25
        else: poci=undef
        n=n+1

        if(trk[n] != 'NaN'and trk[n] != '' ): alf=float(trk[n])   #26
        else: alf=undef
        n=n+1

        depth=trk[n]     #27
        n=n+1

        # -- bug in parseDssTrk
        #
        if(len(trk) > 30 and not(self.dom3)):
            unknown=trk[n]     #28
            n=n+1

        if(trk[n] != 'NaN' and trk[n] != '' ): rmax=float(trk[n])   #29
        else: rmax=undef
        n=n+1

        tdo=trk[n]   #30
        if(tdo == 'NaN' or tdo == '---'): tdo='   '
        n=n+1

        if(verb):
            print self.b1id,rlat,rlon,vmax,pmin,dir,spd
            print tccode,wncode,self.b1id,tdo,ntrk,ndtgs
            print r34m,r34m,r50m,depth
            print r34,r50,poci,roci,rmax
            
        self.trk[dtg]=Trkdata(rlat,rlon,vmax,pmin,dir,spd,\
                              tccode,wncode,b1id=self.b1id,tdo=tdo,ntrk=ntrk+1,ndtgs=ndtgs+1,
                              r34m=r34m,r50m=r50m,depth=depth,
                              r34=r34,r50=r50,poci=poci,roci=roci,
                              rmax=rmax)        
        
        self.trk[dtg].tdo=tdo
        self.trk[dtg].alf=alf
        self.trk[dtg].sname=sname
        self.trk[dtg].stmid=stmid
        self.trk[dtg].postype=postype
        self.trk[dtg].ostm2id=self.ostm2id
        
                
    def makeTrkdata(self,verb=0):
        
        ntrk=0
        ndtgs=0
        dtgs=self.idtgs
        for dtg in dtgs:
            if(verb): print 'ddd',dtg,len(self.itrk[dtg]),self.itrk[dtg]
            
            self.getTrkData4Itrk(dtg,ntrk,ndtgs)
            
            ntrk=ntrk+1
            ndtgs=ndtgs+1
            
            
        
        # -- get prev 12-h track dir/spd
        #
        dirspd={}
        for n in range(0,ndtgs):

            dtg=dtgs[n]
            if(n == 0):
                nm1=n
                if(ndtgs > 2):  n0=n+2
                else:           n0=n+1
            elif(n == 1):
                nm1=n-1
                if(ndtgs > 2):  n0=n+1
                else:           n0=n+1
            elif(n == ndtgs-1):
                nm1=n-2
                if(ndtgs > 2):  n0=n
                else:           n0=n
            else:
                nm1=n-2
                n0=n

            if(n0 > ndtgs-1):
                trkdir=self.undef
                trkspd=self.undef
            else:
                
                rlatm1=self.trk[dtgs[nm1]].rlat
                rlonm1=self.trk[dtgs[nm1]].rlon
                rlat0=self.trk[dtgs[n0]].rlat
                rlon0=self.trk[dtgs[n0]].rlon
                
                dt=dtgdiff(dtgs[nm1],dtgs[n0])
                (trkdir,trkspd,umotion,vmotion)=rumhdsp(rlatm1,rlonm1,rlat0,rlon0,dt)
                
            dirspd[dtg]=(trkdir,trkspd)

        self.ndtgs=ndtgs
        self.dtgs=dtgs

        # -- set the bt dir/spd and dirtype
        #
        for dtg in dtgs:
            
            self.trk[dtg].dirtype=self.trk[dtg].postype
            (trkdir,trkspd)=dirspd[dtg]

            if( (self.trk[dtg].dir == None)):
                (trkdir,trkspd)=dirspd[dtg]
                if(self.trk[dtg].postype == 'c'):
                    self.trk[dtg].dirtype='b'
                    
                self.trk[dtg].dir=trkdir   
                self.trk[dtg].spd=trkspd    
                
            self.trk[dtg].trkdir=trkdir   
            self.trk[dtg].trkspd=trkspd    
        
        
    def anlMDtrk(self,stmD=None,verb=0):

        (ltln,latmn,latmx,lonmn,lonmx,latb,lonb)=self.getlatlon()
        
        (gendtg,gendtgs,genstdd,time2gen,gendtgWN,gendtgBT)=self.getgenesis()
        if(self.sname != None): sname=self.sname
        else:
            sname=self.getname()
            
        (vmax,ace,stcd)=self.getvmax()
        (nRI,nED,nRW,dRI,dED,dRW)=self.getRI()
        (tclife,stclife,stmlife)=self.gettclife()
        syear=self.stm1id.split('.')[1]

        rc=getStmParams(self.stm1id)
        
        # -- if a warning is put, set stmlife to tcgen -- for 9X with warnings in the adecks
        #
        if(time2gen > 0 and Is9X(self.stm1id)):
            stmlife=time2gen/24.0


        if(self.verb):
            print 'FFFFFFFFFF(stm1|2id0:  ',self.stm2id,self.stm1id
            print 'FFFFFFFFFF(tclife):    ',tclife
            print 'FFFFFFFFFF(stclife):   ',stclife
            print 'FFFFFFFFFF(stmlife):   ',stmlife

            print 'FFFFFFFFFF(ace):       ',ace
            print 'FFFFFFFFFF(stcd):      ',stcd

            print 'FFFFFFFFFF(latb):      ',latb
            print 'FFFFFFFFFF(lonb):      ',lonb
            
            print 'FFFFFFFFFF(latmn):     ',latmn
            print 'FFFFFFFFFF(latmx):     ',latmx
            print 'FFFFFFFFFF(lonmn):     ',lonmn
            print 'FFFFFFFFFF(lonmx):     ',lonmx

            print 'FFFFFFFFFF(gendtg):    ',gendtg
            print 'FFFFFFFFFF(gendtgWN):  ',gendtgWN
            print 'FFFFFFFFFF(gendtgBT):  ',gendtgBT
            print 'FFFFFFFFFF(gendtgs):   ',gendtgs
            print 'FFFFFFFFFF(genstdd):   ',genstdd
            print 'FFFFFFFFFF(time2gen):  ',time2gen
            print 'FFFFFFFFFF(sname):     ',sname
            print 'FFFFFFFFFF(vmax):      ',vmax

            print 'FFFFFFFF(nRI):         ',nRI
            print 'FFFFFFFF(nED):         ',nED
            print 'FFFFFFFF(nRW):         ',nRW

            print 'FFFFFFFF(dRI):         ',dRI
            print 'FFFFFFFF(dED):         ',dED
            print 'FFFFFFFF(dRW):         ',dRW


        # -- decorate stm Dataset
        #
        
        self.gendtg=gendtg
        self.gendtgWN=gendtgWN
        self.gendtgBT=gendtgBT
        self.gendtgs=gendtgs
        self.genstdd=genstdd
        self.time2gen=time2gen

        self.sname=sname
        self.vmax=vmax

        self.ace=ace
        self.stcd=stcd

        self.tclife=tclife
        self.stclife=stclife
        self.stmlife=stmlife

        self.latb=latb
        self.lonb=lonb
        
        self.latmn=latmn
        self.lonmn=lonmn
        
        self.latmx=latmx
        self.lonmx=lonmx
    
        self.nRI=nRI
        self.nED=nED
        self.nRW=nRW
        self.dRI=dRI
        self.dED=dED
        self.dRW=dRW
        
        
        # -- adjust 9X dtgs
        #
        if(self.gendtg != None):
            dtg9Xs=dtgrange(self.dtgs[0],self.gendtg)
            if(len(dtg9Xs) > 0):
                for dtg9x in dtg9Xs[0:-1]:
                    if(dtg9x in self.dtgs):
                        self.trk[dtg9x].stmid=self.stm9xid

        
    def getRI(self,dvmaxRI=30,dvmaxED=50,dvmaxRD=-30):

        dRI=dED=-999
        dRW=999
        nRI=0
        nED=0
        nRW=0
        
        for dtg in self.dtgs:
            dtgm24=dtginc(dtg,-24)
            if(dtgm24 in self.dtgs):
                ttm24=self.trk[dtgm24]
                tt=self.trk[dtg]
                vmaxm24=ttm24.vmax
                vmax=tt.vmax
                if(vmax != None):
                    dvmax=vmax-vmaxm24
                else:
                    continue
                if(dvmax >= dvmaxRI):
                    nRI=nRI+1
                    if(dvmax > dRI and dvmax < dvmaxED): dRI=dvmax
                
                if(dvmax >= dvmaxED):
                    nED=nED+1
                    if(dvmax > dED): dED=dvmax

                if(dvmax <= dvmaxRD):
                    nRW=nRW+1
                    if(dvmax < dRW): dRW=dvmax
                

                

        return(nRI,nED,nRW,dRI,dED,dRW)

    def getvmax(self,ddtg=6):
        """assume ddtg=6h"""
        vmax=-999
        ace=0.0
        stcd=0.0
        n=0
        ns=0
        
        for dtg in self.dtgs:
            tt=self.trk[dtg]
            svmax=tt.vmax
            if(svmax > vmax and svmax != self.undef): vmax=tt.vmax

            tace=aceTC(svmax)
            if(tace > 0.0):
                ace=ace+tace*ddtg
                ns=ns+1

            stcd=stcd+scaledTC(svmax)
            n=n+1

        stcd=stcd*0.25

        if(ns > 0):
            ace=ace/(24.0*tymin*tymin)

        return(vmax,ace,stcd)




    def getname(self):

        sname='---------'
        snames=[]
        for dtg in self.dtgs:
            tt=self.trk[dtg]
            #if(tt.sname[0:5] != 'NONAME' and tt.sname[0:5] != 'INVES' and tt.sname != ''):
            if(tt.sname[0:5] == 'INVES' or tt.sname == ''):
                continue
            else:
                snames.append(tt.sname)

        snames=uniq(snames)
        return(sname)

        
    def getgenesis(self,dtgm=-18,dtgp=+12,vmaxTD=25.0,vmaxMin=10.0,verb=0):

        time2gen=-999.
        gendtg=gendtgWN=gendtgBT=None
        stdd=0.0
        
        gendtgs=[]
        genstd=None

        minvmax=1e20
        maxvmax=-1e20
        
        for dtg in self.dtgs:
            tt=self.trk[dtg]
            if(tt.wncode.lower() == 'wn' and gendtgWN == None): gendtgWN=dtg

        # -- if gendtg = None; then no warnings!  use when became tc...
        #
        tcCodeWind=0
        for dtg in self.dtgs:
            tt=self.trk[dtg]
            istc=IsTc(tt.tccode)
            # -- no this
            #if(tt.tccode == 'TW'): tcCodeWind=1
            if(istc >= 1 and gendtgBT == None): 
                tcCodeWind=1
                gendtgBT=dtg
                

        if(gendtgWN != None):
            if(tcCodeWind >= 0):  gendtg=gendtgWN
            else:                 gendtg=gendtgBT
            
        if(gendtg == None and gendtgBT != None): gendtg=gendtgBT
        
        if(gendtg != None):

            time2gen=dtgdiff(self.dtgs[0],gendtg)
            
            bdtg=dtginc(gendtg,dtgm)
            edtg=dtginc(gendtg,dtgp)
            gendtgs=dtgrange(bdtg,edtg)


            stddtime=0.0
            ngd=len(gendtgs)
            for n in range(1,ngd):
                dtgm1=gendtgs[n-1]
                dtg0=gendtgs[n]
                
                if(dtg0 in self.dtgs and dtgm1 in self.dtgs):

                    dtau=dtgdiff(dtgm1,dtg0)
                    ttm1=self.trk[dtgm1]
                    tt0=self.trk[dtg0]
                    
                    vmaxm1=ttm1.vmax
                    vmaxm0=tt0.vmax
                    if(vmaxm1 < 0): vmaxm1=vmaxMin
                    if(vmaxm0 < 0): vmaxm0=vmaxMin

                    if(vmaxm1 > maxvmax): maxvmax=vmaxm1
                    if(vmaxm1 < minvmax): minvmax=vmaxm1
                    if(vmaxm0 > maxvmax): maxvmax=vmaxm0
                    if(vmaxm0 < minvmax): minvmax=vmaxm0
                    
                    stdd=stdd+(((vmaxm1+vmaxm0)*0.5)/vmaxTD)*dtau
                    stddtime=stddtime+dtau

                    if(verb): print 'ggggggggggg ',dtau,dtg0,dtgm1,vmaxm1,vmaxm0,stdd,stddtime

            if(stddtime > 0.0):

                stdd=stdd/24.0
                if(verb): print 'ggggggggggg final stdd: ',stdd


        genstdd=stdd

        if(verb):
            print 'ggggggg ',gendtg
            print 'ggggggg ',gendtgWN
            print 'ggggggg ',gendtgBT
            print 'ggggggg ',gendtgs
            print 'ggggggg ',genstdd
            print 'ggggggg ',time2gen

        return(gendtg,gendtgs,genstdd,time2gen,gendtgWN,gendtgBT)
    
    def getlatlon(self):

        latb=0.0
        lonb=0.0
        
        latmn=999
        latmx=-999
        lonmn=999
        lonmx=-999

        latlon={}
        n=0
            
        for dtg in self.dtgs:
            tt=self.trk[dtg]

            tlat=tt.rlat
            if(n==0):  tlonPri=tt.rlon
            tlon=tt.rlon
            
            # -- cross prime meridion
            if(tlon < primeMeridianChk and tlonPri > primeMeridianChk): tlon=tlon+360.0
            
            if(tlat > latmx): latmx=tlat
            if(tlon > lonmx): lonmx=tlon
            if(tlat < latmn): latmn=tlat
            if(tlon < lonmn): lonmn=tlon
            n=n+1
            latb=latb+tlat
            lonb=lonb+tlon
            latlon[dtg]=(tlat,tlon)
            tlonPri=tlon

        if(n>0):
            latb=latb/n
            lonb=lonb/n

        ndtgs=len(self.dtgs)
        for n in range(0,ndtgs):
            dtg=self.dtgs[n]
            tt=self.trk[dtg]
            
        return(latlon,latmn,latmx,lonmn,lonmx,latb,lonb)


    def gettclife(self):

        tclife=0
        stclife=0
        stmlife=0
        
        ndtgs=len(self.dtgs)

        if(ndtgs == 0):
            return(tclife,stclife,stmlife)
            
        for n in range(1,ndtgs):
            tt=self.trk[self.dtgs[n]]
            dtau=dtgdiff(self.dtgs[n-1],self.dtgs[n])
            stmlife=stmlife+dtau
            if(IsTc(tt.tccode) == 1):
                tclife=tclife+dtau
            if(IsTc(tt.tccode) == 2):
                stclife=stclife+dtau
            
        tclife=tclife/24.0
        stclife=stclife/24.0
        stmlife=stmlife/24.0

        return(tclife,stclife,stmlife)
            

    def lsDSsDtgs(self,dtgs=None,dobt=0,dupchk=0,verb=0,selectNN=1,countsOnly=0,filtTCs=0,doprint=1):

        if(dtgs == None):
            dtgs=self.dtgs
        else:
            if(not(type(dtgs) is ListType)): dtgs=[dtgs]
            else: dtgs=dtgs
            
        itrk=None

        dobtLs=dobt
        if(filtTCs): dobtLs=1

        cards=[]
        ncards=0
        nstrms=0
        nstms=1
        stmid=self.stm1id
        sname=self.sname
        
        for dtg in dtgs:

            if(dtg in self.dtgs):
                
                gentrk=0
                if(dtg in self.gendtgs): gentrk=1
                trk=self.trk[dtg]
                card=printTrk(trk.stmid,dtg,trk.rlat,trk.rlon,trk.vmax,trk.pmin,
                              trk.dir,trk.spd,trk.dirtype,trk.tdo,
                              tccode=trk.tccode,wncode=trk.wncode,
                              r34m=trk.r34m,r50m=trk.r50m,alf=trk.alf,
                              ntrk=trk.ntrk,ndtgs=trk.ndtgs,
                              sname=sname,gentrk=gentrk,doprint=doprint)
                cards.append(card)
                ncards=ncards+1
                
        else:
            nstms=0
            nstmTCs=0
            
        if(countsOnly):
            if(filtTCs):
                print dtg,'N: ',nstmTCs
            else:
                print dtg,'N: ',nstms
                
        if(ncards == 0 and not(countsOnly)): 
            if(filtTCs): 
                print "%s-N"%(dtg),'   NNNNNNNNNNNNNN: filtTCs: ',filtTCs,' nstrms All: ',nstrms
            else:
                print "%s-N -- no storms for this dtg..."%(dtg)    

        return(cards)

    def lsDSsStmSummary(self,
                        doprint=1,warn=0):

        # -- season storm card
        #
        
        stmid=self.stm1id
        sname=self.sname
        if(hasattr(self,'m3tri')): 
            self=self.m3tri
        else:
            None

        if(hasattr(self,'ace')):

            curdtg=dtg()
            curdtgm6=dtginc(curdtg,-6)

            if(len(self.dtgs) == 0):
                if(warn): print 'DDDDDDDDDDDDDDDDDd nada dtgs for stmid: ',stmid
                return

            bdtg=self.dtgs[0]
            edtg=self.dtgs[-1]
            
            ostmid=stmid
                
                
            (snum,b1id,yyyy,b2id,stm2id,stm1id)=getStmParams(ostmid)

            stm=snum+b1id

            livestatus=' '
            tctype=TCType(self.vmax)
            edtgdiff=dtgdiff(edtg,curdtg)
            if(edtg == curdtg or edtg == curdtgm6 or edtgdiff <= 0.0): livestatus='*'
            RIstatus=' NaN '
            timeGen=' NaN '
            if(self.nRI > 0): RIstatus='rrRI'
            if(self.nED > 0): RIstatus='rrED'
            if(self.nRW > 0):
                RIstatus='ddRW'
                if(self.nRI > 0): RIstatus='ddRI'
                if(self.nED > 0): RIstatus='ddED'

                
            stm9x=''
            ostmid9x=self.stm9xid
                
            pad=''
            if(len(stm9x) > 0): pad=' '
            if(self.stmDev == None):
                if(IsNN(ostmid)):
                    stmDev='NN'
                elif(IsNN(ostmid9x)):
                    stmDev='DEV'
                else:
                    stmDev='nonDEV'
            else:
                stmDev=self.stmDev
            
            if(IsNN(ostmid9x)):
                stm9x=stm9x+pad+"NN , %s"%(ostmid9x.split('.')[0])
            else:
                stm9x=stm9x+pad+"9X , %s"%(ostmid9x.split('.')[0])


            otimeGen='NaN'
            if(hasattr(self,'time2gen') and not(Is9X(stmid))):
                if(self.time2gen >= 0.0):
                    timeGen="tG:%3.0f"%(self.time2gen)
                    otimeGen="%3.0f"%(self.time2gen)
                    
            oACE=self.ace
            if(Is9X(stmid)): oACE=0.0


            ovmax="%3d"%(self.vmax)
            if(self.vmax == self.undef): ovmax='***'

            #if(find(stmid,'CC')):
                #tctype='___'

                #ocard="%s %s%1s %3s %-10s :%s :%4.1f;%4.1f :%5.1f %5.1f :%s<->%s :%5.1f<->%-5.1f :%5.1f<->%-5.1f :%s"%\
                    #(yyyy,stm,livestatus,tctype,sname[0:9],ovmax,self.tclife,self.stmlife,self.latb,self.lonb,bdtg,edtg,
                     #self.latmn,self.latmx,self.lonmn,self.lonmx,
                     #stm9x)
            #else:

            try:
                n=int(stm[0:2])
                ogendtg="%s"%(self.gendtg)
            except:
                ogendtg='NaN'
                
            ogenType='NaN'
            if(IsNN(stmid)):
                if(self.gendtgWN != None): ogenType='wn'
                if(self.gendtgWN == None and self.gendtgBT != None): ogenType='bt'

            ocard="%s.%s ,  %3s , %s , %s , %s , %5.1f , %5.1f , %5.1f , %5.1f , \
%s , %s , %5.1f , %-5.1f , %5.1f , %-5.1f , %4.1f , %4.1f , \
%2d , %2d , %2d , %s , %s , %s , %s , %s"%\
                                    (stm,yyyy,tctype,stmDev,sname,ovmax,self.tclife,self.stmlife,self.latb,self.lonb,bdtg,edtg,
                                     self.latmn,self.latmx,self.lonmn,self.lonmx,
                                     self.stcd,oACE,
                                     self.nRI,self.nED,self.nRW,
                                     RIstatus,stm9x,otimeGen,ogendtg,ogenType)

                
                
            rcsum=(tctype,stmDev)
            if(doprint): 
                print ocard
            return(ocard,rcsum)


class prTCMean(MFbase):
    
    
    def __init__(self,
                 dtg,ctlpath,
                 prvar='pr',
                 undef=-999.,
                 verb=0):
        
        self.dtg=dtg
        self.ctlpath=ctlpath
        self.undef=undef
        self.verb=verb
        self.prvar=prvar

        ga=setGA(Quiet=1)
        try:
            ga.open(ctlpath)
        except:
            print 'EEE-prTCmean opening: ',ctlpath
            self=None
            return(self)
        self.ctlpath=ctlpath
        self.ga=ga
        self.ge=ga.ge
        

    def setGrads(self,sdtg=None,tau=0,regrid=0.5):
        
        idtg=self.dtg
        if(sdtg != None): idtg=sdtg
        fdtg=dtginc(idtg,tau)
        gtime=dtg2gtime(fdtg)
        try:
            self.ga('set time %s'%(gtime))
        except:
            print 'EEE-setGrads: ',gtime,self.ctlpath
        self.prMH={}
        self.prM={}
        
    def setTcprop(self,clat,clon,r,bearing=270,verb=0):
        #expr='pr1=re(pr,1)'
        #self.ga(expr)
        expr='tcprop %s %f %f %f %f'%(self.prvar,clat,clon,r,bearing)
        if(verb): print 'expr: ',expr,self.dtg,self.ctlpath
        
        try:
            self.ga(expr)
            cards=self.ga.Lines
        except:
            print 'EEE-setTCprop: ',expr,self.dtg,self.ctlpath
            cards=[]
        
        cprm=prm=prmh1=prmh2=None
        cprm=prm=prmh1=prmh2=-99.
        
        for card in cards:
            if(find(card,'MeanRadinf')): 
                prm=card.split()[-1]
                prm=float(prm)
                if(prm > 9999.): prm=-99.
                cprm="%5.1f"%(prm)
                #cprm=float(cprm)
                if(verb): print '  prm: ',float(prm)
                
            elif(find(card,'MeanHemi1')): 
                prmh1=card.split()[1]
                prmh2=card.split()[-1]
                if(prmh1 > 9999.): prmh1=-99.
                if(prmh2 > 9999.): prmh2=-99.
                if(verb): print 'prmh1: ',float(prmh1)
                if(verb): print 'prmh2: ',float(prmh2)
                
        self.prMH[r]=[prm,prmh1,prmh2]
        self.prM[r]=cprm
        
class superBT(Mdeck3):
    
    sbtTSmeta={}
    sMdesc={}
    
    btime=-240
    btime=-144
    etime=0
    dtime=6
    
    # -- max # of times for an individual storm
    #
    maxTimes=100
    
    def __init__(self,
                 version,
                 tbdir=None,
                 oyearOpt=None,
                 verb=0,
                 doclean=0,
                 dochk=0,
                  ):
        

        self.sTimer('sbt-init')
        self.verb=verb
        self.version=version

        # -- meta
        #
        smcards=open('%s/%s'%(sbtVerDirDat,sbtMeta)).readlines()

        for n in range(0,len(smcards)):
            tt=smcards[n].split(',')
            tt0=tt[0].replace("\n",'')
            tt1=tt[1].replace("\n",'')
            #print n,tt0,tt1
            self.sbtTSmeta[n]=tt0
            self.sMdesc[tt0]=tt1
        #sys.exit()

        sM=self.sbtTSmeta
        self.sMv=self.sbtTSmeta
            
        if(verb):
            kk=self.sMv.keys()
            kk.sort()
            for k in kk:
                print 'sMv ',k,self.sMv[k]
        

        self.tbdir="%s/dat"%(sbtVerDir)
        self.gadatDir="%s/gadat"%(sbtVerDir)
        MF.ChkDir(self.gadatDir,'mk')
        
        if(oyearOpt == None):
            oyearOpt='%s-%s'%(bm3year,em3year)
        
        oyearOpt="%s"%(oyearOpt)
        self.oyearOpt=oyearOpt
        
        sbtCvsPath="%s/sbt-%s-%s-MRG.csv"%(sbtVerDirDat,version,oyearOpt)
        sumCvsPath="%s/sum-md3-%s-MRG.csv"%(sbtVerDirDat,oyearOpt)

        # -- 111 -- get the storm meta data
        #
        stmSum={}
        tcNamesHash={}
        scards=open(sumCvsPath).readlines()
        for scard in scards[1:]:
            #print scard[0:-1]
            tt=scard.split(',')
            stmid=tt[0]
            ss=stmid.split(".")
            year=ss[1]
            b3id=ss[0]
            tccode=tt[1]
            tcdev=tt[2]
            name=tt[3]
            tcNamesHash[(year,b3id)]=name
            stmSum[stmid]=tt
        self.stmSum=stmSum
        self.tcNamesHash=tcNamesHash
        
        # -- 222 -- get the superBT
        #
        sbtNN={}
        sbtDev={}
        sbtNonDev={}
        
        sbtNNdtgs={}
        sbtDevdtgs={}
        sbtNonDevdtgs={}
        
        stmsNon=[]
        stmsDev=[]
        stmsNN=[]
        
        scards=open(sbtCvsPath).readlines()
        for scard in scards[1:]:
            #print scard[0:-1]
            scard=scard.replace(' ','')
            tt=scard.split(',')
            ltt=len(tt)

            if(ltt != 51 and tt[-2] == 'NaN'):
                if(dochk): print 'nnn',ltt,tt[-2],tt
                continue
            else:
                if(dochk): print 'ggg',ltt,tt[0]
                
            stmid=tt[0]
            dtg=tt[3]
            stmDev=tt[2]
            if(stmDev == 'NN'):
                MF.appendDictList(sbtNN, stmid, tt)
                MF.appendDictList(sbtNNdtgs, stmid, dtg)
            elif(stmDev == 'DEV'):
                MF.appendDictList(sbtDev,stmid,tt)
                MF.appendDictList(sbtDevdtgs,stmid,dtg)
            elif(stmDev == 'NONdev'):
                MF.appendDictList(sbtNonDev,stmid, tt)
                MF.appendDictList(sbtNonDevdtgs,stmid, dtg)
                
        stmsNon=sbtNonDev.keys()
        stmsNon.sort()
        
        stmsDev=sbtDev.keys()
        stmsDev.sort
        
        stmsNN=sbtNN.keys()
        stmsNN.sort()
        
        self.sbtNN=sbtNN
        self.sbtDev=sbtDev
        self.sbtNonDev=sbtNonDev
        
        self.sbtNNdtgs=sbtNNdtgs
        self.sbtDevdtgs=sbtDevdtgs
        self.sbtNonDevdtgs=sbtNonDevdtgs
                
        self.stmsNon=stmsNon
        self.stmsDev=stmsDev
        self.stmsNN=stmsNN
        
        # -- make txaxis and xvalsU for TS analysis using grads
        #
        self.makeSbtTSTaxis()
        self.dTimer('sbt-init')

    
    def parseSbt(self,sbt):
        
    #'m3stmid','storm id in NNB.YYYY format'
    #'m3tcType','TC lifetype type: TD (tropical depression <= 34 kt); TS (tropical storm >= 35 kt); TY (typhoon >= 65 kt); STY (super typhoon >= 130 kt)'
    #'m3stmType','TC type NN - numbered TC, NONdev - non-developing pTC; DEV - pTC that developed into NN storm'
    #'dtg','date-time-group YYYYMMDDHH'
    #'blat','best track latitude degN'
    #'blon','best track longitude degE'
    #'bvmax','best track Vmax [kts]'
    #'bpmin','best track central pressure [hPa]'
    #'bdir','best track direction of motion [deg]'
    #'bspd','best track speed [kt]'
    #'btccode','best track TC code'
    #'br34m','best track mean R34 [km]'
    #'land','distance from coast [km]'
    #'mvmax','model Vmax [kts]'
    #'r34m','mean r34 km for diag calc'
    #'shrspd','850-200 hPa shear speed kts'
    #'shrdir','850-200 hPa shear direction deg'
    #'stmspd','storm speed in diagnostic file calc'
    #'stmdir','storm direction of motion in diagnostic file calc'
    #'sst','SST ERA5 degC'
    #'ssta','SST anomaly degC'
    #'vort850','850 hPa relative vorticity'
    #'dvrg200','200 hPa divergence'
    #'cpsb','CPS baroclinic'
    #'cpslo','CPS low: 1000-600 thickness'
    #'cpshi','CPS hi:   600-200 thickness'
    #'tpw','total precipitable water'
    #'rh50','relative humidity 500 hPa'
    #'rh70','relative humidity 700 hPa'
    #'rh85','relative humidity 850 hPa'
    #'u85','u wind 850 hPa'
    #'u70','u wind 700 hPa'
    #'u50','u wind 500 hPa'
    #'v85','v wind 850 hPa'
    #'v70','v wind 700 hPa'
    #'v50','v wind 500 hPa'
    #'roci1','roci of penultimate contour'
    #'poci1','poci of penultimate contour'
    #'roci0','roci outermost contour'
    #'poci0','poci outermost contour'
    #'to3','title'
    #'oc3','CMORPH 300-km precip at Best Track position [mm/d]'
    #'og3','GSMaP  300-km precip at Best Track position [mm/d]'
    #'oi3','IMERG  300-km precip at Best Track position [mm/d]'
    #'to5','title'
    #'oc5','CMORPH 500-km precip at Best Track position [mm/d]'
    #'og5','GSMaP  500-km precip at Best Track position [mm/d]'
    #'oi5','IMERG  500-km precip at Best Track position [mm/d]'
    #'to8','title'
    #'oc8','CMORPH 800-km precip at Best Track position [mm/d]'
    #'og8','GSMaP  800-km precip at Best Track position [mm/d]'
    #'oi8','IMERG  800-km precip at Best Track position [mm/d]'
    #'toe3','title'
    #'ec3','CMORPH 300-km precip at ERA5 position [mm/d]'
    #'eg3','GSMaP  300-km precip at ERA5 position [mm/d]'
    #'ei3','IMERG  300-km precip at ERA5 position [mm/d]'
    #'te3','title'
    #'e3','ERA5 500-km precip [mm/d]'
    #'re3','ERA5 ratio Convective/Total 300-km precip [%]'
    #'toe5','title'
    #'ec5','CMORPH 500-km precip at ERA5 position [mm/d]'
    #'eg5','GSMaP 500-km precip at ERA5 position [mm/d]'
    #'ei5','IMERG 500-km precip at ERA5 position [mm/d]'
    #'te5','title'
    #'e5','ERA5 500-km precip [mm/d]'
    #'re5','ERA5 ratio Convective/Total 500-km precip [%]'
    #'toe8','title'
    #'ec8','CMORPH 800-km precip at ERA5 position [mm/d]'
    #'eg8','GSMaP 800-km precip at ERA5 position [mm/d]'
    #'ei8','IMERG 800-km precip at ERA5 position [mm/d]'
    #'te8','title era5 pr'
    #'e8','ERA5 800-km precip [mm/d]'
    #'re8','ERA5 ratio Convective/Total 800-km precip [%]'        
       
        #n 0 a0w.2019 'm3stmid'
        #n 1 TD 'm3tcType'
        #n 2 DEV 'm3stmType'
        #n 3 2019010306 'dtg'
        #n 4 3.1 'blat'
        #n 5 174.8 'blon'
        #n 6 20 'bvmax'
        #n 7 1007 'bpmin'
        #n 8 231 'bdir'
        #n 9 13 'bspd'
        #n 10 DB 'btccode'
        #n 11 -999.0 'br34m'
        #n 12 3040 'land'
        #n 13 21 'mvmax'
        #n 14 -999 'r34m'
        #n 15 17 'shrspd'
        #n 16 339 'shrdir'
        #n 17 5 'stmspd'
        #n 18 233 'stmdir'
        #n 19 30.0 'sst'
        #n 20 1.5 'ssta'
        #n 21 119 'vort850'
        #n 22 132 'dvrg200'
        #n 23 -4 'cpsb'
        #n 24 2 'cpslo'
        #n 25 8 'cpshi'
        #n 26 65 'tpw'
        #n 27 79 'rh50'
        #n 28 78 'rh70'
        #n 29 87 'rh85'
        #n 30 -38 'u85'
        #n 31 10 'u70'
        #n 32 66 'u50'
        #n 33 9 'v85'
        #n 34 44 'v70'
        #n 35 56 'v50'
        #n 36 -999 'roci1'
        #n 37 -999 'poci1'
        #n 38 -999 'roci0'
        #n 39 -999 'poci0'
        #n 40 O3 'to3'
        #n 41 20.3 'oc3'
        #n 42 16.7 'og3'
        #n 43 16.2 'oi3'
        #n 44 O5 'to5'
        #n 45 29.8 'oc5'
        #n 46 35.4 'og5'
        #n 47 34.2 'oi5'
        #n 48 O8 'to8'
        #n 49 26.5 'oc8'
        #n 50 36.3 'og8'
        #n 51 28.3 'oi8'
        #n 52 OE3 'toe3'
        #n 53 29.0 'ec3'
        #n 54 27.9 'eg3'
        #n 55 38.8 'ei3'
        #n 56 E3 'te3'
        #n 57 37.8 'e3'
        #n 58 67 're3'
        #n 59 OE5 'toe5'
        #n 60 36.4 'ec5'
        #n 61 51.5 'eg5'
        #n 62 43.7 'ei5'
        #n 63 E5 'te5'
        #n 64 32.5 'e5'
        #n 65 55 're5'
        #n 66 OE8 'toe8'
        #n 67 28.2 'ec8'
        #n 68 39.0 'eg8'
        #n 69 29.5 'ei8'
        #n 70 E8 'te8'
        #n 71 23.1 'e8'
        #n 72 45 're8'


        #for n in range(0,len(sbt)):
            #print 'n',n,sbt[n].strip(),self.sMv[n]
        #sys.exit()

        sbtDict={}
        
        n=3
        dtg=sbt[n] ; n=n+1
        blat=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=blat ; n=n+1
        blon=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=blon ; n=n+1
        bvmax=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=bvmax ; n=n+1
        bpmin=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=bpmin ; n=n+1
        bdir=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=bdir ; n=n+1
        bspd=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=bdir ; n=n+1
        btccode=sbt[n] ; sbtDict[self.sMv[n]]=bdir ; n=n+1
        br34m=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=bdir ; n=n+1
        land=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=bdir ; n=n+1
        mvmax=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=bdir ; n=n+1
        mr34m=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=bdir ; n=n+1
        shrspd=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=shrspd ; n=n+1
        shrdir=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=shrdir ; n=n+1
        stmspd=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=stmspd ; n=n+1
        stmdir=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=stmdir ; n=n+1
        sst=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=sst ; n=n+1
        ssta=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=ssta ; n=n+1
        vrt850=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=vrt850 ; n=n+1
        div200=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=div200 ; n=n+1
        cpsb=mkFloat(sbt[n])  ; sbtDict[self.sMv[n]]=cpsb ; n=n+1
        cpslo=mkFloat(sbt[n])  ; sbtDict[self.sMv[n]]=cpslo ; n=n+1
        cpshi=mkFloat(sbt[n])  ; sbtDict[self.sMv[n]]=cpshi ; n=n+1
        tpw=mkFloat(sbt[n])  ; sbtDict[self.sMv[n]]=tpw ; n=n+1
        rh500=mkFloat(sbt[n])  ; sbtDict[self.sMv[n]]=rh500 ; n=n+1
        rh700=mkFloat(sbt[n])  ; sbtDict[self.sMv[n]]=rh700 ; n=n+1
        rh850=mkFloat(sbt[n])  ; sbtDict[self.sMv[n]]=rh850 ; n=n+1
        u500=mkFloat(sbt[n])  ; sbtDict[self.sMv[n]]=u500 ; n=n+1
        u700=mkFloat(sbt[n])  ; sbtDict[self.sMv[n]]=u700 ; n=n+1
        u850=mkFloat(sbt[n])  ; sbtDict[self.sMv[n]]=u850 ; n=n+1
        v500=mkFloat(sbt[n])  ; sbtDict[self.sMv[n]]=v500 ; n=n+1
        v700=mkFloat(sbt[n])  ; sbtDict[self.sMv[n]]=v700 ; n=n+1
        v850=mkFloat(sbt[n])  ; sbtDict[self.sMv[n]]=v850 ; n=n+1
        roci1=mkFloat(sbt[n])  ; sbtDict[self.sMv[n]]=roci1 ; n=n+1
        poci1=mkFloat(sbt[n])  ; sbtDict[self.sMv[n]]=poci1 ; n=n+1
        roci0=mkFloat(sbt[n])  ; sbtDict[self.sMv[n]]=roci0 ; n=n+1
        poci0=mkFloat(sbt[n])  ; sbtDict[self.sMv[n]]=poci0 ; n=n+1 

        if(len(sbt) > 41):
            n=41
            oprc3=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=oprc3 ; n=n+1
            oprg3=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=oprg3 ; n=n+1
            opri3=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=opri3 ; n=n+2 
            oprc5=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=oprc5 ; n=n+1
            oprg5=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=oprg5 ; n=n+1 
            opri5=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=opri5 ; n=n+2
            oprc8=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=oprc8 ; n=n+1
            oprg8=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=oprg8 ; n=n+1
            opri8=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=opri8 ; n=n+2
            
            eprc3=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=eprc3 ; n=n+1
            eprg3=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=eprg3 ; n=n+1
            epri3=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=epri3 ; n=n+2
            epre3=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=epre3 ; n=n+1
            eprr3=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=eprr3 ; n=n+2
            
            eprc5=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=eprc5 ; n=n+1
            eprg5=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=eprg5 ; n=n+1
            epri5=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=epri5 ; n=n+2
            epre5=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=epre5 ; n=n+1
            eprr5=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=eprr5 ; n=n+2

            eprc8=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=eprc8 ; n=n+1
            eprg8=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=eprg8 ; n=n+1
            epri8=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=epri8 ; n=n+2
            epre8=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=epre8 ; n=n+1
            eprr8=mkFloat(sbt[n]) ; sbtDict[self.sMv[n]]=eprr8 
            
        else:
            oprc8=oprg8=opri8=undef
            oprc5=oprg5=opri5=undef
            oprc3=oprg3=opri3=undef
            
            eprc8=eprg8=epri8=epre8=eprr8=undef
            eprc5=eprg5=epri5=epre5=eprr5=undef
            eprc3=eprg3=epri3=epre3=eprr3=undef
            
        
        rc=(dtg,blat,blon,bvmax,bpmin,bdir,bspd,btccode,br34m,
            land,mvmax,shrspd,shrdir,stmspd,stmdir,
            sst,ssta,
            vrt850,div200,
            cpsb,cpslo,cpshi,tpw,
            rh500,rh700,rh850,
            u500,u700,u850,
            v500,v700,v850,
            roci1,poci1,roci0,poci0,
            oprc3,oprg3,opri3,
            oprc5,oprg5,opri5,
            oprc8,oprg8,opri8,
            eprc3,eprg3,epri3,epre3,eprr3,
            eprc5,eprg5,epri5,epre5,eprr5,
            eprc8,eprg8,epri8,epre8,eprr8)
        
        
        #print sbt
        #print rc
        #sys.exit()
        return(rc)

    def parseSbtDict(self,sbt):
        
    #'m3stmid','storm id in NNB.YYYY format'
    #'m3tcType','TC lifetype type: TD (tropical depression <= 34 kt); TS (tropical storm >= 35 kt); TY (typhoon >= 65 kt); STY (super typhoon >= 130 kt)'
    #'m3stmType','TC type NN - numbered TC, NONdev - non-developing pTC; DEV - pTC that developed into NN storm'
    #'dtg','date-time-group YYYYMMDDHH'
    #'blat','best track latitude degN'
    #'blon','best track longitude degE'
    #'bvmax','best track Vmax [kts]'
    #'bpmin','best track central pressure [hPa]'
    #'bdir','best track direction of motion [deg]'
    #'bspd','best track speed [kt]'
    #'btccode','best track TC code'
    #'br34m','best track mean R34 [km]'
    #'land','distance from coast [km]'
    #'mvmax','model Vmax [kts]'
    #'r34m','mean r34 km for diag calc'
    #'shrspd','850-200 hPa shear speed kts'
    #'shrdir','850-200 hPa shear direction deg'
    #'stmspd','storm speed in diagnostic file calc'
    #'stmdir','storm direction of motion in diagnostic file calc'
    #'sst','SST ERA5 degC'
    #'ssta','SST anomaly degC'
    #'vort850','850 hPa relative vorticity'
    #'dvrg200','200 hPa divergence'
    #'cpsb','CPS baroclinic'
    #'cpslo','CPS low: 1000-600 thickness'
    #'cpshi','CPS hi:   600-200 thickness'
    #'tpw','total precipitable water'
    #'rh50','relative humidity 500 hPa'
    #'rh70','relative humidity 700 hPa'
    #'rh85','relative humidity 850 hPa'
    #'u85','u wind 850 hPa'
    #'u70','u wind 700 hPa'
    #'u50','u wind 500 hPa'
    #'v85','v wind 850 hPa'
    #'v70','v wind 700 hPa'
    #'v50','v wind 500 hPa'
    #'roci1','roci of penultimate contour'
    #'poci1','poci of penultimate contour'
    #'roci0','roci outermost contour'
    #'poci0','poci outermost contour'
    #'to3','title'
    #'oc3','CMORPH 300-km precip at Best Track position [mm/d]'
    #'og3','GSMaP  300-km precip at Best Track position [mm/d]'
    #'oi3','IMERG  300-km precip at Best Track position [mm/d]'
    #'to5','title'
    #'oc5','CMORPH 500-km precip at Best Track position [mm/d]'
    #'og5','GSMaP  500-km precip at Best Track position [mm/d]'
    #'oi5','IMERG  500-km precip at Best Track position [mm/d]'
    #'to8','title'
    #'oc8','CMORPH 800-km precip at Best Track position [mm/d]'
    #'og8','GSMaP  800-km precip at Best Track position [mm/d]'
    #'oi8','IMERG  800-km precip at Best Track position [mm/d]'
    #'toe3','title'
    #'ec3','CMORPH 300-km precip at ERA5 position [mm/d]'
    #'eg3','GSMaP  300-km precip at ERA5 position [mm/d]'
    #'ei3','IMERG  300-km precip at ERA5 position [mm/d]'
    #'te3','title'
    #'e3','ERA5 500-km precip [mm/d]'
    #'re3','ERA5 ratio Convective/Total 300-km precip [%]'
    #'toe5','title'
    #'ec5','CMORPH 500-km precip at ERA5 position [mm/d]'
    #'eg5','GSMaP 500-km precip at ERA5 position [mm/d]'
    #'ei5','IMERG 500-km precip at ERA5 position [mm/d]'
    #'te5','title'
    #'e5','ERA5 500-km precip [mm/d]'
    #'re5','ERA5 ratio Convective/Total 500-km precip [%]'
    #'toe8','title'
    #'ec8','CMORPH 800-km precip at ERA5 position [mm/d]'
    #'eg8','GSMaP 800-km precip at ERA5 position [mm/d]'
    #'ei8','IMERG 800-km precip at ERA5 position [mm/d]'
    #'te8','title era5 pr'
    #'e8','ERA5 800-km precip [mm/d]'
    #'re8','ERA5 ratio Convective/Total 800-km precip [%]'        
       
        #n 0 a0w.2019 'm3stmid'
        #n 1 TD 'm3tcType'
        #n 2 DEV 'm3stmType'
        #n 3 2019010306 'dtg'
        #n 4 3.1 'blat'
        #n 5 174.8 'blon'
        #n 6 20 'bvmax'
        #n 7 1007 'bpmin'
        #n 8 231 'bdir'
        #n 9 13 'bspd'
        #n 10 DB 'btccode'
        #n 11 -999.0 'br34m'
        #n 12 3040 'land'
        #n 13 21 'mvmax'
        #n 14 -999 'r34m'
        #n 15 17 'shrspd'
        #n 16 339 'shrdir'
        #n 17 5 'stmspd'
        #n 18 233 'stmdir'
        #n 19 30.0 'sst'
        #n 20 1.5 'ssta'
        #n 21 119 'vort850'
        #n 22 132 'dvrg200'
        #n 23 -4 'cpsb'
        #n 24 2 'cpslo'
        #n 25 8 'cpshi'
        #n 26 65 'tpw'
        #n 27 79 'rh50'
        #n 28 78 'rh70'
        #n 29 87 'rh85'
        #n 30 -38 'u85'
        #n 31 10 'u70'
        #n 32 66 'u50'
        #n 33 9 'v85'
        #n 34 44 'v70'
        #n 35 56 'v50'
        #n 36 -999 'roci1'
        #n 37 -999 'poci1'
        #n 38 -999 'roci0'
        #n 39 -999 'poci0'
        #n 40 O3 'to3'
        #n 41 20.3 'oc3'
        #n 42 16.7 'og3'
        #n 43 16.2 'oi3'
        #n 44 O5 'to5'
        #n 45 29.8 'oc5'
        #n 46 35.4 'og5'
        #n 47 34.2 'oi5'
        #n 48 O8 'to8'
        #n 49 26.5 'oc8'
        #n 50 36.3 'og8'
        #n 51 28.3 'oi8'
        #n 52 OE3 'toe3'
        #n 53 29.0 'ec3'
        #n 54 27.9 'eg3'
        #n 55 38.8 'ei3'
        #n 56 E3 'te3'
        #n 57 37.8 'e3'
        #n 58 67 're3'
        #n 59 OE5 'toe5'
        #n 60 36.4 'ec5'
        #n 61 51.5 'eg5'
        #n 62 43.7 'ei5'
        #n 63 E5 'te5'
        #n 64 32.5 'e5'
        #n 65 55 're5'
        #n 66 OE8 'toe8'
        #n 67 28.2 'ec8'
        #n 68 39.0 'eg8'
        #n 69 29.5 'ei8'
        #n 70 E8 'te8'
        #n 71 23.1 'e8'
        #n 72 45 're8'


        #for n in range(0,len(sbt)):
            #print 'n',n,sbt[n].strip(),self.sMv[n]
        #sys.exit()

        sbtDict={}
        
        n=3
        dtg=sbt[n] ; n=n+1
        blat=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=blat ; n=n+1
        blon=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=blon ; n=n+1
        bvmax=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=bvmax ; n=n+1
        bpmin=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=bpmin ; n=n+1
        bdir=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=bdir ; n=n+1
        bspd=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=bspd ; n=n+1
        btccode=sbt[n] ; sbtDict[self.sMv[n]]=btccode ; n=n+1
        br34m=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=br34m ; n=n+1
        land=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=land ; n=n+1
        mvmax=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=mvmax ; n=n+1
        mr34m=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=mr34m ; n=n+1
        shrspd=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=shrspd ; n=n+1
        shrdir=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=shrdir ; n=n+1
        stmspd=mkFloatU(sbt[n]) 
        # -- bug in lsdiag for best track at end ... undefined to 100, use bspd
        if(stmspd > 90.0): 
            stmspd=bspd
        sbtDict[self.sMv[n]]=stmspd ; n=n+1
        stmdir=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=stmdir ; n=n+1
        sst=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=sst ; n=n+1
        ssta=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=ssta ; n=n+1
        vrt850=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=vrt850 ; n=n+1
        div200=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=div200 ; n=n+1
        cpsb=mkFloatU(sbt[n])  ; sbtDict[self.sMv[n]]=cpsb ; n=n+1
        cpslo=mkFloatU(sbt[n])  ; sbtDict[self.sMv[n]]=cpslo ; n=n+1
        cpshi=mkFloatU(sbt[n])  ; sbtDict[self.sMv[n]]=cpshi ; n=n+1
        tpw=mkFloatU(sbt[n])  ; sbtDict[self.sMv[n]]=tpw ; n=n+1
        rh500=mkFloatU(sbt[n])  ; sbtDict[self.sMv[n]]=rh500 ; n=n+1
        rh700=mkFloatU(sbt[n])  ; sbtDict[self.sMv[n]]=rh700 ; n=n+1
        rh850=mkFloatU(sbt[n])  ; sbtDict[self.sMv[n]]=rh850 ; n=n+1
        u500=mkFloatU(sbt[n])  ; sbtDict[self.sMv[n]]=u500 ; n=n+1
        u700=mkFloatU(sbt[n])  ; sbtDict[self.sMv[n]]=u700 ; n=n+1
        u850=mkFloatU(sbt[n])  ; sbtDict[self.sMv[n]]=u850 ; n=n+1
        v500=mkFloatU(sbt[n])  ; sbtDict[self.sMv[n]]=v500 ; n=n+1
        v700=mkFloatU(sbt[n])  ; sbtDict[self.sMv[n]]=v700 ; n=n+1
        v850=mkFloatU(sbt[n])  ; sbtDict[self.sMv[n]]=v850 ; n=n+1
        roci1=mkFloatU(sbt[n])  ; sbtDict[self.sMv[n]]=roci1 ; n=n+1
        poci1=mkFloatU(sbt[n])  ; sbtDict[self.sMv[n]]=poci1 ; n=n+1
        roci0=mkFloatU(sbt[n])  ; sbtDict[self.sMv[n]]=roci0 ; n=n+1
        poci0=mkFloatU(sbt[n])  ; sbtDict[self.sMv[n]]=poci0 ; n=n+1 

        if(len(sbt) > 41):
            n=41
            oprc3=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=oprc3 ; n=n+1
            oprg3=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=oprg3 ; n=n+1
            opri3=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=opri3 ; n=n+2 
            oprc5=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=oprc5 ; n=n+1
            oprg5=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=oprg5 ; n=n+1 
            opri5=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=opri5 ; n=n+2
            oprc8=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=oprc8 ; n=n+1
            oprg8=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=oprg8 ; n=n+1
            opri8=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=opri8 ; n=n+2
            
            eprc3=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=eprc3 ; n=n+1
            eprg3=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=eprg3 ; n=n+1
            epri3=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=epri3 ; n=n+2
            epre3=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=epre3 ; n=n+1
            eprr3=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=eprr3 ; n=n+2
            
            eprc5=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=eprc5 ; n=n+1
            eprg5=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=eprg5 ; n=n+1
            epri5=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=epri5 ; n=n+2
            epre5=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=epre5 ; n=n+1
            eprr5=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=eprr5 ; n=n+2

            eprc8=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=eprc8 ; n=n+1
            eprg8=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=eprg8 ; n=n+1
            epri8=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=epri8 ; n=n+2
            epre8=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=epre8 ; n=n+1
            eprr8=mkFloatU(sbt[n]) ; sbtDict[self.sMv[n]]=eprr8 
            
        else:
            oprc8=oprg8=opri8=undef
            oprc5=oprg5=opri5=undef
            oprc3=oprg3=opri3=undef
            
            eprc8=eprg8=epri8=epre8=eprr8=undef
            eprc5=eprg5=epri5=epre5=eprr5=undef
            eprc3=eprg3=epri3=epre3=eprr3=undef
            
        
        rc=(dtg,blat,blon,bvmax,bpmin,bdir,bspd,btccode,br34m,
            land,mvmax,shrspd,shrdir,stmspd,stmdir,
            sst,ssta,
            vrt850,div200,
            cpsb,cpslo,cpshi,tpw,
            rh500,rh700,rh850,
            u500,u700,u850,
            v500,v700,v850,
            roci1,poci1,roci0,poci0,
            oprc3,oprg3,opri3,
            oprc5,oprg5,opri5,
            oprc8,oprg8,opri8,
            eprc3,eprg3,epri3,epre3,eprr3,
            eprc5,eprg5,epri5,epre5,eprr5,
            eprc8,eprg8,epri8,epre8,eprr8)
        
        
        #print sbt
        #print rc
        #sys.exit()
        return(dtg,sbtDict)
    
    def setsbtTS(self,stmid,sbtType,btime,doDict=1,warn=0,verb=1):
    
        #smeta=self.stmSum[stmid]
        if(sbtType == 'NONdev'):
            sbts=self.sbtNonDev[stmid]
            sdtgs=self.sbtNonDevdtgs[stmid]
        elif(sbtType == 'DEV'):
            sbts=self.sbtDev[stmid]
            sdtgs=self.sbtDevdtgs[stmid]

        sbtUndef=[]
        for n in range(0,21):
            sbtUndef.append(undef)
            
        sdtgs.sort()
        edtg=sdtgs[-1]
        bdtg=sdtgs[0]
        sbtTS={}
        tdtgs=dtgrange(bdtg,edtg,6)
        for tdtg in tdtgs:
            stime=dtgdiff(edtg, tdtg)
            sbtTS[stime]=sbtUndef
        
        #if(verb): print 'NNN',stmid,sdtgs,'ebdtg:',edtg,bdtg
        for sbt in sbts:
            #print 'sss',sbt
            #for n in range(0,len(sbt)):
                #print n,sbt[n]
            #sys.exit()
            if(doDict):
                (pdtg,psbt)=self.parseSbtDict(sbt)
            else:
                psbt=self.parseSbt(sbt)
                pdtg=psbt[0]
            
            if(doDict and verb == 2):
                kk=psbt.keys()
                kk.sort()
                for k in kk:
                    print 'kkk',k,psbt[k]
            
            stime=dtgdiff(edtg,pdtg)
            if(stime < btime and warn):
                print 'WWW-stime: %d < btime %d for stmid: %s'%(stime,btime,stmid)
            else:
                if(doDict):
                    #if(verb): print 'ddddd-ssseeettt',psbt.values().ks
                    sbtTS[stime]=psbt
                else:
                    #if(verb): print 'ssseeettt',stime,psbt[1:]
                    sbtTS[stime]=psbt[1:]

        if(verb == 2):
            stimes=sbtTS.keys()
            stimes.sort()
            for stime in stimes:
                if(doDict):
                    print 'ooo-ddd',stime,sbtTS[stime].values()
                else:
                    print 'ooo',stime,sbtTS[stime],len(sbtTS[stime])
            
        return(sbtTS)
        
    
    def getSbtTS(self,stmid,verb=0):
        
        """
method to pull variables from sbt to compare dev v non-dev storms
"""
        if(stmid in self.stmsDev):
            sbtType='DEV'
            sbtTS=self.setsbtTS(stmid,sbtType,self.btime,verb=verb)
            
        elif(stmid in self.stmsNon):
            sbtType='NONdev'
            sbtTS=self.setsbtTS(stmid,sbtType,self.btime,verb=verb)
        else:
            sbtTS=None
            sbtType='NN'
            
        return(sbtType,sbtTS)
            
    def makeSbtTSTaxis(self):
        
        taxis=[]
        
        xtimes=range(self.btime,self.etime+1,self.dtime)
        xvals={}
        for n in range(0,len(xtimes)):
            xtime=xtimes[n]*1.0
            taxis.append(xtime)
            xvals[xtime]=undef
            
        self.taxis=taxis
        self.xvalsU=xvals
        
    def makeSbtVarTaxis(self):
        
        taxis=[]
        xvals={}
        for n in range(0,self.maxTimes):
            xtime=n
            taxis.append(xtime)
            xvals[xtime]=undefVar
            
        self.taxis=taxis
        self.xvalsU=xvals
        
        

    def makeSbtTS(self,vvals,nvar,warn=0,verb=0):
        
        ovals=copy.deepcopy(self.xvalsU)
        kk=vvals.keys()
        kk.sort()
        for k in kk:
            if(k < self.btime):
                if(warn): print 'WWW-makeSbtTS time: %d < btime %d'%(k,self.btime)
            else:
                if(verb): print 'kkkk----',k,vvals[k][nvar]
                ovals[k]=vvals[k][nvar]
            
        oo=ovals.keys()
        oo.sort()
        tline=[]
        for o in oo:
            #if(verb): print 'ooo',o,ovals[o]
            tline.append(ovals[o])
            
        rc=tline
        return(rc)

    def makeSbtTSDict(self,vvals,ovar,warn=0,verb=0):
        
        ovals=copy.deepcopy(self.xvalsU)
        kk=vvals.keys()
        kk.sort()
        for k in kk:
            if(k < self.btime):
                if(warn): print 'WWW-makeSbtTS time: %d < btime %d'%(k,self.btime)
            else:
                dovar="'%s'"%(ovar)
                try:
                    ovals[k]=vvals[k][dovar]
                    if(verb): print 'kkkk----',k,vvals[k][dovar]
                except:
                    None
            
        oo=ovals.keys()
        oo.sort()
        tline=[]
        for o in oo:
            if(verb == 2): print 'ooo',o,ovals[o]
            tline.append(ovals[o])
            
        rc=tline
        return(rc)
    
    def makeGaNonDevCtl(self,nx,ny,nvars,verb=0):
            
        ctl="""dset ^%s
title sbt nondev-dev for stmopt: %s
undef %5.1f
xdef %d linear %d %d
ydef %d linear 1 1
zdef 1 levels 1013
tdef 1 linear 12z7sep1953 6hr
vars %d
"""%(self.gadatFile,self.stmopt,undef,
            nx,self.btime,self.dtime,ny,
            len(nvars))
        for nvar in nvars:
            gvar=self.sMv[nvar]
            ctl=ctl+"%s 0 0 %s\n"%(gvar,self.sMdesc[gvar])
            
        ctl=ctl+"endvars"
        MF.WriteCtl(ctl, self.gactlPath,verb=verb)
    
    def makeGaNonDevCtlDict(self,nx,ny,ovars,verb=0):
            
        ctl="""dset ^%s
title sbt nondev-dev for stmopt: %s
undef %5.1f
xdef %d linear %d %d
ydef %d linear 1 1
zdef 1 levels 1013
tdef 1 linear 12z7sep1953 6hr
vars %d
"""%(self.gadatFile,self.stmopt,undef,
            nx,self.btime,self.dtime,ny,
            len(ovars))
        for ovar in ovars:
            mvar="'%s'"%(ovar)
            gvar=ovar
            ctl=ctl+"%s 0 0 %s\n"%(gvar,self.sMdesc[mvar])
            
        ctl=ctl+"endvars"
        MF.WriteCtl(ctl, self.gactlPath,verb=verb)
    
    def makeGaNonVDevTS(self,sbtTS,tsType,nvars,verb=0):
        
        gadir=self.gadatDir
        gadatPath="%s/ts-%s-%s.dat"%(gadir,tsType,self.stmopt)
        gactlPath="%s/ts-%s-%s.ctl"%(gadir,tsType,self.stmopt)
        (gdir,gfile)=os.path.split(gadatPath)
        self.gadatPath=gadatPath
        self.gactlPath=gactlPath
        self.gadatFile=gfile
        

        B=open(gadatPath,'wb')

        nkk=sbtTS.keys()
        nkk.sort()
        tsOut={}
        
        for nvar in nvars:
            
            for nk in nkk:
                print 'NNNNNNNN nvar: ',nk,nvar,self.sMv[nvar]
                nvvals=sbtTS[nk]
                print 'nk:',len(nvvals),nvvals.keys()
                tvals=self.makeSbtTS(nvvals,nvar,verb=0)
                print 'kkkk',nk,len(tvals)
                MF.appendDictList(tsOut,nvar,tvals)
                if(verb): print tsType,nk,self.sMv[nvar],tvals[-13:]
                
            tt=tsOut[nvar]
            ny=len(tt)
            print 'tsType ny',tsType,ny
            nx=len(self.xvalsU)
    
            for t in tt:
                for x in t:
                    b=struct.pack('1f',x)
                    B.write(b)
        
        B.close()
        
        rc=self.makeGaNonDevCtl(nx,ny,nvars)
        
    def makeGaNonVDevTSDict(self,sbtTS,tsType,ovars,verb=0):

        gadir=self.gadatDir
        gadatPath="%s/ts-%s-%s.dat"%(gadir,tsType,self.stmopt)
        gactlPath="%s/ts-%s-%s.ctl"%(gadir,tsType,self.stmopt)
        (gdir,gfile)=os.path.split(gadatPath)
        self.gadatPath=gadatPath
        self.gactlPath=gactlPath
        self.gadatFile=gfile
        

        B=open(gadatPath,'wb')

        nkk=sbtTS.keys()
        nkk.sort()
        tsOut={}
        
        for ovar in ovars:
            
            for nk in nkk:
                if(verb): print 'NNNNNNNN--DDD ovar: ',nk,ovar
                nvvals=sbtTS[nk]
                #print 'nk:',len(nvvals),nvvals.keys()
                tvals=self.makeSbtTSDict(nvvals,ovar,verb=verb)
                #print 'kkkk',nk,len(tvals)
                MF.appendDictList(tsOut,ovar,tvals)
                
            tt=tsOut[ovar]
            ny=len(tt)
            print 'tsType ny',tsType,ny
            nx=len(self.xvalsU)
    
            for t in tt:
                for x in t:
                    b=struct.pack('1f',x)
                    B.write(b)
        
        B.close()
        
        rc=self.makeGaNonDevCtlDict(nx,ny,ovars)

    def setsbtVar(self,stmid,sbtType,doDict=1,doDtgKey=0,warn=0,verb=0):
    
        #smeta=self.stmSum[stmid]

        if(sbtType == 'NONdev'):
            sbts=self.sbtNonDev[stmid]
            sdtgs=self.sbtNonDevdtgs[stmid]

        elif(sbtType == 'DEV'):
            sbts=self.sbtDev[stmid]
            sdtgs=self.sbtDevdtgs[stmid]

        elif(sbtType == 'NN'):
            sbts=self.sbtNN[stmid]
            sdtgs=self.sbtNNdtgs[stmid]

        # -- dict by dtg with (dict form of sBT by varname)
        #
        
        sbtVar={}

        # -- set x axis with values to undefVar
        #
        sdtgs.sort()
        edtg=sdtgs[-1]
        bdtg=sdtgs[0]
        tdtgs=dtgrange(bdtg,edtg,6)
        for n in range(0,len(tdtgs)):
            skey=n
            if(doDtgKey):
                skey=tdtgs[n]
            sbtVar[skey]=undefVar

        for n in range(0,len(sbts)):
         
            skey=n
            if(doDtgKey):
                skey=tdtgs[n]
                
            sbt=sbts[n]
            #print 'nnnnnn',n,sbt,len(sbt)

            if(doDict):
                (pdtg,psbt)=self.parseSbtDict(sbt)
                sbtVar[skey]=psbt
            else:
                psbt=self.parseSbt(sbt)
                pdtg=psbt[0]
                sbtVar[skey]=psbt[1:]
            
            if(doDict and verb == 2):
                kk=psbt.keys()
                kk.sort()
                for k in kk:
                    print 'kkk',k,psbt[k]
            
        if(verb == 2):
            sns=sbtVar.keys()
            sns.sort()
            for sn in sns:
                
                if(doDict):
                    print 'ooo-ddd',sdtg,sbtTS[sn].values()
                else:
                    print 'ooo',sdtg,sbtTS[sn],len(sbtTS[sn])
            
        return(sbtVar)
        

    def getSbtVar(self,stmid,doDict=1,doDtgKey=0,warn=0,verb=0):
        
        """
method to pull variables from sbt to compare dev v non-dev storms
"""
        if(stmid in self.stmsDev):
            sbtType='DEV'
            sbtVar=self.setsbtVar(stmid,sbtType,
                                  doDict=doDict,doDtgKey=doDtgKey,warn=warn,verb=verb)
            
        elif(stmid in self.stmsNon):
            sbtType='NONdev'
            sbtVar=self.setsbtVar(stmid,sbtType,
                                  doDict=doDict,doDtgKey=doDtgKey,warn=warn,verb=verb)
            
        elif(stmid in self.stmsNN):
            sbtType='NN'
            sbtVar=self.setsbtVar(stmid,sbtType,
                                  doDict=doDict,doDtgKey=doDtgKey,warn=warn,verb=verb)

        else:
            sbtVar=None
            sbtType='XXX'
            
        if(sbtVar == None):
            print 'EEEEEEEEEEE: ',stmid
            sys.exit()
        return(sbtType,sbtVar)
    

    def makeGaVarAllDict(self,sbtvarAll,ovars,verb=0):

        gadir=self.gadatDir
        gadatPath="%s/all-bystm-%s.dat"%(gadir,self.stmopt)
        gactlPath="%s/all-bystm-%s.ctl"%(gadir,self.stmopt)
        gadatPathAll="%s/all-all-%s.dat"%(gadir,self.stmopt)
        gactlPathAll="%s/all-all-%s.ctl"%(gadir,self.stmopt)
        (gdir,gfile)=os.path.split(gadatPath)
        (gdir,gfileAll)=os.path.split(gadatPathAll)
        
        self.gadatPath=gadatPath
        self.gactlPath=gactlPath
        self.gadatFile=gfile

        self.gadatPathAll=gadatPathAll
        self.gactlPathAll=gactlPathAll
        self.gadatFileAll=gfileAll

        B=open(gadatPath,'wb')
        A=open(gadatPathAll,'wb')

        nkk=sbtvarAll.keys()
        nkk.sort()
        tsVar={}
        tsVarAll={}
        
        for ovar in ovars:
            
            for nk in nkk:
                if(verb): print 'NNNNNNNN--DDD ovar: ',nk,ovar
                nvvals=sbtvarAll[nk]
                #print 'nk:',len(nvvals),nvvals.keys()
                tvals=self.makeSbtVarDict(nvvals,ovar,verb=verb)
                #print 'kkkk',nk,len(tvals)
                MF.appendDictList(tsVar,ovar,tvals)
                
            tt=tsVar[ovar]
            ny=len(tt)
            #print 'varall ny',ny
            nx=len(self.xvalsU)
    
            for t in tt:
                for x in t:
                    b=struct.pack('1f',x)
                    B.write(b)
        
        B.close()
        
        # -- make the .ctl
        #
        rc=self.makeGaVarAllCtlDict(nx,ny,ovars)
        
        
        # -- all only varies in x
        #

        oNx={}
        for ovar in ovars:
            
            for nk in nkk:
                if(verb): print 'NNNNNNNN--DDD ovar: ',nk,ovar
                nvvals=sbtvarAll[nk]
                #print 'nk:',len(nvvals),nvvals.keys()
                avals=self.makeSbtVarDictAll(nvvals,ovar,verb=verb)
                if(verb): print 'aaa',nk,ovar,len(avals),avals[-10:]
                MF.appendDictList(tsVarAll,ovar,avals)
                
            tt=tsVarAll[ovar]
            #if(verb == 0): print 'varall nk',nk,tt[-10:]
    
            ox=[]
            
            for t in tt:
                for x in t:
                    ox.append(x)
                    b=struct.pack('1f',x)
                    A.write(b)
                
            oNx[ovar]=len(ox)    
                    
        A.close()
        
        nx=oNx[ovars[0]]
        for ovar in ovars[1:]:
            nx1=oNx[ovar]
            if(nx1 != nx):
                print 'oooooooooooooopppppppppppppppppsssssssssssssssssss',ovar,nx,nx1
                
                
        # -- make the .ctl for all file with vars in x only
        #
        rc=self.makeGaVarAllCtlDictAll(nx,ovars)

    def makeSbtVarDict(self,vvals,ovar,warn=0,verb=0):
        
        ovals=copy.deepcopy(self.xvalsU)
        kk=vvals.keys()
        kk.sort()
        for k in kk:
            dovar="'%s'"%(ovar)
            try:
                ovals[k]=vvals[k][dovar]
                if(ovar == 'btccode'):
                    ovals[k]=float(IsTc(ovals[k]))
                if(verb == 2): print 'kkkk----',k,vvals[k][dovar]
            except:
                None
            
        oo=ovals.keys()
        oo.sort()
        tline=[]
        for o in oo:
            if(verb == 2): print 'ooo',o,ovals[o]
            tline.append(ovals[o])
            
        rc=tline
        return(rc)

    def makeSbtVarDictAll(self,vvals,ovar,warn=0,verb=0):
        
        ovals={}
        kk=vvals.keys()
        kk.sort()
        for k in kk:
            dovar="'%s'"%(ovar)
            #print 'kkkk----',k,dovar,vvals[k][dovar]
            try:
                ovals[k]=vvals[k][dovar]
                if(ovar == 'btccode'):
                    ovals[k]=float(IsTc(ovals[k]))
                #lovals=len(ovars[k])
                #print 'gggg',k,ovals[k]
                #print 'kkkk----',k,lovals,ovals[k]
            except:
                #print 'ffff',k
                None
            
        oo=ovals.keys()
        oo.sort()
        tline=[]
        for o in oo:
            #print 'ooo',o,ovals[o]
            tline.append(ovals[o])
            
        rc=tline
        #print 'tttt',tline
        return(rc)

    
    def makeGaVarAllCtlDict(self,nx,ny,ovars,verb=0):
            
        ctl="""dset ^%s
title sbt var by stm for stmopt: %s
undef %5.1f
xdef %d linear 0 1
ydef %d linear 1 1
zdef 1 levels 1013
tdef 1 linear 12z7sep1953 6hr
vars %d
"""%(self.gadatFile,self.stmopt,undefVar,
            nx,ny,
            len(ovars))
        for ovar in ovars:
            mvar="'%s'"%(ovar)
            gvar=ovar
            ctl=ctl+"%s 0 0 %s\n"%(gvar,self.sMdesc[mvar])
            
        ctl=ctl+"endvars"
        MF.WriteCtl(ctl, self.gactlPath,verb=verb)

    def makeGaVarAllCtlDictAll(self,nx,ovars,verb=0):
        
        ctlAll="""dset ^%s
title sbt var by stm for stmopt: %s
undef %5.1f
xdef %d linear 0 1
ydef 1 linear 1 1
zdef 1 levels 1013
tdef 1 linear 12z7sep1953 6hr
vars %d
"""%(self.gadatFileAll,self.stmopt,undefVar,
            nx,
            len(ovars))
        for ovar in ovars:
            mvar="'%s'"%(ovar)
            gvar=ovar
            ctlAll=ctlAll+"%s 0 0 %s\n"%(gvar,self.sMdesc[mvar])
            
        ctlAll=ctlAll+"endvars"
        MF.WriteCtl(ctlAll, self.gactlPathAll,verb=verb)

    def lsGaVarAllDict(self,sbtvarAll,ovars,verb=0):
        # -- all only varies in x
        #
        oNx={}
        nkk=sbtvarAll.keys()
        nkk.sort()
        
        for ovar in ovars:
            
            for nk in nkk:
                if(verb): print 'NNNNNNNN--DDD ovar: ',nk,ovar
                vvals=sbtvarAll[nk]
                kk=vvals.keys()
                kk.sort()
                
                print 'ls of: %s for stmid: %s'%(ovar,nk)
                for k in kk:
                    dovar="'%s'"%(ovar)
                    pval=vvals[k][dovar]
                    if(ovar == 'btccode'):
                        print pval
                        pval=IsTc(pval)
                    print "%s %6.1f"%(k,pval)
                    try:
                        ovals[k]=vvals[k][dovar]
                        #lovals=len(ovars[k])
                        #print 'gggg',k,ovals[k]
                        #print 'kkkk----',k,lovals,ovals[k]
                    except:
                        #print 'ffff',k
                        None
                    
                
        return         
        
        
MF=MFutils()
