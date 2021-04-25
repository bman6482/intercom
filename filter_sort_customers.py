import sys
import argparse
import json
import logging
import os
from math import radians, sin, cos, acos
from collections import namedtuple


# Usage: python filter_sort_customers.py --customer_list_file <file name>
#                                        --office_location 'longitude, latitude ' --range < distance in km >
# Class to find customer living within a range from office location
class Customers:
    # Constructor to initialize customer list
    def __init__(self):
        self.customer_list = []

    # Function to load customers from a file
    def load_from_file(self, customer_list_file):
        customer_file = open(customer_list_file)
        lines = customer_file.readlines()
        count = 0
        for line in lines:
            count += 1
            self.customer_list.append(json.loads(line.strip()))

    # Function to calculate distance between 2 points on earth
    @staticmethod
    def find_great_circle_distance(longitude1, latitude1, longitude2, latitude2):
        longitude1, latitude1, longitude2, latitude2 = \
            map(lambda x: radians(float(x)), [longitude1, latitude1, longitude2, latitude2])
        distance = 6371 * (acos(sin(latitude1) * sin(latitude2) + cos(latitude1)
                                * cos(latitude2) * cos(longitude1 - longitude2)))
        return distance

    # Function to filter the customer list by a range of distance from a location
    def filter_by_distance(self, office_location, radius):
        logging.debug("Before filter, customer_list size: %d", len(self.customer_list))
        filtered_customers = []
        for customer in self.customer_list:
            distance = self.find_great_circle_distance(customer['longitude'], customer['latitude'],
                                                       office_location.longitude, office_location.latitude)
            if distance < radius:
                filtered_customers.append(customer)
        self.customer_list = filtered_customers
        logging.debug("After filter, customer_list size: %d", len(self.customer_list))

    # Function to sort the customer list by the user_id
    def sort_by_id(self):
        self.customer_list.sort(key=lambda customer: customer['user_id'])

    # Function to print the customers in a format of userid and name
    def print(self):
        logging.debug("customer_list size: %d", len(self.customer_list))
        for customer in self.customer_list:
            print("user id: {}, name: {}".format(customer['user_id'], customer['name']))

    # Function to check whether input file exists
    @staticmethod
    def validate_input_file(file):
        if not os.path.isfile(file):
            raise ValueError("Input file does not exist")

    # Function to check whether input location is in correct format and value
    @staticmethod
    def validate_extract_location(location):
        if "," not in location:
            raise ValueError("Latitude and Longitude need to be provided as comma separated value")
        location_array = location.split(",")
        Location = namedtuple('Location', ['latitude', 'longitude'])
        coordinates = Location(float(location_array[0]), float(location_array[1]))
        if coordinates.latitude > 90 or coordinates.latitude < -90\
                or coordinates.longitude > 180 or coordinates.longitude < -180:
            raise ValueError("Invalid Latitude and Longitude.")
        return coordinates


# main function
def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--customer_list_file", default='/data2/input_data/intercom/customers.txt')
    parser.add_argument("--office_location", default='53.339428, -6.257664')
    parser.add_argument("--range", type=int, default=100)
    args = parser.parse_args()
    Customers.validate_input_file(args.customer_list_file)
    office_coordinates = Customers.validate_extract_location(args.office_location)
    customers = Customers()
    customers.load_from_file(args.customer_list_file)
    customers.filter_by_distance(office_coordinates, args.range)
    customers.sort_by_id()
    print('Customers within {}km distance of office at {}'.format(str(args.range), args.office_location))
    customers.print()


# main program
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s-%(process)d-%(levelname)s-%(message)s')
    try:
        main(sys.argv)
    except ValueError as ve:
        logging.error("Customer processing failed. " + str(ve))
