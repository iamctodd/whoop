"""
Created on: 14 Sep 2020
Created by: Philip.P_adm

Module to load data from habitdash.com API for WHOOP data
"""
import json

import requests

from utils import find

habitdash_cfg = json.load(open(
    find(folder_path='dataload/config', pattern='habitdash_private.json', full_path=True),
    'r'))

response = requests.request("GET",
                            url=habitdash_cfg["url"],
                            headers=habitdash_cfg,
                            params={
                                "source": "WHOOP",
                                # "date_start": "2020-09-01",
                                # "date_end": "2020-09-03"
                            }
                            )
print(response.text)

generic_results = response.json()
generic_field_id_results = generic_results['results']
