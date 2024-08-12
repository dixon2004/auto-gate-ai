import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from flask_limiter.util import get_remote_address
from src.views.routes.resident import resident_bp
from src.views.routes.history import history_bp
from src.views.routes.visitor import visitor_bp
from src.views.routes.auth import auth_bp
from flask_limiter import Limiter
from config import Config
from flask import Flask
import os


app = Flask(__name__, template_folder='./templates')
app.config.from_object(Config)

# Initialize rate limiter
limiter = Limiter(
    get_remote_address, 
    app=app,
    default_limits=["20 per minute"],
    storage_uri=app.config['DATABASE_URL'],
    strategy="moving-window"
)

# Register blueprints
app.register_blueprint(resident_bp)
app.register_blueprint(history_bp)
app.register_blueprint(visitor_bp)
app.register_blueprint(auth_bp)


if __name__ == "__main__":
    app.run(port=app.config['PORT'], debug=False, use_reloader=False)