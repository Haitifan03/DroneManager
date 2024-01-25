import json

class Drone:
    def __init__(self, latitude, longitude, height, uid, iso8601date=None, rating=None):
        self.latitude = latitude
        self.longitude = longitude
        self.height = height
        self.uid = uid
        self.iso8601date = iso8601date or "2023-02-16T10:00:03Z"
        self.rating = rating

    def __eq__(self, other):
        if self is other:
            return True
        if not isinstance(other, Drone):
            return False
        return (
            self.latitude == other.latitude
            and self.longitude == other.longitude
            and self.height == other.height
            and self.uid.casefold() == other.uid.casefold()
        )

    def to_dict(self):
        return {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "height": self.height,
            "rating": self.rating,
            "unique_id": self.uid,
            "date": self.iso8601date,
        }

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["latitude"],
            data["longitude"],
            data["height"],
            data["unique_id"],
            data.get("date", "2023-02-16T10:00:03Z"),
            data.get("rating"),
        )

