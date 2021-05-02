import os
import urllib.request
import wget

import zipfile
import tarfile

# Functions adapted from keras data_utils
# https://github.com/keras-team/keras/blob/master/keras/utils/data_utils.py

def _extract_archive(file_path, path='.', archive_format='auto' ):
    """Extracts an archive if it matches tar, tar.gz, tar.bz, or zip formats.
    # Arguments
        file_path: path to the archive file
        path: path to extract the archive file
        archive_format: Archive format to try for extracting the file.
            Options are 'tar', 'zip', and None.
            'tar' includes tar, tar.gz, and tar.bz files.
            None or an empty list will return no matches found.
    # Returns
        True if a match was found and an archive extraction was completed,
        False otherwise.
    """
    fmts = ['zip','tar']
    if archive_format is None:
        return False

    if archive_format is not 'auto':
        fmts = [archive_format]

    for archive_type in fmts:
        if archive_type is 'tar':
            open_fn = tarfile.open
            is_match_fn = tarfile.is_tarfile
        if archive_type is 'zip':
            open_fn = zipfile.ZipFile
            is_match_fn = zipfile.is_zipfile

        if is_match_fn(file_path):
            with open_fn(file_path) as archive:
                try:
                    archive.extractall(path)
                except (tarfile.TarError, RuntimeError,
                        KeyboardInterrupt):
                    if os.path.exists(path):
                        if os.path.isfile(path):
                            os.remove(path)
                        else:
                            shutil.rmtree(path)
                    raise
            return True
    return False

def get_file(fname,
             dset_name,
             origin,
             extract=False,
             archive_format=None,
             cache_dir=None):

    """Downloads a file from a URL if it not already in the cache.
    # Arguments
    fname: Name of the file. If an absolute path `/path/to/file.txt` is
        specified the file will be saved at that location.
    dset_name: Dataset name e.g. mnist
    origin: Original URL of the file.
    extract: True tries extracting the file as an Archive, like tar or zip.
    cache_dir: Location to store cached files, when None it
        defaults to the [~/.datasets/<dset_name> Directory]
    # Returns
        Path to the downloaded file
    """

    if cache_dir is None:
        cache_dir = os.path.join(os.path.expanduser('~'), '.datasets')
    datadir_base = os.path.expanduser(cache_dir)
    if not os.access(datadir_base, os.W_OK):
        datadir_base = os.path.join('/tmp', '.datasets')
    if not os.path.exists(datadir_base):
        os.makedirs(datadir_base)

    datadir = os.path.join(datadir_base,dset_name)
    if not os.path.exists(datadir):
        os.makedirs(datadir)

    fpath = os.path.join(datadir, fname)

    download = False
    if not os.path.exists(fpath):
        download = True

    if download:
        print('Downloading data from', origin)
        wget.download(url=origin,out=fpath)

    if extract & (archive_format in ['zip','tar']):
        _extract_archive(fpath,datadir,archive_format)

    return fpath
