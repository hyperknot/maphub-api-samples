#!/usr/bin/env python3

import json
from pathlib import Path

import requests

API_KEY = '<api_key>'
MAP_DATA_JSON = Path('map_data.json')


def refresh_image():
    if not MAP_DATA_JSON.is_file():
        print('Please create an empty map first')
        return

    with open(MAP_DATA_JSON) as f:
        map_data = json.load(f)

    url = 'https://maphub.net/api/1/map/refresh_image'

    args = {
        'map_id': map_data['id'],
    }

    headers = {'Authorization': 'Token ' + API_KEY}

    res = requests.post(url, json=args, headers=headers)
    data = res.json()

    if 'id' not in data:
        print(data['error'])
        return

    print(data['message'])


def main():
    refresh_image()


main()
