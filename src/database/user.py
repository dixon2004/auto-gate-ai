from src.utils.config import ADMIN_PHONE_NUMBER, ADMIN_PASSWORD
from src.database.setup import database
from src.utils.log import write_log


class UserDatabase:

    def __init__(self):
        """
        Initialize the user database.
        """
        self.collection = database["users"]
        self.add_admin_user()


    def find_all(self) -> list:
        """
        Returns all users in the database.
        
        Returns:
            list: list of all users in the database.
        """
        try:
            return list(self.collection.find({}, {"_id": False}))
        except Exception as e:
            write_log("error", f"[UserDatabase] Failed to retrieve users: {e}")
        

    def find_by_phone_number(self, phone_number: int) -> dict:
        """
        Find a user by phone number.
        
        Args:
            phone_number (int): The phone number of the user.
            
        Returns:
            dict: The user data.
        """
        try:
            return self.collection.find_one({"phone_number": phone_number}, {"_id": False})
        except Exception as e:
            write_log("error", f"[UserDatabase] Failed to retrieve user by phone number: {e}")
    

    def add_user(self, user: dict) -> None:
        """
        Add a user to the database.
        
        Args:
            user (dict): The user data.
        """
        try:
            self.collection.insert_one(user)
        except Exception as e:
            write_log("error", f"[UserDatabase] Failed to insert user: {e}")
    

    def add_admin_user(self) -> None:
        """
        Add an admin user to the database.
        """
        try:
            user = self.find_by_phone_number(ADMIN_PHONE_NUMBER)
            if not user:
                user_data = {
                    "phone_number": ADMIN_PHONE_NUMBER,
                    "password": ADMIN_PASSWORD,
                    "address": None,
                    "group": None,
                    "role": "Founder",
                    "vehicle": []
                }
                self.add_user(user_data)
                write_log("info", "Admin user created in database")
                
        except Exception as e:
            write_log("error", f"[UserDatabase] Failed to add admin user: {e}")


    def update_user(self, user: dict) -> None:
        """
        Update a user in the database.
        
        Args:
            user (dict): The user data.
        """
        try:
            self.collection.update_one({"phone_number": user["phone_number"]}, {"$set": user})
        except Exception as e:
            write_log("error", f"[UserDatabase] Failed to update user: {e}")


    def delete_user(self, phone_number: int):
        """
        Delete a user from the database.
        
        Args:
            phone_number (int): The phone number of the user.
        """
        try:
            self.collection.delete_one({"phone_number": phone_number})
        except Exception as e:
            write_log("error", f"[UserDatabase] Failed to delete user: {e}")
    

    def find_by_car_plate(self, car_plate: str) -> dict:
        """
        Find a user by car plate.
        
        Args:
            car_plate (str): The license plate of the vehicle.
            
        Returns:
            dict: The user data.
        """
        try:
            return self.collection.find_one({"vehicle": {"$elemMatch": {"license_plate": car_plate}}})
        except Exception as e:
            write_log("error", f"[UserDatabase] Failed to retrieve user by car plate: {e}")
