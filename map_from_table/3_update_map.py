#!/usr/bin/env python3
import csv
import json
from pathlib import Path

import requests

API_KEY = '<api_key>'
MAP_DATA_JSON = Path('map_data.json')
IMAGES_DIR = Path('images')
MARKERS_DIR = Path('markers')


def create_geojson_from_csv(csv_file):
    assert csv_file.is_file()

    features = []

    with open(csv_file, newline='') as f:
        # auto-detect the CSV dialect
        dialect = csv.Sniffer().sniff(f.read())
        f.seek(0)

        # use DictReader which gives a dict for each row
        reader = csv.DictReader(f, dialect=dialect)

        # for each row in the CSV file
        for row in reader:
            row = dict(row)

            lat = float(row['latitude'])
            lon = float(row['longitude'])

            # basic properties
            properties = {
                "title": row['title'],
                "description": row['description'],
                "url": row['url'],
            }

            # if we have an icon from the default set, use it
            if row['icon_default']:
                properties['marker-symbol'] = row['icon_default']

            # if we have a custom icon, use the uploaded marker
            if row['icon_custom']:
                marker_info = get_image_marker_info('marker', row['icon_custom'])
                if marker_info:
                    properties['marker_id'] = marker_info['marker_id']

            # if we have an image, use the uploaded image
            if row['image']:
                image_info = get_image_marker_info('image', row['image'])
                if image_info:
                    properties['image'] = {
                        'id': image_info['image_id'],
                        'w': image_info['width'],
                        'h': image_info['height'],
                        'tip_color': image_info['tip_color'],
                        'avg_color': image_info['avg_color'],
                    }

            # create the GeoJSON for the item
            feature = {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [lon, lat]},
                "properties": properties,
            }
            features.append(feature)

    geojson = {
        "type": "FeatureCollection",
        "features": features,
    }

    return geojson


def get_image_marker_info(kind, file_name):
    assert kind in {'image', 'marker'}

    if kind == 'image':
        file_path = IMAGES_DIR / file_name
    else:
        file_path = MARKERS_DIR / file_name

    if not file_path.is_file():
        print(f'{kind} file missing: {file_path}')
        return

    info_json = file_path.parent / f'{file_path.stem}.json'
    if not info_json.is_file():
        print(f'Info JSON missing, please upload {kind} first: {file_path}')
        return

    with open(info_json) as f:
        return json.load(f)


def update_map(geojson):
    if not MAP_DATA_JSON.is_file():
        print('Please create an empty map first')
        return

    with open(MAP_DATA_JSON) as f:
        map_data = json.load(f)

    url = 'https://maphub.net/api/1/map/update'

    args = {
        'map_id': map_data['id'],
        'geojson': geojson,
        'basemap': 'maphub-light',
        'description': (
            'Sample map for MapHub API tutorial:\n'
            '[Create a map from a table CSV file](https://docs.maphub.net/tutorials/first_map/tutorial.html)\n\n'
            'Texts and images are from visitlondon.com'
        ),
        'visibility': 'public',
    }

    headers = {'Authorization': 'Token ' + API_KEY}

    res = requests.post(url, json=args, headers=headers)
    data = res.json()

    if 'id' not in data:
        print(data['error'])
        return

    print('Map updated')
    print(json.dumps(map_data, indent=2, ensure_ascii=False))


def main():
    geojson = create_geojson_from_csv(Path('table.csv'))
    update_map(geojson)


main()
