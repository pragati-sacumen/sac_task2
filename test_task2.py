"""Test file for task2.py"""
import pytest
import warnings
from sac_requests.constants.general import HTTPS, BEARER_TOKEN
from sac_requests.context.config import HttpConfig
from sac_requests.context.headers import HttpHeaders
from sac_requests.context.request import HttpRequest
from sac_requests.context.url import HttpURL
from sac_log.logger import get_logger
from sac_log.utils import get_configurations
from task2 import get_method

""" Dummy inputs."""
dummy_token = HttpHeaders({
    "Authorization" : "Bearer token"
})
dummy_url = HttpURL(host="slack.com/api/",protocol=HTTPS)
dummy_conf = HttpConfig()

dummy_input = HttpRequest(headers=dummy_token, url=dummy_url, auth_type=BEARER_TOKEN,config = dummy_conf)

config = get_configurations('log_folder2/config.cfg')
log_it = get_logger('TEST',config["TEST"])

@pytest.mark.vcr()
def test_get_method():
    """check the status code"""
    result = get_method(dummy_input, "users.list", "members", log_it, 2)
    assert result.status_code == 200, log_it.info("test_get_method(): Failed ")

def test_url_get_method():
    """testcase for wrong url"""
    with pytest.raises(ConnectionError):
        result = get_method(dummy_input, "wrong_url", "members", log_it, 2)
        
@pytest.mark.vcr()
def test_limit_get_method():
    """check the status code"""
    result = get_method(dummy_input, "users.list", "members", log_it, -1)
    assert result.json()["members"] == [], log_it.info("test_get_method(): Failed ")
    
@pytest.mark.vcr()
def test_token_get_method():
    """check the status code"""
    result = get_method(dummy_input, "users.list", "members", log_it, 2)
    assert result.json()["ok"] == False, log_it.info("test_get_method(): Failed ")
 
@pytest.mark.vcr()
def test_fetch_vcr():
   """testing fetch method using vcr """
   response = get_method(dummy_input, "users.list", "members", log_it, 2)
   assert response.status_code == 200
