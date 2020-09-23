"""
Created on: 14 Sep 2020
Created by: Philip.P_adm

Module to load data from habitdash.com API for WHOOP data
"""
import json
import os

import pandas as pd
import requests

from whoop.utils import find, df_columns_to_dict

pd.set_option('display.width', 500)
pd.set_option('display.max_columns', 15)

if __name__ == "__main__":
    habitdash_cfg = json.load(
        open(find(folder_path=os.getcwd(),
                  pattern='habitdash_config_private.json',
                  full_path=True),
             'r'))

    # ---------------------
    # QUERY THE FIELDS DATA
    # ---------------------
    fields_url = "https://api.habitdash.com/v1/fields/"

    response = requests.request(
        "GET",
        url=fields_url,
        headers=habitdash_cfg,
        params={
            "source": "WHOOP"
        })

    request_response = response.json()
    generic_field_id_results = pd.DataFrame(request_response['results'])
    field_id_to_name_map = df_columns_to_dict(df=generic_field_id_results,
                                              columns=['field_id', 'field_name'])

    # -------------------
    # QUERY PERSONAL DATA
    # -------------------
    data_url = "https://api.habitdash.com/v1/data/"
    query_str = {
        "date_start": "2020-08-01",
        "date_end": "2020-08-31",
        "source": "WHOOP"
    }
    response = requests.request(
        "GET",
        url=data_url,
        headers=habitdash_cfg,
        params=query_str)
    august_data = pd.DataFrame(response.json()['results'])
    august_data['field'] = august_data['field_id'].map(field_id_to_name_map)
    august_data['field'] = [x.replace("whoop_", "") for x in august_data['field']]

    august_data['date'] = pd.to_datetime(august_data['date'])
    august_data.set_index('date', inplace=True)
    august_data.sort_index(inplace=True, ascending=True)
    august_data['value'] = pd.to_numeric(august_data['value'])

    strain_score = august_data[august_data['field'] == 'strain_score']['value']

    type(strain_score)