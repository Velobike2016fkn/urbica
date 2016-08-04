__author__ = 'DmitriyBrosalin'

import glob
from dateutil.parser import parse
from pymongo import MongoClient
import json


class ItemsToJSONClass():
    def __init__(self, directory_path):
        self.directory_path = directory_path
        self.VeloItems = self.establish_connection()

    def parse_string_date_header(self, string):
        string = string.split('+')[0]
        return parse(string).isoformat()

    def establish_connection(self):
        client = MongoClient('localhost', 27017)
        db_ = client['VeloItems']
        VeloItems = db_.VeloItems
        return VeloItems

    def get_list_of_json_files(self, path_to_directory):
        """
        :param path_to_directory: you must provide here path to directory where files from velodata.tar are extracted
                                  WARNING: your path must ends with /*.json
        :return: list of files
        """
        dir_list = glob.glob(path_to_directory)
        return dir_list

    def make_mongo_eat_data(self, path_to_direcory):
        for file in path_to_direcory:
            with open(file) as f:
                single_item = json.load(f)
                data = single_item.values()[0]
                for item in data:
                    file = file.split('/')
                    file = file[len(file)-1]
                    time = self.parse_string_date_header(file)
                    item.update({'time': time})
                    self.VeloItems.insert_one(item)