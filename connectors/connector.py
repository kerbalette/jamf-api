import requests
from requests.exceptions import SSLError, HTTPError, ConnectionError, RequestException
from base import Base

class Connector(Base):
    _session = None
    _base_url = ""

    def __init__(self, base_url: str = ""):
        super().__init__()
        self._session = requests.Session()
        self._base_url = base_url

    def _get(self, uri: str = "", params: dict = {}, headers: dict = {},
            auth = None):
      
        url = self._base_url + uri
        try:
            response = self._session.get(url, params = params, \
                                         headers = headers, auth = auth, \
                                         verify = False)
        except (SSLError, HTTPError, ConnectionError, RequestException):
            print("Error occurred when attempting to connect "
                                "to '{0}'".format(url))
        return response

    def _post(self, uri: str = "", data: dict = {}, headers: dict = {},
              auth = None):

        url = self._base_url + uri
        try:
            response = self._session.get(url, data = data, \
                                         headers = headers, auth = auth, \
                                         verify = False)
        except (SSLError, HTTPError, ConnectionError, RequestException):
            print("Error occurred when attempting to connect "
                                "to '{0}'".format(url))
        return response

    def _set_basic_auth(self, credentials: tuple):
        self._session.auth = credentials

    def _set_session_headers(self, headers = None):
        self._session.headers.update(headers)

    def _set_base_url(self, base_url: str = ""):
        if not isinstance(base_url, str):
            base_url = str(base_url)
        self._base_url = base_url
