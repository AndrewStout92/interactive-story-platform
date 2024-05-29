from flask import Flask
from flask_sqlalchemy import SQLAlchemy  # Import SQLAlchemy for database management
from flask_migrate import Migrate  # Import Migrate for handling database migrations
from flask_login import LoginManager  # Import LoginManager for handling user sessions

# Initialize SQLAlchemy instance for database operations
db = SQLAlchemy()

# Initialize Migrate instance for database migrations
migrate = Migrate()

# Initialize LoginManager instance for user session management
login_manager = LoginManager()


def create_app():
    # Create a new Flask application instance
    app = Flask(__name__)

    # Set up the database URI for SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stories.db'

    # Disable SQLALCHEMY_TRACK_MODIFICATIONS to avoid overhead
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Set a secret key for session management and security
    app.secret_key = 'your_secret_key'

    # Initialize the app with SQLAlchemy
    db.init_app(app)

    # Initialize the app with Flask-Migrate
    migrate.init_app(app, db)

    # Initialize the app with Flask-Login
    login_manager.init_app(app)

    # Set the login view to redirect users to the login page if they are not authenticated
    login_manager.login_view = 'main.login'

    # Import the User model for loading users from the database
    from .models import User  # Ensure User is imported here

    # Define user loader callback function for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        # Query the User model by user ID
        return User.query.get(int(user_id))

    # Import and register the main blueprint for organizing routes
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Return the Flask application instance
    return app


