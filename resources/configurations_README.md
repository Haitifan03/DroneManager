This adheres to the F3411-22a_Standard Specification for Remote ID and Tracking

This document's purpose is to add comments to configurations.csv given that they cannot be
added directly to the file without messing up the program.

Each configuration is set based off of an attribute, a lower and upper bound of normal values, and
// a lower and upper bound of what would be abnormal but still potentially legitimate
//values outside of these two bounds are marked as extremely strange in calculations
//explanations for each are given below

speed_meters_second, 0, 44, 45, 100
// speeds below 0 are impossible
// speeds above 100 meters per second are so high as to be highly improbable for a drone

area_floor, 24, 24, 12, 12
area_ceiling, 24, 24, 12, 12
// area floor and ceiling are normally 24, abnormally 12 and suspicious if anything else

track_direction, 1, 360, 361, 720
// track direction according to the standard should be between 1 and 360 inclusive
// 361 may be legitimate if there is no horizontal movement
// Values above 361 are common in legitimate data as a programming convenience according to client
// Values below 1 or above 720 show a complete disregard of this standard

ua_type, 2, 2, 2, 2
// according to the standard, drones are marked a 2
// anything besides a 2 in drone data is highly suspicious
// As an example, the SQUID_RID data marked itself as 1, an aeroplane

operational_status, 1, 2, 0, 3
// 1 and 2 mark a vehicle in flight or on the ground
// 0 marks undeclared, 3 marks emergency
// anything outside of those either disregards the standard or indicates Remote ID system failure

vertical_accuracy, 1, 6, 0, 15
    0: $150 m or Unknown 1: <150 m
    2: <45 m
    3: <25 m
    4: <10 m
    5: <3 m
    6: <1 m
    7-15: Reserved
//depending on the drone, accuracy may fluctuate


horizontal_accuracy, 6, 11, 1, 12
   0: $18.52 km (10 NM) or Unknown 1: <18.52 km (10 NM)
   2: <7.408 km (4 NM)
   3: <3.704 km (2 NM)
   4: <1852 m (1 NM)
   5: <926 m (0.5 NM)
   6: <555.6 m (0.3 NM)
   7: <185.2 m (0.1 NM)
   8: <92.6 m (0.05 NM)
   9: <30 m
   10: <10 m
   11: <3 m
   12: <1 m
   13-15: Reserved
//extremely low accuracy may be normal for a large aircraft, but not for a drone
//12 would be extremely high, approaching military grade. Not suitable for civilian drones


