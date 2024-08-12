from flask import Blueprint, redirect, flash, render_template, session
from src.utils.utils import check_login, format_times
from src.database.history import HistoryRecord
from src.views.routes.auth import user_db
from src.utils.log import write_log
import time


history_bp = Blueprint('history', __name__)

history_db = HistoryRecord()


@history_bp.route('/')
def main():
    """
    Redirect to the main page.
    """
    try:
        if not session.get('phone_number', False):
            return redirect("/login")
        else:
            login_time = session.get("logged_in")
            if time.time() - login_time > 86400:
                session.pop('phone_number', None)
                session.pop('logged_in', None)
                flash("Session expired. Please login again.", "warning")
                return redirect("/login")
        
        return redirect('/visitor')
    
    except Exception as e:
        write_log("error", f"[API] Failed to load main page: {e}")


@history_bp.route('/history')
def home():
    """
    Load the history page.
    """
    try:
        login_redirect = check_login(session)
        if login_redirect:
            return login_redirect

        phone_number = session.get('phone_number')
        if not phone_number:
            flash("Please login to access the page.", "warning")
            return redirect("/login")

        user = user_db.find_by_phone_number(phone_number)
        if not user:
            flash("Please login to access the page.", "warning")
            return redirect("/login")

        user_role = user['role']
        user_group = user['group']
        whitelisted = user_role in ['Founder', 'Admin']
        if not whitelisted:
            flash("You do not have permission to access the page.", "warning")
            return redirect("/visitor")

        records = history_db.find_all()
        records = format_times(records)
        if user_role != 'Founder':
            records = [record for record in records if record['group'] == user_group]

        return render_template("index.html", record=records, whitelisted=whitelisted)
    
    except Exception as e:
        write_log("error", f"[API] Failed to load history page: {e}")
