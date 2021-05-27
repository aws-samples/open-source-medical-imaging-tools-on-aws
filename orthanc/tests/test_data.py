import os, sys
import zipfile


# TCIA REST API: https://wiki.cancerimagingarchive.net/display/Public/TCIA+REST+API+Guide

# Datasets: SeriesInstanceUID, Size (MB), count
tcia_lung = 'Lung Phantom'
tcia_mri = 'RIDER Phantom MRI'
tcia_pancreas = 'PDMR-292921-168-R'
datasets = {
    tcia_pancreas : [
        ['2.25.261125208346081067001561416436112649326', 22, 36],
        ['2.25.78405646070613891644155235998027765296',  22, 36],
        ['2.25.201714014262473862029353876514171609613', 22, 36],
        ['2.25.242361664646590607061996344922936492489', 22, 36]
    ],
    tcia_lung : [
        ['1.2.840.113619.2.55.3.1930041893.617.1308206442.326.4', 127, 237]
    ],
    tcia_mri : [
        ['1.2.840.113619.2.176.3596.3311940.6866.1220205031.849',  37,  70],
        ['1.2.840.113619.2.176.3596.3311940.6866.1220205031.850', 240, 450]
    ]
}

import jq
import requests

tcia_url = 'https://services.cancerimagingarchive.net/services/v4'
# Collection name from https://wiki.cancerimagingarchive.net/display/Public/Wiki or /TCIA/query/getCollectionValues

def do_get(query_str):
    url = f"{tcia_url}/TCIA/query/{query_str}"
    r = requests.get(url)
    assert r.status_code == 200
    return r.json()

def ensure_test_directory(datadir):
    """Ensure that given directory exists, creating it if necessary.
    Return the total size of the directory.
    """
    (dirsize, dircount) = (0, 0)
    if os.path.isdir(datadir):
        sizes = [d.stat().st_size for d in os.scandir(datadir) if d.is_file() and '.dcm' in d.name]
        dirsize = sum(sizes)
        dircount = len(sizes)
        # print(f"{dirsize} bytes in {dircount} files in existing data directory {datadir}")
    else:
        print(f"ensure_test_directory({datadir}): Creating directory")
        os.makedirs(datadir)
    return (dirsize, dircount)

def download_test_data(datadir, seriesinstanceuid):
    url = f"{tcia_url}/TCIA/query/getImage?SeriesInstanceUID={seriesinstanceuid}"
    print(f"download_test_data({url})")
    r = requests.get(url, allow_redirects=True)
    assert r.status_code == 200
    zip_file = f"{datadir}/{seriesinstanceuid}.zip"
    open(zip_file, 'wb').write(r.content)
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        # print(f"Extracting {len(zip_ref.namelist()) - 1} files into {datadir}")
        zip_ref.extractall(datadir)
    os.remove(zip_file)

def ensure_test_data(uid):
    """Ensure that the test dataset exists in directory named after uid.
    Check uid-named directory and if necessary, download data set into it.
    """
    # Get existing size and count
    thisdir = os.path.dirname(os.path.realpath(__file__))
    datadir = os.path.join(thisdir, 'data', uid)
    (datasize, datacount) = ensure_test_directory(datadir)
    # Get expected size and count
    series_size_j = do_get(f"getSeriesSize?SeriesInstanceUID={uid}")
    expected_size = int(float(jq.compile('.[] | .TotalSizeInBytes').input(series_size_j).first()))
    expected_count = jq.compile('.[] | .ObjectCount').input(series_size_j).first()

    if datasize == expected_size and datacount == expected_count:
        print(f"ensure_test_data({uid}): Data set already exists")
    else:
        # print(f"expected count {expected_count}, size {expected_size}, existing count {datacount}, size {datasize}")
        print(f"ensure_test_data({uid}): Downloading")
        download_test_data(datadir, uid)
    exit

# seriesinstanceuid = datasets[tcia_mri][0][0]
# ensure_test_data(seriesinstanceuid)
# exit
