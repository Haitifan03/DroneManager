import json
import os
from drone import Drone
from property_evaluator import PropertyEvaluator
from epoch_time_manager import epoch_to_iso8601
from property_data import get_property_data


class DataProcessor:
    objectMapper = json.JSONEncoder()

    latitude = "latitude"
    longitude = "longitude"
    unique_id = "unique_id"
    height = "geodetic_altitude_meters"
    timeStamp = "epoch2019"

    latitudeProperty = PropertyEvaluator(latitude, -90, 90, -90, 90)
    longitudeProperty = PropertyEvaluator(longitude, -180, 180, -180, 180)
    heightProperty = PropertyEvaluator(height, 0, 10000, 0, 10000)
    timeProperty = PropertyEvaluator(timeStamp, 100000000, float('inf'), 100000000, float('inf'))

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

                property_data = get_property_data()
                for json_object in json_array:
                    uid = json_object[DataProcessor.unique_id]

                    uids_set.add(uid)

                    completeness_valuation = DataProcessor.rate_data_completeness(json_object, property_data)
                    normalcy_valuation = DataProcessor.rate_data_normalcy(json_object, property_data)
                    json_object["rating"] = min(normalcy_valuation, completeness_valuation)

                    if DataProcessor.important_values_exist(json_object):
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
    def important_values_exist(json_object):
        return (
            DataProcessor.latitudeProperty.evaluate_property(json_object) > 1 and
            DataProcessor.longitudeProperty.evaluate_property(json_object) > 1 and
            DataProcessor.heightProperty.evaluate_property(json_object) > 1 and
            DataProcessor.timeProperty.evaluate_property(json_object) > 1
        )

    @staticmethod
    def rate_data_completeness(json_object, property_data):
        total = 0
        total_complete = 0
        for property_evaluator in property_data:
            if property_evaluator.evaluate_property(json_object) > 0:
                total_complete += 1
            total += 1
        return total_complete / total

    @staticmethod
    def rate_data_normalcy(json_object, property_data):
        normalcy_sum = 0
        total_complete = 0
        for property_evaluator in property_data:
            if property_evaluator.evaluate_property(json_object) > 0:
                total_complete += 1
                normalcy_sum += property_evaluator.evaluate_property(json_object)
        return normalcy_sum / (3.0 * total_complete)

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
