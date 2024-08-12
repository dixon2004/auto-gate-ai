from src.database.setup import database
from src.utils.log import write_log
import time


class VisitorRecord:

    def __init__(self) -> None:
        """
        Initialize the visitor record database.
        """
        self.collection = database["visitor-record"]


    def insert(self, data: dict) -> None:
        """
        Insert a visitor record into the database.
        """
        try:
            self.collection.insert_one(data)
        except Exception as e:
            write_log("error", f"[VisitorRecord] Failed to insert visitor record: {e}")


    def find_all(self) -> list:
        """
        Returns all visitor records in the database.

        Returns:
            list: list of all visitor records in the database.
        """
        try:
            current_time = time.time()
            visitors = list(self.collection.find({}))
            
            valid_visitors = []
            for visitor in visitors:
                exit_time = visitor.get('exit_time')
                if exit_time and current_time > exit_time:
                    self.collection.delete_one({"_id": visitor["_id"]})
                else:
                    valid_visitors.append(visitor)
            
            return valid_visitors
        
        except Exception as e:
            write_log("error", f"[VisitorRecord] Failed to retrieve visitor records: {e}")


    def delete(self, license_plate: int) -> None:
        """
        Delete a visitor record from the database.

        Args:
            license_plate (int): The license plate of the visitor.
        """
        try:
            self.collection.delete_many({"license_plate": license_plate})
        except Exception as e:
            write_log("error", f"[VisitorRecord] Failed to delete visitor record: {e}")


    def find_by_car_plate(self, car_plate: int) -> dict:
        """
        Find a visitor record by car plate.

        Args:
            car_plate (int): The car plate of the visitor.

        Returns:
            dict: The visitor data.
        """
        try:
            current_time = time.time()            
            for visitor in self.collection.find({"license_plate": car_plate}, {}):
                enter_time = visitor.get('enter_time')
                exit_time = visitor.get('exit_time')

                if enter_time and exit_time:
                    if (enter_time - 1800) < current_time < (exit_time + 1800):
                        return visitor
                    elif exit_time < current_time:
                        self.collection.delete_one({"_id": visitor["_id"]})
            
            return None
        except Exception as e:
            write_log("error", f"[VisitorRecord] Failed to retrieve visitor by license plate: {e}")
