from src.database.setup import database
from src.utils.log import write_log


class HistoryRecord:

    def __init__(self) -> None:
        """
        Initialize the history record database.
        """
        self.collection = database["history-record"]


    def insert(self, data: dict) -> None:
        """
        Insert a history record into the database.
        
        Args:
            data (dict): The history record data.
        """
        try:
            self.collection.insert_one(data)
        except Exception as e:
            write_log("error", f"[HistoryRecord] Failed to insert history record: {e}")


    def find_all(self) -> list:
        """
        Returns all history records in the database.

        Returns:
            list: list of all history records in the database.
        """
        try:
            return list(self.collection.find({}, {"_id": False}))
        except Exception as e:  
            write_log("error", f"[HistoryRecord] Failed to retrieve history records: {e}")


    def find_by_car_plate(self, car_plate) -> dict:
        """
        Find a history record by car plate.
        
        Args:
            car_plate (str): The license plate of the vehicle.
            
        Returns:
            dict: The latest history record.
        """
        try:
            data = list(self.collection.find({"license_plate": car_plate}, {})
                                        .sort("enter_time", -1)
                                        .limit(1))
            if data:
                return data[0]
            else:
                return {}
        except Exception as e:
            write_log("error", f"[HistoryRecord] Failed to retrieve history record by car plate: {e}")


    def update(self, id: str, data: dict) -> None:
        """
        Update a history record in the database.
        
        Args:
            id (str): The ID of the history record.
            data (dict): The updated history record data.
        """
        try:
            self.collection.update_one({"_id": id}, {"$set": data})
        except Exception as e:
            write_log("error", f"[HistoryRecord] Failed to update history record: {e}")
