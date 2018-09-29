import sys,os,subprocess
import glob
import numpy as np
import pandas as pd
from astropy.io import fits

dbfile = 'raw_dataMIKE.db'

slitdirs = {'0.35':'35slit',
            '0.50':'50slit',
            '0.70':'70slit',
            '1.00':'10slit'}

def read_db(dbfile):
    # automatically detect column widths to read
    with open(dbfile,'r') as f:
        h = f.readline()
        sep = f.readline()
        lines = f.readlines()

    columns = ['filename','inst','date','start','mjd','slita','exptime','type','object']
    colspecs = []
    prevloc = 1 #skip the # symbol
    for i,col in enumerate(columns):
        loc = h.find(col)+len(col)
        colspecs.append((prevloc,loc))
        prevloc = loc

    df = pd.read_fwf(dbfile,colspecs=colspecs,skiprows=2,header=None,names=columns)
    assert np.all(df.index-np.arange(len(df))==0)
    return df,h,sep,lines

def make_new_db(uslit,color,df,hline,sepline,lines):
    assert len(lines)==len(df)
    dboutfile = "{0}/{1}/{1}MIKE.db".format(slitdirs[uslit],color)
    with open(dboutfile,'w') as f:
        f.write(hline)
        f.write(sepline)
        for line,(i,row) in zip(lines,df.iterrows()):
            if color in row['inst'].lower() and uslit==row['slit']:
                f.write(line)
            else:
                pass
            

if __name__=="__main__":
    # Read in db file
    df,hline,sepline,lines = read_db(dbfile)
    
    # Read in slits
    slits = [np.nan for x in lines]
    for i,f in df['filename'].iteritems():
        hdu = fits.open(f)
        header = hdu[0].header
        slit = header['SLITSIZE']
        assert slit[4:]=='x5.00'
        slits[i] = slit[0:4]
    unique_slits = list(np.unique(slits))
    for slit in unique_slits: assert slit in slitdirs
    slits = pd.Series(slits)
    assert np.all(slits.index-np.arange(len(slits))==0)
    df['slit'] = slits
    
    calib_count={}
    for i,row in df.iterrows():
        if pd.isnull(row['object']): continue
        obj=row['object'].lower()
        if 'blue' in row['inst'].lower(): continue
        if 'quartz' in obj: obj='quartz'
        elif 'milky' in obj: obj='milky'
        elif 'thar' in obj: obj='thar'
        else: continue
        #print obj,row['slit'],row['exptime']

        key = "{}_{}".format(obj,row['slit'])
        if key in calib_count:
            calib_count[key] += 1
        else:
            calib_count[key] = 1
    print calib_count

    # Make directories
    for uslit in unique_slits:
        reddir = '{0}/red'.format(slitdirs[uslit])
        bluedir = '{0}/blue'.format(slitdirs[uslit])
        subprocess.call('mkdir -p '+reddir,shell=True)
        subprocess.call('mkdir -p '+bluedir,shell=True)

    # Make new files
    for uslit in unique_slits:
        for color in ['red','blue']:
            make_new_db(uslit,color,df,hline,sepline,lines)
