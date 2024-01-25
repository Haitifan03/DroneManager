import os
from property_evaluator import PropertyEvaluator

def DataRater():    

    def __init__(self, properties):
        self.property_data = properties

    def rate_data(self, json_object):
        completeness_valuation = rate_data_completeness(json_object)
        normalcy_valuation = rate_data_normalcy(json_object)
        return min(normalcy_valuation, completeness_valuation)
    
    def rate_data_completeness(self, json_object):
        total = 0
        total_complete = 0
        for property_evaluator in self.property_data:
            if property_evaluator.evaluate_property(json_object) > 0:
                total_complete += 1
            total += 1
        return total_complete / total

    
    def rate_data_normalcy(self, json_object):
        normalcy_sum = 0
        total_complete = 0
        for property_evaluator in self.property_data:
            if property_evaluator.evaluate_property(json_object) > 0:
                total_complete += 1
                normalcy_sum += property_evaluator.evaluate_property(json_object)
        return normalcy_sum / (3.0 * total_complete)

    def important_values_exist(self, json_object):

        latitudeProperty = PropertyEvaluator("latitude", -90, 90, -90, 90)
        longitudeProperty = PropertyEvaluator("longitude", -180, 180, -180, 180)
        heightProperty = PropertyEvaluator("geodetic_altitude_meters", 0, 10000, 0, 10000)
        timeProperty = PropertyEvaluator("epoch2019", 100000000, float('inf'), 100000000, float('inf'))
        return (
            latitudeProperty.evaluate_property(json_object) > 1 and
            longitudeProperty.evaluate_property(json_object) > 1 and
            heightProperty.evaluate_property(json_object) > 1 and
            timeProperty.evaluate_property(json_object) > 1
        )
    
rater_data = DataRater()

