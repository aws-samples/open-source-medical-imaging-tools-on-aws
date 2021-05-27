# DICOMWeb test routines for test_orthanc_rest_api.py

import logging
import pydicom
import requests
from requests.auth import HTTPBasicAuth
from progress.bar import Bar


import utilities

from dicomweb_client.api import DICOMwebClient
from dicomweb_client.session_utils import create_session_from_auth

def make_client(url, port, user, password):
    auth = HTTPBasicAuth(user, password)
    session = create_session_from_auth(auth)
    full_url = utilities.make_url(url, 'dicom-web', port)
    client = DICOMwebClient(url = full_url, session = session)
    return client

def test_login(url, port, user, password):
    full_url = utilities.make_url(url, '', port)
    auth = (user, password)
    # Log in
    r = requests.get(full_url, auth = auth)
    return r.status_code == 200

def test_dicomweb(url, port, user, password):
    client = make_client(url, port, user, password)
    seriesinstanceuid = test_data.datasets[test_data.tcia_mri][0][0]
    test_data.ensure_test_data(seriesinstanceuid)
    if series_exists(client, seriesinstanceuid):
        logging.info(f"Series exists")
    else:
        logging.info(f"Series does not exist")

def test_upload(url, port, user, password):
    client = make_client(url, port, user, password)
    seriesinstanceuid = test_data.datasets[test_data.tcia_mri][0][0]
    test_data.ensure_test_data(seriesinstanceuid)
    do_test_upload(url, port, user, password, seriesinstanceuid)

def test_load_test(url, port, user, password):
    client = make_client(url, port, user, password)
    seriesinstanceuid = test_data.datasets[test_data.tcia_mri][0][0]
    test_data.ensure_test_data(seriesinstanceuid)
    for i in range(0, 10):
        do_test_upload(url, port, user, password, seriesinstanceuid)

def do_test_upload(url, port, user, password, seriesinstanceuid):
    client = make_client(url, port, user, password)
    # Delete test series if it already exists
    if series_exists(client, seriesinstanceuid):
        delete_series_rest(url, port, user, password, seriesinstanceuid)
        assert not series_exists(client, seriesinstanceuid)
    # Upload test series and check its correctness
    do_test_stow(client, seriesinstanceuid)
    return series_exists(client, seriesinstanceuid)

def series_exists(client, seriesinstanceuid):
    """Return true if the given series exists on the server.
    Queries the server for the series, and each instance in the series.
    Compares each instance in the series with its file in the data/ directory"""
    series_exists = False
    all_series = client.search_for_series(search_filters={'SeriesInstanceUID': seriesinstanceuid})
    if len(all_series) == 1:
        dicomfiles_details = utilities.get_dicomfiles_details(seriesinstanceuid)
        all_instances_server = client.search_for_instances(
            study_instance_uid = dicomfiles_details.StudyInstanceUID,
            series_instance_uid = seriesinstanceuid
            )
        all_instances_local = utilities.get_dicomfiles(seriesinstanceuid)
        if len(all_instances_server) == len(all_instances_local):
            series_exists = True
    logging.info(f"series_exists({seriesinstanceuid}) returning {series_exists}")
    return series_exists

def test_stow(url, port, user, password):
    """STOW-RS operations on every directory located under data/"""
    client = make_client(url, port, user, password)
    for dicomdir in utilities.get_datadirs():
        do_test_stow(client, dicomdir)

def do_test_stow(client, dicomdir):
    """STOW-RS operations on every DICOM file in a directory"""
    # logging.info(f"do_test_stow({dicomdir})")
    dicomfiles = utilities.get_dicomfiles(dicomdir)
    bar = Bar('Uploading DICOM files', max = len(dicomfiles))
    for dicomfile in dicomfiles:
        dataset = pydicom.dcmread(dicomfile)
        client.store_instances(datasets=[dataset])
        bar.next()
    bar.finish()
