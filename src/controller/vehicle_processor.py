import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.database.visitor import VisitorRecord
from src.database.history import HistoryRecord
from src.database.user import UserDatabase
from src.utils.config import ACTION_OPTION
from src.utils.log import write_log
import time


visitor_db = VisitorRecord()
history_db = HistoryRecord()
user_db = UserDatabase()


class VehicleDetectionProcessor:

    def __init__(self) -> None:
        """
        Initialize the process detection controller.
        """
        self.action = ACTION_OPTION
        self.cooldown = 180


    def create_new_entry(self, car_plate: str, user: dict, vehicle_type: str) -> dict:
        """
        Create a new entry record for the vehicle.

        Args:
            car_plate (str): The license plate of the vehicle.
            user (dict): The user data.
            vehicle_type (str): The type of the vehicle.

        Returns:
            dict: The new entry data.
        """
        return {
            "group": user.get("group"),
            "role": user.get("role", "Visitor"),
            "vehicle_type": vehicle_type,
            "license_plate": car_plate,
            "enter_time": time.time(),
            "exit_time": None
        }


    def process_entry(self, car_plate: str, user: dict, vehicle_type: str, data: dict) -> str:
        """
        Handle the entry process for a vehicle.

        Args:
            car_plate (str): The license plate of the vehicle.
            user (dict): The user data.
            vehicle_type (str): The vehicle type.
            data (dict): The existing history data for the vehicle.

        Returns:
            str: The role of the user.
        """
        if data and time.time() - data["enter_time"] < self.cooldown:
            write_log("info", f"{vehicle_type} with {car_plate} already entered before.")
            return user.get("role", "Visitor")

        new_data = self.create_new_entry(car_plate, user, vehicle_type)
        history_db.insert(new_data)
        write_log("info", f"{vehicle_type} with {car_plate} entered.")
        return user.get("role", "Visitor")


    def process_exit(self, car_plate: str, data: dict) -> str:
        """
        Handle the exit process for a vehicle.

        Args:
            car_plate (str): The license plate of the vehicle.
            data (dict): The entry data for the vehicle.

        Returns:
            str: The role of the user.
        """
        if not data:
            write_log("info", f"Vehicle with license plate {car_plate} not found in history records.")
            return
        
        if data.get("exit_time"):
            write_log("info", f"Vehicle with {car_plate} already exited.")
            return data["role"]

        data["exit_time"] = time.time()
        history_db.update(data["_id"], data)
        write_log("info", f"{data['vehicle_type']} with {car_plate} exited.")
        return data["role"]


    def get_user_and_vehicle_type(self, car_plate: str) -> tuple:
        """
        Retrieve the user and vehicle type based on the license plate.

        Args:
            car_plate (str): The license plate of the vehicle.

        Returns:
            tuple: A tuple containing the user data and vehicle type.
        """
        user = user_db.find_by_car_plate(car_plate)
        if not user:
            write_log("info", f"Vehicle with {car_plate} is not registered as resident.")
            user = visitor_db.find_by_car_plate(car_plate)
            if not user:
                write_log("info", f"Vehicle with {car_plate} is not registered as visitor.")
                return None, None
            return user, user["vehicle_type"]

        vehicle = next((v for v in user["vehicle"] if v["license_plate"] == car_plate), None)
        if not vehicle:
            write_log("info", f"Vehicle with {car_plate} not found in user's records.")
            return None, None

        return user, vehicle["type"]


    def verify_vehicle(self, car_plate: str) -> str:
        """
        Verify the vehicle and process the detection.

        Args:
            car_plate (str): The license plate of the vehicle.

        Returns:
            str: The role of the user or None if processing fails.
        """
        try:
            user, vehicle_type = self.get_user_and_vehicle_type(car_plate)
            if not user:
                return

            data = history_db.find_by_car_plate(car_plate)

            if self.action == "entry":
                return self.process_entry(car_plate, user, vehicle_type, data)
            
            if self.action == "exit":                
                return self.process_exit(car_plate, data)

            raise ValueError(f"Invalid action ({self.action}).")

        except Exception as e:
            write_log("error", f"Failed to process detection for {car_plate}: {e}")
            return
        