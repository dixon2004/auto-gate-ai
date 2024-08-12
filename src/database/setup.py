from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from src.utils.config import DATABASE_URL
from src.utils.log import write_log


# Create a new client and connect to the server
client = MongoClient(DATABASE_URL, server_api=ServerApi('1'))
database = client["smart-gate"]


# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    write_log("info", "Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    write_log("error", f"Failed to ping your deployment: {e}")
