from property_evaluator import PropertyEvaluator
import os

def getProperties():
        csv_file = os.path.join(os.getcwd(), "resources", "configurations.csv")
        properties = []

        try:
            with open(csv_file, 'r') as file:
                for line in file:
                    values = [val.strip() for val in line.split(",")]
                    property_evaluator = PropertyEvaluator(values[0], int(values[1]), int(values[2]), int(values[3]), int(values[4]))
                    properties.append(property_evaluator)
        except IOError as e:
            print("Error reading configurations.csv file:", e)
        return properties