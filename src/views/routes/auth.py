from flask import Blueprint, render_template, redirect, flash, url_for, request, session
from src.database.user import UserDatabase
from src.utils.log import write_log
import time


auth_bp = Blueprint('auth', __name__, template_folder='./templates')

user_db = UserDatabase()


def is_cooldown_period() -> bool:
    """
    Check if the cooldown period is active.

    Returns:
        bool: True if the cooldown period is active, False otherwise.
    """
    try:
        return session.get("cooldown") and time.time() < session["cooldown"]
    except Exception as e:
        write_log("error", f"[API] Failed to check cooldown period: {e}")


def increment_attempts() -> None:
    """
    Increment the number of login attempts and set cooldown if needed.
    """
    try:
        session["attempts"] = session.get("attempts", 0) + 1
        if session["attempts"] >= 3:
            session.pop("attempts", None)
            session["cooldown"] = time.time() + (60 * 60)
    except Exception as e:
        write_log("error", f"[API] Failed to increment login attempts: {e}")


@auth_bp.route("/login", methods=['GET', 'POST'])
def login():
    """
    Login the user.
    """
    try:
        if request.method == 'POST':
            phone_number = request.form.get('phone_number', '').strip()
            password = request.form.get('password', '')

            if is_cooldown_period():
                write_log("error", f"[API] Too many login attempts: {phone_number}")
                flash('Too many attempts. Please try again later.', 'warning')
                return redirect(url_for('auth.login'))

            if not phone_number:
                return redirect(url_for('auth.login'))
            
            if not password:
                return redirect(url_for('auth.login'))
            
            user = user_db.find_by_phone_number(phone_number)
            if user and password == user['password']:
                session['phone_number'] = phone_number
                session["logged_in"] = time.time()
                session.pop('attempts', None)
                session.pop('cooldown', None)
                flash('Login successful.', 'success')
                
                if user["role"] == "Resident":
                    return redirect(url_for('visitor.visitor'))
                else:
                    return redirect(url_for('history.home'))
            else:
                increment_attempts()
                write_log("error", f"[API] Invalid phone number or password: {phone_number}")
                flash('Invalid phone number or password.', 'error')
                return redirect(url_for('auth.login'))

        return render_template('auth/login.html')
    
    except Exception as e:
        write_log("error", f"[API] Failed to login: {e}")


@auth_bp.route("/logout")
def logout():
    """
    Logout the user.
    """
    try:
        session.pop('phone_number', None)
        flash('Logged out successfully.', 'success')
        return redirect(url_for('auth.login'))
    
    except Exception as e:
        write_log("error", f"[API] Failed to logout: {e}")
