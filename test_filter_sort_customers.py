import unittest
from filter_sort_customers import Customers


class TestCustomers(unittest.TestCase):
    def test_customers_filtering(self):
        """
        Test that script can filter and sort customers
        """
        customer_list_file = 'customers.txt'
        office_location = '53.339428, -6.257664'
        distance_range = 100
        customers = Customers()
        customers.load_from_file(customer_list_file)
        coordinates = Customers.validate_extract_location(office_location)
        customers.filter_by_distance(coordinates, distance_range)
        customers.sort_by_id()
        self.assertEqual(len(customers.customer_list), 16)
        self.assertEqual(customers.customer_list[0]['user_id'], 4)
        self.assertEqual(customers.customer_list[15]['user_id'], 39)


if __name__ == '__main__':
    unittest.main()
