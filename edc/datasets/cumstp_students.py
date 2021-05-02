from ..utils import get_airtable, get_file
import keyring
import numpy as np
import pandas as pd
import os

DEFAULT_CACHE_DIR = os.path.join(os.path.expanduser('~'), 'data')

def _fetch():
    base_id = keyring.get_password('airtable','CUMSTP_BASE_ID')
    api_key = keyring.get_password('airtable','CUMSTP_API_KEY')

    return get_airtable(base_id,'Current Students',api_key)
    


def load_data(from_airtable=False):
    if from_airtable:
        recs = _fetch()
        return pd.DataFrame([r['fields'] for r in recs])
    else:
        fname = 'cumstp_students.csv'
        fpath = get_file(
            fname,
            origin='https://www.elijahc.net/files/{}'.format(fname),
            cache_dir=DEFAULT_CACHE_DIR,
            dset_name='cumstp'
        )
        return pd.read_csv(fpath)
