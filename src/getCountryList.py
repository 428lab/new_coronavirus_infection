# -*- coding: utf-8 -*-
import sys
import csv


def convert_count_by_country(csv_data):
    countries = []
    for date, country, confirmed ,deaths, recovered in zip(csv_data['ObservationDate'], csv_data['Country/Region'],csv_data['Confirmed'],csv_data['Deaths'],csv_data['Recovered']):
        countries.append(country)
    print(set(countries ))


def read_csv(filename):
    data = {}
    with open(filename) as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            for cnt, name in enumerate(header):
                if name not in data:
                    data[name] = []
                data[name].append(row[cnt])
    convert_count_by_country(data)

if __name__ == '__main__':

    ############################################################
    # Read csv file and country.json
    ############################################################
    args = sys.argv
    covid_19_data = read_csv('covid_19_data.csv')



