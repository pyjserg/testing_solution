import json

import requests


class RESTRequestLibrary(object):
    """
    A test library providing keywords for GET and POST-request operations.

    ``RESTRequestLibrary`` is Robot Framework's custom library that provides a
    set of keywords for requesting data from a specified resource, sending data
    to a server to create/update a resource.

    The library contains following keywords:

    | = Keyword Name =                              | = Comment = |
    | `Make Connection`                             | creates a connection for further using via Get/Post requests
    | `Delete Connection`                           | removes a specific connection from the storage
    | `Delete All Connections`                      | removes all connections from the storage
    | `Get  Request`                                | GET-method implementation
    | `Post Request`                                | POST-method implementation
    | `Check If Response Contains Service `         | Checking the POST-request JSON answer if it contains a service

    """

    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'

    headers: dict = {}
    server_url: str = ''
    connections: dict = {}

    def __init__(self, server_url: str = None, headers: dict = None):
        self.server_url = server_url
        self.headers = headers if headers else {'Content-Type': 'application/json'}

    @staticmethod
    def _get_connection(alias: str):
        """
        The method returns an RESTRequestLibrary instance stored in connections dictionary,
        :param alias: str, according to RESTRequestLibrary.connections key
        :return: RESTRequestLibrary instance
        """
        if alias not in RESTRequestLibrary.connections:
            raise AttributeError(f"Can't find connection named {alias}")
        return RESTRequestLibrary.connections.get(alias)

    @staticmethod
    def make_connection(alias: str, server_url: str, headers: dict = None):
        """
        The method creates a 'connection' - a class instance under the alias alias key in
        RESTRequestLibrary.connections dictionary which contains server url and headers.

         Example:
        | ${headers} = | Create Dictionary | Content-Type=application/json
        | Post request | google | http://google.com | ${headers}

        or can be used without headers attribute (headers {'Content-Type': 'application/json'} provided by default):
        | Post request | google | http://google.com

        :param alias: str
        :param server_url: str, the server name including 'http(s)://'
        :param headers: dict
        :return: RESTRequestLibrary instance
        """
        if alias not in RESTRequestLibrary.connections.keys():
            RESTRequestLibrary.connections[alias] = RESTRequestLibrary(server_url, headers)
        return RESTRequestLibrary.connections[alias]

    @staticmethod
    def delete_connection(alias: str):
        """
        The method deletes connection named 'alias' from RESTRequestLibrary.connections dictionary if it exists.
        Rises LookupError otherwise.

         Example:
        | Delete connection | ${connection_alias}

        :param alias: str, according to RESTRequestLibrary.connections key
        :return: None
        """
        if alias in RESTRequestLibrary.connections.keys():
            del RESTRequestLibrary.connections[alias]
        else:
            raise LookupError(f"There is no connection with alias {alias}")

    @staticmethod
    def delete_all_connections():
        """
        The method reinitializes RESTRequestLibrary.connections with empty dictionary.
        :return: None
        """
        RESTRequestLibrary.connections = {}

    def post_request(self, alias: str, url_tail: str, data: dict, headers: dict = None) -> requests.models.Response:
        """
        POST-method implementation. Uses server URL and headers (by default) stored in connection named 'alias'
        so url_tail shouldn't contain server URL.

         Example:
        | ${headers} = | Create Dictionary | Content-Type=application/json
        | ${data_dictionary} = | Create Dictionary | service_id=1
        | Post request | google | /some_service | ${data_dictionary} | ${headers}

         or can be used without headers attribute if it had been provided in `Make connection` keyword:
        | Post request | google | /some_service | ${data_dictionary}

        :param alias: str, according to RESTRequestLibrary.connections key
        :param url_tail: str
        :param data: dict
        :param headers: dict
        :return: requests.models.Response instance
        """
        connection = self._get_connection(alias)
        url = connection.server_url + url_tail

        if not headers:
            headers = connection.headers

        try:
            response = requests.api.post(url=url, data=json.dumps(data), headers=headers)
        except requests.exceptions.ConnectionError:
            raise AssertionError(f"Can't connect to the URL: {url}. Connection error occurred.")
        return response

    def get_request(self, alias: str, url_tail, headers: dict = None) -> requests.models.Response:
        """
        GET-method implementation. Uses server URL and headers (by default) stored in connection named 'alias'
        so url_tail shouldn't contain server URL.

         Example:
        | ${headers} = | Create Dictionary | Content-Type=application/json
        | Get request | google | /some_service | ${headers}

         or can be used without headers attribute if it had been provided in `Make connection` keyword:
        | Get request | google | /some_service

        :param alias: str, according to RESTRequestLibrary.connections key
        :param url_tail: str
        :param headers: dict
        :return: requests.models.Response instance
        """
        connection = self._get_connection(alias)
        url = connection.server_url + url_tail

        if not headers:
            headers = connection.headers

        try:
            response = requests.api.get(url=url, headers=headers)
        except requests.exceptions.ConnectionError:
            raise AssertionError(f"Can't connect to the URL: {url}. Connection error occurred.")
        return response

    def check_if_response_contains_service(self,
                                           alias: str,
                                           url_tail: str,
                                           data: dict,
                                           service_id: int):
        """
        The method provides the functionality of checking the POST-request answer if it contains
        the service with id `service_id`.
        :param alias: str, according to RESTRequestLibrary.connections key
        :param url_tail: str
        :param data: dict
        :param service_id: int
        :return: None
        """

        response = self.post_request(alias, url_tail, data)
        return any((('id', service_id) in service.items() for service in response.json().get('items')))
