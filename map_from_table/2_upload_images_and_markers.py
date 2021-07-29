#!/usr/bin/env python3

import json
from pathlib import Path

import requests

API_KEY = '<api_key>'
IMAGES_DIR = Path('images')
MARKERS_DIR = Path('markers')


def upload_image_marker(kind, file_path):
    assert kind in {'image', 'marker'}

    # make sure the image file exists
    assert file_path.is_file()

    # path where we store the info JSON
    info_json = file_path.parent / f'{file_path.stem}.json'

    # if the JSON file exists, the image/marker is already uploaded, skip the upload
    if info_json.is_file():
        print(f'Skipping {kind} {file_path.name}')
        return

    print(f'Uploading {kind} {file_path.name}')

    # ----- upload start -----
    url = f'https://maphub.net/api/1/{kind}/upload'

    # use the file's extension as file_type
    args = {
        'file_type': file_path.suffix[1:],
    }

    headers = {
        'Authorization': 'Token ' + API_KEY,
        'MapHub-API-Arg': json.dumps(args),
    }

    with open(file_path, 'rb') as f:
        # the upload request
        res = requests.post(url, headers=headers, data=f)
        data = res.json()

    # check that upload was successful, if not print error
    if f'{kind}_id' not in data:
        print(data['error'])
        return

    # ----- upload end -----

    # save the image_info dict to disk
    with open(info_json, 'w') as f:
        json.dump(data, f, indent=2)


def main():
    # for each image in the images dir
    for file_path in list(IMAGES_DIR.glob('*.jpg')) + list(IMAGES_DIR.glob('*.png')):
        # upload image
        upload_image_marker('image', file_path)

    # for each marker in the markers dir
    for file_path in MARKERS_DIR.glob('*.png'):
        # upload marker
        upload_image_marker('marker', file_path)


main()
