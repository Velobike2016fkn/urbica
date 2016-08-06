__author__ = 'DmitriyBrosalin'

from pymongo import MongoClient
import json


class VeloPositionToJSONClass():
    def __init__(self, path_to_file):
        self.path_to_file = path_to_file
        self.VeloPosition = self.establish_connection()

    def establish_connection(self):
        client = MongoClient('localhost', 27017)
        db_ = client['VeloPosition']
        VeloPosition = db_.VeloPosition
        return VeloPosition

    def make_mongo_eat_data(self, path_to_file):
        print("Start processing data...")
        bulc = self.VeloPosition.initialize_unordered_bulk_op()
        with open(path_to_file) as f:
            velo_data = json.load(f)
        velo_data = velo_data.values()[0]
        for item in velo_data:
            bulc.insert(item)
        bulc.execute()
        print("Data processed !!!")

    def make_me_happy(self):
        self.make_mongo_eat_data(self.path_to_file)