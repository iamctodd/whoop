"""
Created on: 12 Aug 2020
Created by: Philip.P_adm

Test functions for MongoDB (non-relational database)
# TODO: add functions for appending, initialising and creating a library
(without actually doing so and having to delete them)
"""
import json
import unittest

from pymongo import MongoClient

from whoop.database import (db_connect, db_keys_and_symbols, db_arctic_library,
                            db_arctic_read)


class TestMongoDB(unittest.TestCase):
    def setUp(self) -> None:
        mongo_cfg_path = '/Users/philip_p/python/src/dataload/config/mongo_private.json'
        self.mongo_config = json.load(open(mongo_cfg_path, 'r'))
        username = self.mongo_config['mongo_user']
        pw = self.mongo_config['mongo_pwd']
        mongo_url = self.mongo_config['url_cluster']

        self.pymongo_connect = MongoClient(
            host="".join(["mongodb+srv://", username, ":", pw, "@", mongo_url]))

    def test_db_connect_general(self):
        # check that there are databases on MongoDB connection
        self.assertIsNotNone(
            db_connect(mongo_config=self.mongo_config))

    def test_db_connect_arctic(self):
        # check that it works for arctic database
        self.assertIsNotNone(
            db_connect(mongo_config=self.mongo_config,
                       is_arctic=True))

    def test_db_keys_and_symbols(self):
        self.assertIsNotNone(
            db_keys_and_symbols(is_arctic=True,
                                library_name='security_data',
                                mongo_config=self.mongo_config),
            msg="Should've listed the names of the keys and symbols in the "
                "collection on mongoDB Atlas cluster, unless none exist")

    def test_db_arctic_library(self):
        self.assertIsNotNone(
            db_arctic_library(mongo_config=self.mongo_config,
                              library='whoop'),
            msg="Should've listed the names of the libraries unless none exist"
        )

    def test_db_arctic_read(self):
        self.assertIsNotNone(
            db_arctic_read(mongo_config=self.mongo_config,
                           library='whoop',
                           symbol='habitdash'),
            "Should've returned habitdash data in the *whoop** collection on"
            "mongoDB Atlas"
        )


if __name__ == '__main__':
    unittest.main()
