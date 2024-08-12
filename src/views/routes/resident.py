from flask import Blueprint, redirect, flash, render_template, session, request
from src.utils.utils import clean_string, check_login
from src.views.routes.auth import user_db
from src.utils.log import write_log


resident_bp = Blueprint('resident', __name__)


@resident_bp.route('/resident')
def resident():
    """
    Load the resident page.
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

        records = user_db.find_all()
        if user_role != 'Founder':
            records = [record for record in records if record['group'] == user_group]

        formatted_records = []
        for record in records:
            if record['role'] != 'Founder':
                for vehicle in record['vehicle']:
                    formatted_records.append({
                        "role": record['role'],
                        "phone_number": record['phone_number'],
                        "home_address": record['home_address'],
                        "vehicle_type": vehicle['type'],
                        "license_plate": vehicle['license_plate']
                    })

        return render_template(
            "resident.html", 
            record=formatted_records, 
            whitelisted=whitelisted,
            role=user_role
            )
    
    except Exception as e:
        write_log("error", f"[API] Failed to load resident page: {e}")


@resident_bp.route('/add_resident', methods=['POST'])
def add_resident():
    """
    Add a resident to the database.
    """
    try:
        return handle_resident_request(request.form, 'add')
    except Exception as e:
        write_log("error", f"[API] Failed to add resident: {e}")


@resident_bp.route('/update_resident', methods=['POST'])
def update_resident():
    """
    Update a resident in the database.
    """
    try:
        return handle_resident_request(request.form, 'update')
    except Exception as e:
        write_log("error", f"[API] Failed to update resident: {e}")


@resident_bp.route('/delete_resident', methods=['POST'])
def delete_resident():
    """
    Delete a resident from the database.
    """
    try:
        return handle_resident_request(request.get_json(), 'delete')
    except Exception as e:
        write_log("error", f"[API] Failed to delete resident: {e}")


@resident_bp.route('/reset_password', methods=['POST'])
def reset_password():
    """
    Reset a resident's password.
    """
    try:
        return handle_resident_request(request.form, 'reset_password')
    except Exception as e:
        write_log("error", f"[API] Failed to reset resident password: {e}")


def handle_resident_request(form_data: dict, action: str):
    """
    Handle the resident request.
    
    Args:
        form_data (dict): The form data.
        action (str): The action to perform
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
        if user_role not in ["Founder", "Admin"]:
            flash("You do not have permission to access the page.", "warning")
            return redirect("/visitor")

        resident_phone_number = clean_string(form_data.get('phone_number'))
        resident = user_db.find_by_phone_number(resident_phone_number)
        if action == 'add':
            if not resident:
                if user_role == "Founder":
                    user_group = form_data.get('group')

                resident_data = {
                    "phone_number": resident_phone_number,
                    "password": form_data.get('password'),
                    "home_address": form_data.get('home_address'),
                    "group": user_group,
                    "role": form_data.get('role').capitalize(),
                    "vehicle": [
                        {
                            "type": form_data.get('vehicle_type'),
                            "license_plate": clean_string(form_data.get('license_plate')),
                        }
                    ]
                }
                user_db.add_user(resident_data)
                flash("Resident record added successfully.", "success")
                write_log("info", f"[API] Resident record added: {resident_phone_number}")
            else:
                flash("Resident record already exists.", "error")
                write_log("info", f"[API] Resident record already exists: {resident_phone_number}")
            return redirect("/resident")

        elif action == 'update':
            if not resident:
                flash("Resident record not found.", "error")
                return redirect("/resident")

            vehicle_type = form_data.get('vehicle_type')
            if not vehicle_type:
                flash("Vehicle type is required.", "error")
                return redirect("/resident")

            license_plate = clean_string(form_data.get('license_plate'))
            if not license_plate:
                flash("License plate is required.", "error")
                return redirect("/resident")

            vehicle_data = {
                "type": vehicle_type,
                "license_plate": license_plate,
            }
            
            if vehicle_data in resident['vehicle']:
                flash("Vehicle record already exists.", "error")
                return redirect("/resident")
            
            resident['vehicle'].append(vehicle_data)
            user_db.update_user(resident)

            flash("Resident record updated successfully.", "success")
            write_log("info", f"[API] Resident record updated ({resident_phone_number}): {vehicle_data}")
            return redirect("/resident")
        
        elif action == "delete":
            if not resident:
                flash("Resident record not found.", "error")
                return redirect("/resident")

            license_plate = clean_string(form_data.get('license_plate'))
            resident['vehicle'] = [vehicle for vehicle in resident['vehicle'] if vehicle['license_plate'] != license_plate]
            if resident['vehicle']:
                user_db.update_user(resident)
                write_log("info", f"[API] Resident vehicle deleted: {license_plate}")
            else:
                user_db.delete_user(resident_phone_number)
                write_log("info", f"[API] Resident record deleted: {resident_phone_number}")

            return {"success": True}
        
        elif action == 'reset_password':
            if not resident:
                flash("Resident record not found.", "error")
                return redirect("/resident")

            resident['password'] = form_data.get('password')
            user_db.update_user(resident)

            flash("Resident password reset successfully.", "success")
            write_log("info", f"[API] Resident password reset: {resident_phone_number}")
            return redirect("/resident")    

    except Exception as e:
        write_log("error", f"[API] Failed to handle resident request: {e}")
