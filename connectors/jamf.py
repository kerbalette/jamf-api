from requests.status_codes import codes

from connectors.connector import Connector

class Jamf(Connector):
    def __init__(self):
        super().__init__()
        self._set_basic_auth(self._config.get_connector_credentials("jamf"))
        self._set_base_url(self._config.get_connector_base_api_url("jamf"))
        self._set_session_headers({"Accept": "application/json"})

    def get_computer_by_serial(self, serial: str = "") -> dict:
        uri = "/computers/serialnumber/{0}".format(serial)

        return self._process_request(uri)

    def get_device_by_serial(self, serial: str = "") -> dict:
        device = self.get_computer_by_serial(serial)
        if device is not None:
            return device
        return self.get_mobile_device_by_serial(serial)

    def get_computer_by_mac_addr(self, mac_addr: str = "") -> dict:
        uri = "/computers/macaddress/{0}".format(mac_addr)

        return self._process_request(uri)

    def get_device_by_mac_addr(self, mac_addr: str = "") -> dict:
        device = self.get_computer_by_mac_addr(mac_addr)
        if device is not None:
            return device
        return self.get_mobile_device_by_mac_addr(mac_addr)

    def _process_request(self, uri: str = "", params: str = ""):
        try:
            response = self._get(uri)
            if response.status_code == codes.ok:
                return response.json()
            elif response.status_code == codes.not_found:
                print("Response({0}) - Resource not found - {1}"
                           .format(response.status_code, uri))
            else:
                print("Invalid response({0}) returned from the API - {1}"
                                .format(response.status_code, uri))
            return None
        except ValueError:
            print("Error has occurred")
