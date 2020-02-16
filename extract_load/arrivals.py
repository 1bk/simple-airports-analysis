import datetime as dt
import json
import os
import re
from os import path

import pandas as pd
import requests
from pandas import Series
from pandas.io.json import json_normalize
from requests import Response
from sqlalchemy.engine import ResultProxy
from typing import List, Dict

from util.database import DatabaseConnection
from util.tools import create_dir
from util.yaml_config import read_yaml_file

pd.set_option('display.max_columns', 150)
pd.set_option('display.width', 150)

PARENT_PATH: str = path.dirname(__file__)
ROOT_PATH: str = path.abspath(path.join(PARENT_PATH, '..'))
ROOTER_PATH: str = path.abspath(path.join(PARENT_PATH, '..', ".."))

DBT_DATA_DIR: str = path.join(ROOT_PATH, 'dbt/data')
OUTPUT_DIR: str = path.join(PARENT_PATH, 'output')

CONFIG = read_yaml_file(path.join(PARENT_PATH, 'config.yaml'))
HEADERS = CONFIG['HEADERS']
BASE_WEBSITE = CONFIG['WEBSITE']['ARRIVALS']

CRED = read_yaml_file(path.join(PARENT_PATH, 'cred/credentials.yaml'))
POSTGRES_CRED = CRED['POSTGRES_CRED']
PG_URL = 'postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}'.format(**POSTGRES_CRED)

INPUT_FILE_NAME = CONFIG['OUTPUT']['FILE_NAME']['AIRPORTS']
OUTPUT_FILE_NAME = CONFIG['OUTPUT']['FILE_NAME']['ARRIVALS']


def main():
    tmr = dt.date.today() + dt.timedelta(days=1)
    print(f'Scrapping data for the date: {tmr}')

    airport_code_list = get_airport_code_list('ICAO', 'Malaysia')
    print(f'Airport International Code list: {airport_code_list}')

    valid_hours = [0, 6, 12, 18]

    flights = []
    for airport_code in airport_code_list:
        for hour in valid_hours:
            flights += scrap_flight_stats(airport_code, tmr.year, tmr.month, tmr.day, hour)

    # Imports list of dictionary and flattens data
    df = json_normalize(flights)

    # Replace '.' with '_' for in column names
    df.rename(lambda x: x.replace('.', '_'), inplace=True, axis=1)

    create_dir(OUTPUT_DIR, to_clear=False)

    output_file_path_1: str = os.path.join(DBT_DATA_DIR, OUTPUT_FILE_NAME)
    output_file_path_2: str = os.path.join(OUTPUT_DIR, OUTPUT_FILE_NAME)

    print(f'Saving data to {output_file_path_1}')
    df.to_csv(path_or_buf=output_file_path_1, index=False)

    print(f'Saving data to {output_file_path_2}')
    df.to_csv(path_or_buf=output_file_path_2, index=False)

    print('Sample Results:')
    print(df)

    print('Done')


def get_airport_code_list(iata_or_icao: str = 'ICAO', country: str = 'Malaysia') -> List[str]:
    """Gets the list of Airport Codes (IATA or ICAO). First try database tables. If fails, use CSV."""
    try:
        print(f'Get Airport Code list ({iata_or_icao}) for {country} via Database...')
        results = get_airport_code_list_db(iata_or_icao, country)
    except Exception as e:
        print(f'Failed to get list via Database: {e} | Will get from CSV instead')
        results = get_airport_code_list_csv(iata_or_icao, country)

    return results


def get_airport_code_list_db(iata_or_icao: str = 'ICAO', country: str = 'Malaysia') -> List[str]:
    """Gets the list of Airport Codes (IATA or ICAO) from the Database Table `stg_airports`."""
    with DatabaseConnection(PG_URL) as conn:
        results: ResultProxy = conn.execute(
            f"SELECT {iata_or_icao} FROM public.stg_airports WHERE country = '{country}';"
        )
    return [str(raw_airport_code[0]) for raw_airport_code in results.fetchall()]


def get_airport_code_list_csv(iata_or_icao: str = 'ICAO', country: str = 'Malaysia') -> List[str]:
    """Gets the list of Airport Codes (IATA or ICAO) from the CSV file (alternative to Database Table sourcing)."""
    df = pd.read_csv(
        os.path.join(OUTPUT_DIR, INPUT_FILE_NAME),
        index_col='Airport_ID'
    ).replace('"', '', regex=True)

    airport_code_df: Series = df[df['Country'] == country][iata_or_icao]

    return airport_code_df.tolist()


def scrap_flight_stats(airport_code: str, year: int, month: int, date: int, hour: int) -> List[Dict[str, str]]:
    """Web scrapper for Airport Arrivals from www.flightstats.com"""
    full_url: str = f'{BASE_WEBSITE}/{airport_code}/?year={year}&month={month}&date={date}&hour={hour}'

    response: Response = requests.get(full_url)
    source: str = response.text

    print(f'Getting for Airport Code: {airport_code} | For hour: {hour} | {full_url}')

    # Use REGEX to find the JSON data that ia available in the website source code.
    match = re.search(r'(__NEXT_DATA__\s+?=\s+?)(.*)(\s+?module={})', source)
    raw_data = match.group(2)

    # Use the JSON parser to parse the str
    json_data = json.loads(raw_data)

    # Extract the proper fields in the JSON
    flight_tracker = json_data['props']['initialState']['flightTracker']
    flights = flight_tracker['route']['flights']

    # Add back arrival airport information for joins purposes.
    for flight in flights:
        flight['date'] = flight_tracker['route']['header']['date']
        flight['iata'] = flight_tracker['route']['header']['arrivalAirport']['iata']
        flight['icao'] = flight_tracker['route']['header']['arrivalAirport']['icao']
        flight['airport_name'] = flight_tracker['route']['header']['arrivalAirport']['name']

    print(f'Number of results for {airport_code}: {len(flights)}')

    return flights


def to_time(time_str: str) -> dt.time:
    """Cleans the time string `HH:MM` to a proper datetime.time object"""
    t = time_str.split(':')
    return dt.time(int(t[0]), int(t[1]))


if __name__ == '__main__':
    main()
