"""
Created on: 18 Aug 2020
Created by: Philip.P

Script to update MongoDB Atlas with WHOOP data for Analysis
"""
import json

import numpy as np
import pandas as pd

from whoop.database import (db_arctic_read, db_arctic_append)
from whoop.development.exploratory_analysis import clean_input_data

if __name__ == "__main__":
    data_dir = "/Users/philip_p/Documents/whoop/"
    input_data = pd.read_csv(f"{data_dir}/2020-08-18 Habit Dash (flat file).csv")

    # clean data
    clean_whoop_data = clean_input_data(input_data=input_data)

    # ---------------------
    # WRITE DATA TO MONGODB
    # ---------------------
    mongo_cfg = json.load(
        open('/Users/philip_p/python/src/dataload/config/mongo_private.json', 'r'))

    # initialise the mongoDB library
    # db_arctic_initialise(
    #     mongo_config=mongo_cfg,
    #     library_name='whoop',
    #     library_type=CHUNK_STORE)

    # check if the library is there
    # db_connect(mongo_config=mongo_cfg, is_arctic=True).list_libraries()

    # write data to DB if new dates are present in dataframe
    current_data = db_arctic_read(
        mongo_config=mongo_cfg,
        library='whoop',
        symbol='habitdash')

    current_data.sort_index(axis=1, inplace=True)
    current_data.reset_index(inplace=True)  # get the date index as a column

    old_dates = np.array(current_data['date'].unique(), dtype='datetime64[ns]')
    new_dates = np.array(clean_whoop_data['date'].unique(), dtype='datetime64[ns]')

    new_dates_to_add = np.setdiff1d(new_dates, old_dates)
    if len(new_dates_to_add) > 0:
        print(f"There are {len(new_dates_to_add)} new dates to add to WHOOP data in MongoDB")

        new_whoop_data = clean_whoop_data.loc[clean_whoop_data['date'].isin(new_dates_to_add)]
        new_whoop_data.set_index('date', inplace=True)

        print("Updating MongoDB for new WHOOP data")

        db_arctic_append(mongo_config=mongo_cfg,
                         df=new_whoop_data,
                         library_name='whoop',
                         symbol='habitdash')
    else:
        print("No new WHOOP data to add to the database, process will exit")
