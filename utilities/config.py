import os
import sys
import yaml

class Config(object):
    _instance = None

    _NAME = "name"
    _CONNECTORS = "connectors"
    _PROPERTIES = "properties"

    def __init__(self, path: str = ""):
        if Config._instance is not None:
            print("Only a single instance of this class is permitted.")
            sys.exit(1)
        else:
            Config._instance = self

        try:
            self._data = self._parse_configuration(path)
        except OSError:
            print("Configuration file not found. Terminating.")
            sys.exit(1)
        except yaml.YAMLError:
            print("An error occurred while parsing YAML configuration. "
                  "Terminating.")
            sys.exit(1)

    @staticmethod
    def get_instance(path: str = ""):
        if Config._instance is None:
            return Config(path)
        else:
            return Config._instance

    def get_connector_credentials(self, name: str = "") -> tuple:
        m_attrs = ["username", "password"]
        properties = {key: str(value) for (key, value) in
                      self.get_connector_properties(name).items()}

        if not all(val in properties.keys() for val in m_attrs):
            raise KeyError("Mandatory attributes '{}' not present in "
                           "connector properties.".format(str(m_attrs)))
        return properties.get("username"), properties.get("password")

    def get_connector_base_api_url(self, name: str = "") -> str:
        try:
            """
            Fetch the connector properties and enforce type conversion on values so we
            can properly build the base URL through trivial string
            concatenation.  """
            m_attrs = ["protocol", "hostname", "port", "api_base_uri"]
            properties = self.get_connector_properties(name)
            properties = {key: str(value) for (key, value) in
                          properties.items()}

            if not all(val in properties.keys() for val in m_attrs):
                raise KeyError("Manadatory attributes '{}' not present in "
                               "JSON connector properties."
                               .format(str(m_attrs)))
                sys.exit(1)

            protocol = properties.get("protocol")
            hostname = properties.get("hostname")
            port = properties.get("port")
            api_base_uri = properties.get("api_base_uri")
            return protocol + "://" + hostname + ":" + port + "/" + api_base_uri
        except AttributeError:
            print("Error occurred when attempting to build base "
                  "URL for connector.")
            return None
        return None

    def get_connector_property(self, name: str = "", property: str = "") -> str:
        try:
            return str(self.get_connector_properties(name).get(property))
        except AttributeError:
            print("Property for this connector not found.")
            return None

    def get_connector_properties(self, name: str = "") -> dict:
        connector = self.get_connector(name)
        if connector is None:
            print("Error. Could not find connector with the name '%s'." % name)
            return None

        if self._PROPERTIES not in connector:
            raise AttributeError("Connector '%s' does not contain attribute '%s'. Terminating."
                                 % (name, self._PROPERTIES))
        return connector.get(self._PROPERTIES)

    def get_connector(self, name: str = "") -> dict:
        for connector in self.get_connectors():
            if connector.get(self._NAME) == name:
                return connector
        return None

    def get_connectors(self) -> list:
        return self._get_root_object(self._CONNECTORS)

    def _get_root_object(self, object: str = ""):
        return self._data.get(object)

    def _parse_configuration(self, path: str = "") -> dict:
        if not os.path.isfile(path):
            raise OSError
        with open(path) as file:
            return yaml.safe_load(file)
