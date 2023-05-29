
"""TASK 3 PYTHON FILE"""
from sac_log.logger import get_logger
from sac_log.utils import get_configurations
from sac_requests.constants.general import HTTPS, BEARER_TOKEN
from sac_requests.context.config import HttpConfig
from sac_requests.context.headers import HttpHeaders
from sac_requests.context.request import HttpRequest
from sac_requests.context.url import HttpURL

"""Configuration for logging the fetched data."""
config = get_configurations('config1.cfg')
"""config : passes the filename of the configuration file to get_configuration()."""
user_logger = get_logger('TEST_SAC', config["TEST"])
group_logger = get_logger('TEST2_SAC', config["TEST2"])
"""logger : passes the name of the logger and name of the configuration dict to the get_logger()."""

"""Setting up the get request."""
http_config = HttpConfig()
"""HttpConfig() : keeps the settings related to request."""
http_url = HttpURL(host="slack.com/api/",protocol=HTTPS)
"""HttpURL : takes the hostname, protocol."""
headers = HttpHeaders({
    "Authorization" : "Bearer xoxp-2866334873382-2873046169155-2925981877831-8d152cd4d5cd8c2310a3b4aa2b3336f1"
})
"""passing token for accessing the endpoint."""
http_request = HttpRequest(headers=headers, url=http_url, auth_type=BEARER_TOKEN,config = http_config)

def get_method(h:str, endpoint:str, meta_data:str, logger: str, limit:int):
    response = h.get(endpoint=endpoint, params={"limit":limit})
    if __name__ == 'main':
        if response.json()["ok"] is True and response.status_code == 200:
           cursor = response.json()["response_metadata"]["next_cursor"]
           while cursor != "":
                for i in range(limit):
                    logger.info(f"{response.json()[meta_data][i]['id']}")
                logger.info({len(response.json()[meta_data])})
                try:
                    response = http_request.get(endpoint=endpoint, params={"limit":limit,       "cursor":cursor})
                    cursor = response.json()["response_metadata"]["next_cursor"]
                except:
                    logger.error(f"{response.json()['error']}")
        else:
             logger.error(f"{response.json()['error']}")
    else :
        logger.info("Test_successfull")
    return response

# get_method(http_request, "users.list", "members",user_logger,2)
# get_method(http_request, "conversations.list", "channels",group_logger,2)

