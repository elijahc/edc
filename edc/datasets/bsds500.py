"""BSDS500 dataset.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import gzip
import tarfile
import os

import numpy as np
import imageio

from ..utils import get_file

DEFAULT_CACHE_DIR = os.path.join(os.path.expanduser('~'), 'data')

def load_data():

    """Loads the Fashion-MNIST dataset.

    # Returns
            Tuple of Numpy arrays: `(train, test)`.
    """

    base = 'http://www.eecs.berkeley.edu/Research/Projects/CS/vision/grouping/BSR/'
    fname = 'BSR_bsds500.tgz'

    path = get_file(fname,
                    origin = base + fname,
                    cache_dir = DEFAULT_CACHE_DIR,
                    dset_name = 'bsds500')

    f = tarfile.open(path)

    train_data = []
    test_data = []
    for name in f.getnames():
        if name.startswith('BSR/BSDS500/data/images/train/'):
            try:
                fp = f.extractfile(name)
                img = imageio.imread(fp)
                train_data.append(img)
            except:
                continue
        elif name.startswith('BSR/BSDS500/data/images/test/'):
            try:
                fp = f.extractfile(name)
                img = skimage.io.imread(fp)
                test_data.append(img)
            except:
                continue


    return (train_data, test_data)
