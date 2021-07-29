#!/usr/bin/env python3

import json
from pathlib import Path

import requests

API_KEY = '<api_key>'
MAP_DATA_JSON = Path('map_data.json')


def create_empty_map():
    if MAP_DATA_JSON.is_file():
        print('Map already exist')
        return

    url = 'https://maphub.net/api/1/map/upload'

    args = {
        'file_type': 'empty',
        'title': 'London Attractions',
        'short_name': 'london-attractions',
        'visibility': 'public',
    }

    headers = {
        'Authorization': 'Token ' + API_KEY,
        'MapHub-API-Arg': json.dumps(args),
    }

    res = requests.post(url, headers=headers)
    data = res.json()

    if 'id' not in data:
        print(data['error'])
        return

    with open(MAP_DATA_JSON, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print('Map created')
    print(json.dumps(data, indent=2, ensure_ascii=False))


def main():
    create_empty_map()


main()
