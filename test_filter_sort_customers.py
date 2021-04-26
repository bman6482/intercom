import unittest
from collections import namedtuple
from filter_sort_customers import Customers


class TestCustomers(unittest.TestCase):
    def test_customers_filtering(self):
        """
        Test that it can filter and sort customers
        """
        customer_list_file = '/data2/input_data/intercom/customers.txt'
        office_location = '53.339428, -6.257664'
        distance_range = 100
        expected_customer_list_size = 16
        customers = Customers()
        customers.load_from_file(customer_list_file)
        coordinates = Customers.validate_extract_location(office_location)
        customers.filter_by_distance(coordinates, distance_range)
        customers.sort_by_id()
        customer_list_size = len(customers.customer_list)
        self.assertEqual(customer_list_size, expected_customer_list_size)


if __name__ == '__main__':
    unittest.main()
