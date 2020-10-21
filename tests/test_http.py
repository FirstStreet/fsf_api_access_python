# Author: Kelvin Lai <kelvin@firststreet.org>
# Copyright: This module is owned by First Street Foundation

# External Imports
import asyncio


class TestNetworkErrors:

    def test_error_400(self, setup_connection):

        loop = asyncio.get_event_loop()
        endpoint = ("https://httpstat.us/400", "test_item", "test_product", "test_subtype")
        response = loop.run_until_complete(setup_connection.endpoint_execute([endpoint]))
        print(response)

    def test_error_403(self, setup_connection):

        loop = asyncio.get_event_loop()
        endpoint = ("https://httpstat.us/403", "test_item", "test_product", "test_subtype")
        response = loop.run_until_complete(setup_connection.endpoint_execute([endpoint]))
        print(response)

    def test_error_404(self, setup_connection):

        loop = asyncio.get_event_loop()
        endpoint = ("https://httpstat.us/404", "test_item", "test_product", "test_subtype")
        response = loop.run_until_complete(setup_connection.endpoint_execute([endpoint]))
        print(response)

    def test_error_500(self, setup_connection):

        loop = asyncio.get_event_loop()
        endpoint = ("https://httpstat.us/500", "test_item", "test_product", "test_subtype")
        response = loop.run_until_complete(setup_connection.endpoint_execute([endpoint]))
        print(response)

    def test_error_501(self, setup_connection):

        loop = asyncio.get_event_loop()
        endpoint = ("https://httpstat.us/501", "test_item", "test_product", "test_subtype")
        response = loop.run_until_complete(setup_connection.endpoint_execute([endpoint]))
        print(response)

    def test_error_502(self, setup_connection):

        loop = asyncio.get_event_loop()
        endpoint = ("https://httpstat.us/502", "test_item", "test_product", "test_subtype")
        response = loop.run_until_complete(setup_connection.endpoint_execute([endpoint]))
        print(response)

    def test_error_503(self, setup_connection):

        loop = asyncio.get_event_loop()
        endpoint = ("https://httpstat.us/503", "test_item", "test_product", "test_subtype")
        response = loop.run_until_complete(setup_connection.endpoint_execute([endpoint]))
        print(response)

    def test_error_522(self, setup_connection):

        loop = asyncio.get_event_loop()
        endpoint = ("https://httpstat.us/522", "test_item", "test_product", "test_subtype")
        response = loop.run_until_complete(setup_connection.endpoint_execute([endpoint]))
        print(response)

    def test_error_524(self, setup_connection):

        loop = asyncio.get_event_loop()
        endpoint = ("https://httpstat.us/524", "test_item", "test_product", "test_subtype")
        response = loop.run_until_complete(setup_connection.endpoint_execute([endpoint]))
        print(response)
