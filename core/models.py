from datetime import datetime

class Crop:
    def __init__(self, name, harvest_date, sowing_date=None, notes="", crop_type=""):
        self.name = name
        self.harvest_date = datetime.strptime(harvest_date, "%Y-%m-%d")
        self.sowing_date = datetime.strptime(sowing_date, "%Y-%m-%d") if sowing_date else None
        self.notes = notes
        self.crop_type = crop_type

    def to_dict(self):
        return {
            "name": self.name,
            "harvest_date": self.harvest_date.strftime("%Y-%m-%d"),
            "sowing_date": self.sowing_date.strftime("%Y-%m-%d") if self.sowing_date else None,
            "notes": self.notes,
            "crop_type": self.crop_type,
        }