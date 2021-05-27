import requests
import pydicom

import test_data
import dicomweb_test
import rest_test
import utilities

# -------------------------------------------------------------------------------------------------
# Tests
# -------------------------------------------------------------------------------------------------

def test_dicomweb_login(url, port, user, password, seriesinstanceuid):
    assert     dicomweb_test.test_login(url, port, user, password)
    assert not dicomweb_test.test_login(url, port, '', '')

def test_dicomweb_upload(url, port, user, password, seriesinstanceuid):
    series_exists = rest_test.series_exists(url, port, user, password, seriesinstanceuid)
    if series_exists:
        rest_test.delete_series_rest(url, port, user, password, seriesinstanceuid)
        assert not rest_test.series_exists(url, port, user, password, seriesinstanceuid)
    assert dicomweb_test.do_test_upload(url, port, user, password, seriesinstanceuid)
    dicomweb_client = dicomweb_test.make_client(url, port, user, password)
    assert dicomweb_test.series_exists(dicomweb_client, seriesinstanceuid)