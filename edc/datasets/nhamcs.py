"""NHAMCS Dataset
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
from ftplib import FTP

import numpy as np
import pandas as pd
import glob
from tqdm import tqdm
import pyreadstat

from ..utils import get_file

from .nchs import DEFAULT_COLS,_remote_ls,PUB_DIR

NHAMCS_DIR = '/'.join([PUB_DIR,'dataset_documentation','nhamcs'])

HOSP_INFO = ['MSA','OWNER','HOSPCODE']

DEFAULT_CACHE_DIR = os.path.join(os.path.expanduser('~'), 'data')

ED_SPSS = [
    'ED2017-spss.zip',
    'ed2016-spss.zip',
    'ed2015-spss.zip',
    'ed2014-spss.zip',
    'ed2013-spss.zip',
    'ed2011-spss.zip',
    'ed2010-spss.zip',
]

OPD_SPSS = [
    'opd2011-spss.zip',
    'opd2010-spss.zip',
]

SPSS_FILES = ED_SPSS

def _remote_spss():
    spss_data_dir = '/'.join([NHAMCS_DIR,'spss'])
    files = _remote_ls(path=spss_data_dir)
    dat_files = [f for f in files if f.endswith('spss.zip') and 'chc' not in f]
    return dat_files

def _cache_spss_sav(files=SPSS_FILES):
    base = 'ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/dataset_documentation/nhamcs/spss/'

    # with FTP('ftp.cdc.gov') as ftp:
    #     ftp.login()
    #     ftp.cwd('pub/Health_Statistics/NCHS/dataset_documentation/nhamcs/spss/')
    #     contents = []
    #     ftp.dir(contents.append
    fpaths = []
    for fname in files:
        path = get_file(fname.lower(),
                        origin = base + fname,
                        cache_dir = DEFAULT_CACHE_DIR,
                        extract=True,
                        dset_name = 'nhamcs')
        fpaths.append(path)

    return fpaths

def _load_spss(spss_files,usecols=None):
    usecols = usecols or DEFAULT_COLS

    pbar = tqdm(sorted(spss_files))
    for fp in pbar:
        pbar.set_description(os.path.split(fp)[-1])
        yield pd.read_spss(fp,usecols=usecols)

def load_opd(cached_files):
    # sav_files = glob.glob(os.path.join(base,'nhamcs','*.sav'))
    sav_files = [f.split('.zip')[0]+'.sav' for f in cached_files]
    load_fps = [os.path.join(DEFAULT_CACHE_DIR,'nhamcs',f) for f in sav_files]

    addl_cols = ['CLINTYPE','ADMITHOS','REFERED','OTHDISP']
    dataset = pd.concat(_load_spss(load_fps,usecols=DEFAULT_COLS+addl_cols),sort=False)
    # dataset.AGE = dataset.AGE.astype(np.uint64)

    return dataset

def load_ed(cached_files):
    """Loads the NHAMCS ED dataset.

    Arguments
        year: None, int, or list

    # Returns
            Pandas Dataframe
    """
    # sav_files = glob.glob(os.path.join(base,'nhamcs','*.sav'))
    sav_files = [f.split('.zip')[0]+'.sav' for f in cached_files]
    load_fps = [os.path.join(DEFAULT_CACHE_DIR,'nhamcs',f) for f in sav_files]

    ed_cols = ['ADMIT','ADMITHOS','ADMITOBS','LOS','HDSTAT']

    dataset = pd.concat(_load_spss(load_fps,DEFAULT_COLS+ed_cols),sort=False)
    dataset['SPECCAT'] = 'Emergency Medicine'
    dataset.AGEDAYS = dataset.AGEDAYS.replace({'Less than 1 day':0.5})
    def convert_age(r):
        if r.AGE == 'Under one year':
            r.AGE = int(r.AGEDAYS)/365.0
        
        return r
    dataset = dataset.transform(convert_age,axis=1)
    # dataset.AGE = dataset.AGE.astype(np.uint64)

    return dataset

class NHAMCS(object):
    def __init__(self, spss_files, read_func):
        self.SPSS_FILES = spss_files
        self._read_data = read_func

    def load_data(self, year=None, usecols=None):
        """Loads the NHAMCS datasets filterable by year.

        Arguments
            year: None, int, or list

        # Returns
                Pandas Dataframe
        """
        is_in_year = lambda f: True in [str(y) in f for y in year]
        if isinstance(year,int):
            year = [year]

        if year is None:
            # Just load latest year
            sel_files = [self.SPSS_FILES[0]]
        elif isinstance(year,(list,np.ndarray)):
            sel_files = filter(is_in_year,OPD_SPSS)

        cached_files = _cache_spss_sav(sel_files)
        return self._read_data(cached_files)

ed = NHAMCS(spss_files = ED_SPSS, read_func=load_ed)
opd = NHAMCS(spss_files = OPD_SPSS, read_func=load_opd)


