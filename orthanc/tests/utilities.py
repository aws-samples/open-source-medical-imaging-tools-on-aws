from os import listdir
from os.path import dirname, isdir, isfile, join, realpath

import pydicom

# -------------------------------------------------------------------------------------------------
# Utility Orthanc routines
# -------------------------------------------------------------------------------------------------

def make_url(url, path, port):
    return f"https://{url}:{port}/{path}"

def get_datadir():
    """Return fully qualified name of data/ directory"""
    thisdir = dirname(realpath(__file__))
    datadir = join(thisdir, 'data')
    return datadir

def get_datadirs():
    """Return fully qualified name of each subdirectory of data/"""
    datadir = get_datadir()
    datadirs = [join(datadir, f) for f in listdir(datadir) if isdir(join(datadir, f))]
    return datadirs

def get_dicomfiles(seriesinstanceuid):
    """Return list of files in data/{seriesinstanceuid}"""
    dicomdir = join(get_datadir(), seriesinstanceuid)
    dicomfiles = [join(dicomdir, f) for f in listdir(dicomdir) if isfile(join(dicomdir, f))]
    return dicomfiles

def get_dicomfiles_details(seriesinstanceuid):
    """Return pydicom dump of first file in corresponding data/ directory"""
    dicom_file = get_dicomfiles(seriesinstanceuid)[0]
    dataset = pydicom.dcmread(dicom_file)
    return dataset
