from pymongo import MongoClient
from config import DB, PASS
import pandas as pd
import json

class LoadCSV():
    DATABASE = None
    COLLECTION = None

    def __init__(self, csv_name):
        self.csv_name = csv_name
        self.__connect()
        self.__load_csv(self.csv_name)

    def __connect(self):
        try:
            client = MongoClient("mongodb+srv://{}:{}@cluster0.ystvw.mongodb.net".format(DB, PASS))
            self.DATABASE = client.glassdoor_jobs
            self.COLLECTION = self.DATABASE.ft_jobs
        except pymongo.errors.ConnectionFailure as e:
            print("Connection Failure: " + str(e))

    def __load_csv(self, file_name):
        df = pd.read_csv('../resources/' + file_name)
        data = df.to_dict(orient='records')
        self.__insert_csv(data)

    def __insert_csv(self, data):
        try:
            self.COLLECTION.insert_many(data)
        except Exception as e:
            print('Error while inserting data: ' + str(e))


clsLoad = LoadCSV('glassdoor_jobs_cleaned.csv')