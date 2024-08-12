from src.utils.utils import clean_string, check_login, convert_to_utc, format_times
from flask import Blueprint, redirect, flash, render_template, session, request
from src.database.visitor import VisitorRecord
from src.views.routes.auth import user_db
from src.utils.log import write_log


visitor_bp = Blueprint('visitor', __name__)

visitor_db = VisitorRecord()


@visitor_bp.route("/visitor")
def visitor():
    """
    Load the visitor page.
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

        records = visitor_db.find_all()
        records = format_times(records)
        if user_role == 'Admin':
            records = [record for record in records if record['group'] == user_group]
        elif user_role == 'Resident':
            records = [record for record in records if record['phone_number'] == phone_number]

        return render_template("visitor.html", record=records, whitelisted=whitelisted)
    
    except Exception as e:
        write_log("error", f"[API] Failed to load visitor page: {e}")


@visitor_bp.route('/add_visitor', methods=['POST'])
def add_visitor():
    """
    Add a visitor record.
    """
    try:
        return handle_visitor_request(request.form, 'add')
    except Exception as e:
        write_log("error", f"[API] Failed to add visitor record: {e}")


@visitor_bp.route('/delete_visitor', methods=['POST'])
def delete_visitor():
    """
    Delete a visitor record.
    """
    try:
        return handle_visitor_request(request.get_json(), 'delete')
    except Exception as e:
        write_log("error", f"[API] Failed to delete visitor record: {e}")


def handle_visitor_request(form_data: dict, action: str):
    """
    Handle a visitor request.
    
    Args:
        form_data (dict): The form data.
        action (str): The action to perform.
    """
    try:
        phone_number = session.get('phone_number')
        if not phone_number:
            flash("Please login to access the page.", "warning")
            return redirect("/login")

        user = user_db.find_by_phone_number(phone_number)
        if not user:
            flash("Please login to access the page.", "warning")
            return redirect("/login")

        if action == 'add':
            user_group = user['group']
            visitor_data = {
                "group": user_group,
                "phone_number": phone_number,
                "vehicle_type": form_data.get('vehicle_type'),
                "license_plate": clean_string(form_data.get('license_plate')),
                "enter_time": convert_to_utc(form_data.get('enter_time')),
                "exit_time": convert_to_utc(form_data.get('exit_time')),
            }
            visitor_db.insert(visitor_data)
            flash("Visitor record added successfully.", "success")
            write_log("info", f"[API] Added visitor record: {visitor_data}")
            return redirect("/visitor")
        
        elif action == 'delete':
            license_plate = clean_string(form_data.get('license_plate'))
            if license_plate:
                visitor_db.delete(license_plate)
                write_log("info", f"[API] Deleted visitor record: {license_plate}")
                
            return {"success": True}
        
    except Exception as e:
        write_log("error", f"[API] Failed to handle visitor request: {e}")
