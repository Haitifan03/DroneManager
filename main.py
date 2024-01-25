import json
import os
from drone import Drone
from epoch_time_manager import epoch_to_iso8601
from property_data import DataRater
from property_reader import getProperties


class DataProcessor:
    objectMapper = json.JSONEncoder()

    latitude = "latitude"
    longitude = "longitude"
    unique_id = "unique_id"
    height = "geodetic_altitude_meters"
    timeStamp = "epoch2019"


    @staticmethod
    def main():
        current_dir = os.getcwd()
        json_file_path = os.path.join(current_dir, "resources", "TrainingSet-2003-11-28.json")
        DataProcessor.process_data(json_file_path)

    @staticmethod
    def process_data(json_file):
        logger = DataProcessor.get_logger()

        try:
            with open(json_file, 'r') as file:
                json_array = json.load(file)
                printed_uids = set()
                uids_set = set()

                uid_to_coordinates = {}
                properties = getProperties()
                data_rater = DataRater(properties)

                for json_object in json_array:
                    uid = json_object[DataProcessor.unique_id]

                    uids_set.add(uid)
                    
                    json_object["rating"] = data_rater.rate_data(json_object)

                    if rater.important_values_exist(json_object):
                        DataProcessor.add_json_object_to_map(json_object, uid_to_coordinates)
                    else:
                        printed_uids.add(uid)

                DataProcessor.output_unique_points_to_json(uid_to_coordinates)
        except IOError as e:
            logger.error("Error reading JSON file: %s", e)

    @staticmethod
    def get_logger():
        import logging
        logger = logging.getLogger(DataProcessor.__name__)
        logger.setLevel(logging.INFO)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        logger.addHandler(console_handler)
        return logger



    @staticmethod
    def add_json_object_to_map(json_object, uid_to_coordinates):
        uid = json_object[DataProcessor.unique_id]
        lat = float(json_object[DataProcessor.latitude]) if DataProcessor.latitude in json_object else 0.0
        lon = float(json_object[DataProcessor.longitude]) if DataProcessor.longitude in json_object else 0.0
        alt = float(json_object[DataProcessor.height]) if DataProcessor.height in json_object else 0.0
        rating = float(json_object.get("rating", 0.0))
        epoch = int(json_object[DataProcessor.timeStamp]) if DataProcessor.timeStamp in json_object else 0
        timestamp = epoch_to_iso8601(epoch)

        drone = Drone(lat, lon, alt, uid, timestamp, rating)

        if uid not in uid_to_coordinates:
            uid_to_coordinates[uid] = []

        uid_to_coordinates[uid].append(drone.to_dict())


    @staticmethod
    def output_unique_points_to_json(uid_to_coordinates):
        json_array = {}

        for uid, drone_set in uid_to_coordinates.items():
            sorted_drone_set = sorted(drone_set, key=lambda x: x["date"])

            json_array[uid] = sorted_drone_set

        json_file_path = os.path.join(os.getcwd(), "resources", "cesiumOutput.json")


        with open(json_file_path, 'w') as file_writer:
            # Convert sets to lists before serialization
            json.dump(json_array, file_writer)
            print("JSON objects written to", json_file_path)


if __name__ == "__main__":
    DataProcessor.main()
