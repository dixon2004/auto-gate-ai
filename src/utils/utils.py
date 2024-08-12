from src.utils.log import write_log
from flask import flash, redirect
from datetime import datetime
import time
import pytz


def convert_to_malaysia_time(unix_timestamp: int) -> str:
    """
    Convert a Unix timestamp to Malaysia time.

    Args:
        unix_timestamp (int): The Unix timestamp to convert.

    Returns:
        str: The Malaysia time in the format "YYYY-MM-DD HH:MM:SS".
    """
    try:
        utc_time = datetime.fromtimestamp(unix_timestamp, pytz.utc)
        malaysia_zone = pytz.timezone('Asia/Kuala_Lumpur')
        malaysia_time = utc_time.astimezone(malaysia_zone)
        return malaysia_time.strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        write_log("error", f"[Utils] Failed to convert to Malaysia time: {e}")


def format_times(record: list) -> list:
    """
    Convert UTC timestamps to Malaysia time and format them.
    
    Args:
        record (list): The list of records to format.

    Returns:
        list: The list of records with formatted timestamps.
    """
    try:
        for r in record:
            if r.get('enter_time'):
                r['enter_time'] = convert_to_malaysia_time(r['enter_time'])

            if r.get('exit_time'):    
                r['exit_time'] = convert_to_malaysia_time(r['exit_time'])
        return record
    except Exception as e:
        write_log("error", f"[Utils] Failed to format times: {e}")



def convert_to_utc(timestamp: str) -> int:
    """
    Convert a local timestamp string to a UTC datetime object.
    
    Args:
        timestamp (str): The local timestamp string.
        
    Returns:
        timestamp (int): The UTC timestamp.
    """
    try:
        if timestamp:
            utc_tz = pytz.utc
            return datetime.fromisoformat(timestamp).astimezone(utc_tz).timestamp()
        return None
    
    except Exception as e:
        write_log("error", f"[Utils] Failed to convert to UTC: {e}")


def clean_string(input_str: str) -> str:
    """
    Remove spaces from a string.
    
    Args:
        input_str (str): The string to clean.

    Returns:
        string (str): The cleaned string.
    """
    try:
        if input_str:
            return input_str.replace(" ", "").upper().strip()
        return input_str
    except Exception as e:
        write_log("error", f"[Utils] Failed to clean string: {e}")


def check_login(session: dict) -> bool:
    """
    Check if the user is logged in.
    
    Args:
        session (dict): The session object.
        
    Returns:
        bool: True if the user is logged in, False otherwise.
    """
    try:
        if not session.get('phone_number', False):
            flash("Please login to access the page.", "warning")
            return redirect("/login")
        else:
            login_time = session.get("logged_in")
            if time.time() - login_time > 86400:
                session.pop('phone_number', None)
                session.pop('logged_in', None)
                flash("Session expired. Please login again.", "warning")
                return redirect("/login")
        
    except Exception as e:
        write_log("error", f"[Utils] Failed to check login: {e}")
