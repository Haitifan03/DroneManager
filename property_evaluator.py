class PropertyEvaluator:
    def __init__(self, property, normal_lower, normal_upper, abnormal_lower, abnormal_upper):
        self.property = property
        self.normal_lower = normal_lower
        self.normal_upper = normal_upper
        self.abnormal_lower = abnormal_lower
        self.abnormal_upper = abnormal_upper

    def evaluate_property(self, json_object):
        if self.property in json_object and json_object[self.property]:
            property_value = float(json_object[self.property])
            if self.normal_lower <= property_value <= self.normal_upper:
                return 3
            if self.abnormal_lower <= property_value <= self.abnormal_upper:
                return 2
            return 1
        return 0

    def get_property(self):
        return self.property


# Example Usage:
json_data = {
    "property1": "123.45",
    "property2": "678.90",
    # Add other properties as needed
}

property_evaluator = PropertyEvaluator("property1", 100.0, 200.0, 50.0, 300.0)
result = property_evaluator.evaluate_property(json_data)

print(result)
