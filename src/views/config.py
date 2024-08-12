from src.utils.port import PortConfiguration
import os
    

class Config:
    """
    Configuration settings for the Flask application.
    """
    SECRET_KEY = os.urandom(24)
    PORT = PortConfiguration().get_port()
    DATABASE_URL = os.getenv("DATABASE_URL")
