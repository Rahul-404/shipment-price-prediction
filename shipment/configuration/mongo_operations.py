import sys
from json import loads
from typing import Collection
from pandas import DataFrame
from pymongo.database import Database
import pandas as pd
from pymongo import MongoClient
from shipment.constant import DB_URL
from shipment.exception import shippingException
from shipment.logger import logging


class MongoDBOperation:

    def __init__(self):
        self.DB_URL = DB_URL
        self.client = MongoClient(self.DB_URL)

    def get_database(self, db_name) -> Database:
        """ 
        
        Mathod Name : get_database

        Description : This method gets databse from MongoDB from the db_name

        Output      : A database is created in MongoDb with name as db_name
        """
        logging.info("Entered get_databse method of MongoDB_Operation class")

        try:
            # Getting the DB
            db = self.client[db_name]

            logging.info(f"Create {db_name} database is MongoDB")
            logging.info("Exited get_databse method MongoDB_Operation class")
            return db
        except Exception as e:
            raise shippingException(e, sys) from e
        
    @staticmethod
    def get_collection(database, colelction_name) -> Collection:

        """ 
        Method Name : get_collection

        Description : This method gets collection from the particular databse and collection name

        Output      : A collection is returned from databse with name as collection name
        
        """
        logging.info("Entered get_collection method of MongoDB_Operation class")

        try:
            # Getting the collection name
            collection = database[colelction_name]

            logging.info(f"Created {colelction_name} collection in mongodb")
            logging.info("Exited get_collcetion method of MongoDB_Operation class")
            return collection
        except Exception as e:
            raise shippingException(e, sys) from e
        
    def get_collection_as_dataframe(self, db_name, collection_name) -> DataFrame:
        """ 
        Method Name : get_collection_as_dataframe

        Description : This mthod is used for converting the selected collection to dataframe

        Output      : A collection is returned from the selected db_name and collection_name
        
        """
        logging.info(
            "Entered get_collection_as_dataframe method of MongoDB_Operation class"
        )

        try:
            # Getting the database
            databse = self.get_database(db_name)

            # Getting the collection name
            collection = databse.get_collection(name=collection_name)

            # Reading the datafarme and dropping the _id column
            df = pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"],axis=1)

            logging.info("Converted collection to dataframe")
            logging.info(
                "Exited get_collection_as_dataframe method of MongoDB_Operation class"
            )
            return df
        
        except Exception as e:
            raise shippingException(e, sys) from e
        
    def insert_dataframe_as_record(self, data_frame, db_name, collection_name) -> None:
        """ 
        
        Method Name : insert_dataframe_as_record

        Description : This method inserts the dataframe as record in databse collection

        Output      : The dataframe is inserted in database collection
        """
        logging.info("Entered insert_dataframe_as_record method of MongoDB_Operation")

        try:
            # Converting dataframe into json
            records = loads(data_frame.T.to_json()).values()
            logging.info(f"Converted dataframe to json records")

            # Getting the database and collection
            database = self.get_database(db_name)
            collection = database.get_collection(collection_name)
            logging.info("Inserting records to MongoDB")

            # Inserting data to MongoDB databse
            collection.insert_many(records)
            logging.info("Inserted records to MongoDB")
            logging.info(
                "Exited the insert_dataframe_as_record method of MongoDB_Operation"
            )

        except Exception as e:
            raise shippingException(e, sys) from e