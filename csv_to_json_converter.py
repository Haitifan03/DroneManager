import csv
import json
import os

class CsvToJsonConverter:
    @staticmethod
    def convert_csv_to_json(csv_file):
        json_array = []

        try:
            with open(csv_file, 'r') as file:
                reader = csv.reader(file)
                headers = next(reader)

                for line in reader:
                    if len(line) < len(headers):
                        continue
                    obj = {headers[i]: line[i] for i in range(len(headers))}
                    json_array.append(obj)

        except FileNotFoundError:
            print(f"File not found: {csv_file}")
        except Exception as e:
            print(f"Error during CSV to JSON conversion: {e}")

        return json_array

    @staticmethod
    def write_json_file(json_array, json_file):
        try:
            os.makedirs(os.path.dirname(json_file), exist_ok=True)
            with open(json_file, 'w') as file:
                json.dump(json_array, file, indent=2)
        except Exception as e:
            print(f"Error writing JSON file: {e}")

    @staticmethod
    def main():
        try:
            # Set the CSV file
            csv_file = os.path.join(os.getcwd(), "Project", "src", "main", "resources", "PBS-TrainingSet-2023-11-28.csv")

            # This can be named anything because it will be a newly created file
            json_file = os.path.join(os.getcwd(), "Project", "src", "main", "resources", "TrainingSet-2003-11-28.json")

            json_array = CsvToJsonConverter.convert_csv_to_json(csv_file)
            CsvToJsonConverter.write_json_file(json_array, json_file)

            print("CSV to JSON conversion completed.")
        except FileNotFoundError as e:
            print(f"File not found: {e}")
        except Exception as e:
            print(f"Error during conversion: {e}")

# Example Usage:
CsvToJsonConverter.main()
