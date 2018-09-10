class ParseDataLibrary(object):
    """
    A test library providing keywords for data parsing operation.

    """

    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'

    @staticmethod
    def get_non_purchased_service_id_and_price(enrolled_services: list, available_services: list) -> tuple:
        """
        The method gets a list of services which are available to purchase and don't exist in
        the enrolled services list. Then returns the first one. Raises LookupError if can't find non-bought service.

         Example:
        | @{variable} = | Get non enrolled service id and price | ${subscribed_services} | ${available_services}
        | ${srv_id} | ${srv_price} = | Get non enrolled service id and price | ${subscribed_srv} | ${available_srv}

        :param enrolled_services: list of dictionaries
        :param available_services: list of dictionaries
        :return: tuple (id, cost)
        """
        enrolled_services_id_list = [service.get('id') for service in enrolled_services]
        try:
            non_enrolled_service = next(service for service in available_services
                                        if service.get('id') not in enrolled_services_id_list)
        except StopIteration:
            raise LookupError('There is no non-enrolled services (all available services are bought already)')

        return non_enrolled_service.get('id'), non_enrolled_service.get('cost')
