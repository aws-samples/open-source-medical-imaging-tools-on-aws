import pytest
import logging
logging.basicConfig(level=logging.WARNING)

def pytest_addoption(parser):
    parser.addoption("--url"              , action = "store", default = "", help = "URL to test, in format 'some.address.com")
    parser.addoption("--port"             , action = "store", default = "", help = "Port number")
    parser.addoption("--user"             , action = "store", default = "", help = "User")
    parser.addoption("--password"         , action = "store", default = "", help = "Password")
    parser.addoption("--seriesinstanceuid", action = "store", default = "", help = "Series Instance UID")
    parser.addoption("--loglevel"         , action = "store", default = "", help = "Log level DEBUG INFO WARNING ERROR CRITICAL")

def pytest_generate_tests(metafunc):
    # This is called for every test. Only get/set command line arguments
    # if the argument is specified in the list of test "fixturenames".
    option_value = metafunc.config.option.url
    if 'url' in metafunc.fixturenames and option_value is not None:
        metafunc.parametrize("url", [option_value])
    option_value = metafunc.config.option.user
    if 'user' in metafunc.fixturenames and option_value is not None:
        metafunc.parametrize("user", [option_value])
    option_value = metafunc.config.option.password
    if 'password' in metafunc.fixturenames and option_value is not None:
        metafunc.parametrize("password", [option_value])
    option_value = metafunc.config.option.port
    if 'port' in metafunc.fixturenames and option_value is not None:
        metafunc.parametrize("port", [option_value])
    option_value = metafunc.config.option.seriesinstanceuid
    if 'seriesinstanceuid' in metafunc.fixturenames and option_value is not None:
        metafunc.parametrize("seriesinstanceuid", [option_value])
