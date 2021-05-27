from os import listdir
from os.path import dirname, isdir, isfile, join, realpath
import hashlib

import logging
import requests
import utilities

def make_orthanc_id(vals):
    """Return Orthanc ID of Patient, Study, or Series
    https://book.orthanc-server.com/faq/orthanc-ids.html#orthanc-ids
    Format: SHA-1 hash of (PatientID|StudyInstanceUID|SeriesInstanceUID)
    """
    str = '|'.join(vals)
    hh = hashlib.sha1(str.encode('utf-8')).hexdigest()
    sha1 = '-'.join([hh[n * 8:(n + 1) * 8] for n in range(0, 5)])
    return sha1

def make_orthanc_patient_id(seriesinstanceuid):
    dcm = utilities.get_dicomfiles_details(seriesinstanceuid)
    patient_id = make_orthanc_id([dcm.PatientID])
    return patient_id

def make_orthanc_study_id(seriesinstanceuid):
    dcm = utilities.get_dicomfiles_details(seriesinstanceuid)
    study_id = make_orthanc_id([dcm.PatientID, dcm.StudyInstanceUID])
    return study_id

def make_orthanc_series_id(seriesinstanceuid):
    dcm = utilities.get_dicomfiles_details(seriesinstanceuid)
    series_id = make_orthanc_id([dcm.PatientID, dcm.StudyInstanceUID, seriesinstanceuid])
    return series_id

def series_exists(url, port, user, password, seriesinstanceuid):
    series_id = make_orthanc_series_id(seriesinstanceuid)
    full_url = utilities.make_url(url, f"series/{series_id}", port)
    logging.info(f"rest_test::series_exists: {full_url}")
    auth = (user, password)
    r = requests.get(full_url, auth = auth)
    series_exists = (r.status_code == 200)
    logging.info(f"series_exists({seriesinstanceuid}) returning {series_exists}")
    return series_exists


def delete_series_rest(url, port, user, password, seriesinstanceuid):
    """Delete given series using Orthanc REST API
    The DICOMWeb plugin does not always support DELETE https://book.orthanc-server.com/plugins/dicomweb.html#id7
    """
    series_id = make_orthanc_series_id(seriesinstanceuid)
    full_url = utilities.make_url(url, f"series/{series_id}", port)
    auth = (user, password)
    r = requests.delete(full_url, auth = auth)
    logging.info(f"delete_series_rest({seriesinstanceuid}) returned {r.status_code}")
