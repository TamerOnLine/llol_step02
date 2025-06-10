from flask import Flask
from .models.models import (
    db, Section, Setting, ResumeSection,
    ResumeParagraph, ResumeField, NavigationLink, LanguageOption
)
from .routes.admin_routes import admin_bp
from .routes.admin_builder_routes import admin_builder_bp
from .routes.admin_paragraph import admin_paragraph
from .routes.admin_field import admin_field


from .routes.public_routes import public_bp
from .routes.main_routes import main_bp
from .extensions import babel
from .i18n_runtime import init_i18n, get_locale
import os
import logging

def create_app():
    """
    Create and configure the Flask application.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object("main.config.settings.Config")
    app.config['LANGUAGES'] = ['de', 'en', 'ar']
    translations_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'translations'))
    app.config['BABEL_TRANSLATION_DIRECTORIES'] = translations_path
    app.debug = True

    logging.basicConfig(level=logging.DEBUG)
    app.logger.setLevel(logging.DEBUG)

    os.makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)
    babel.init_app(app)
    babel.locale_selector_func = get_locale
    init_i18n(app)

    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(public_bp)
    app.register_blueprint(admin_builder_bp)
    app.register_blueprint(admin_paragraph)
    app.register_blueprint(admin_field)
    

    with app.app_context():
        db_path = os.path.join(app.instance_path, 'lebenslauf.db')
        if not os.path.exists(db_path):
            db.create_all()
            insert_initial_sections()
            insert_initial_navigation()
            insert_initial_languages()

    @app.before_request
    def log_locale_info():
        print("Requested locale:", get_locale())
        print("Babel directory:", app.config.get('BABEL_TRANSLATION_DIRECTORIES'))

    @app.context_processor
    def inject_globals():
        nav_links = NavigationLink.query.order_by(NavigationLink.order).all()
        langs = LanguageOption.query.order_by(LanguageOption.order).all()
        return dict(nav_links=nav_links, langs=langs)

    return app

def insert_initial_sections():
    """
    Insert default resume sections into the database.
    """
    default_sections = [
        "Summary", "Career Objective", "Experience", "Qualifications",
        "Skills", "Languages", "Projects", "Links", "Interests"
    ]
    for idx, title in enumerate(default_sections, start=1):
        print(f"Adding section: {title}")
        section = Section(order=idx, title=title, content="")
        db.session.add(section)
    db.session.commit()
    print("Sections inserted.")

def insert_initial_navigation():
    """
    Insert default navigation links into the database.
    """
    if NavigationLink.query.count() == 0:
        nav_items = [
            {"label": "Home", "icon": "🏠", "endpoint": "main.home", "order": 1},
            {"label": "Sections", "icon": "📝", "endpoint": "admin.manage_sections", "order": 2},
            {"label": "Settings", "icon": "🎨", "endpoint": "admin.manage_settings", "order": 3},
            {"label": "Resume", "icon": "📄", "endpoint": "public.resume", "order": 4},
            {"label": "Builder", "icon": "🧱", "endpoint": "admin.resume_builder", "order": 5}
            

        ]
        for item in nav_items:
            link = NavigationLink(**item)
            db.session.add(link)
        db.session.commit()
        print("Navigation links inserted.")

def insert_initial_languages():
    """
    Insert supported languages into the database.
    """
    if LanguageOption.query.count() == 0:
        langs = [
            {"code": "ar", "name": "Arabic", "order": 1},
            {"code": "en", "name": "English", "order": 2},
            {"code": "de", "name": "German", "order": 3}
        ]
        for lang in langs:
            db.session.add(LanguageOption(**lang))
        db.session.commit()
        print("Languages inserted.")
