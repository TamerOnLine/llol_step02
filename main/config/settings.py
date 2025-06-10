import os

class Config:
    """
    Central configuration class for the Flask application.

    Attributes:
        basedir (str): Root directory of the application.
        db_path (str): Path to the SQLite database file.
        SECRET_KEY (str): Secret key for session security.
        SQLALCHEMY_DATABASE_URI (str): Database URI for SQLAlchemy.
        SQLALCHEMY_TRACK_MODIFICATIONS (bool): Disable modification tracking.
        DEBUG (bool): Enable or disable debug mode.
    """
    basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    db_path = os.path.join(basedir, 'instance', 'lebenslauf.db')

    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_key')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + db_path
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
