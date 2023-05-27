from flask import Flask

from .admin import admin
from .models import db, login, migrate, User
from . import views


def insert_admin(*args, **kwargs):
    u = User()
    u.username="admin"
    u.pwd = '123'
    u.is_admin = True
    db.session.add(u)
    db.session.commit()


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "informatics"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"

    db.init_app(app)
    login.init_app(app)
    admin.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)

    app.add_url_rule("/", view_func=views.index_page)
    app.add_url_rule("/<int:theme_id>", view_func=views.theme_page, methods=["GET", "POST"])
    app.add_url_rule("/profile", view_func=views.profile, methods=["GET"])
    app.add_url_rule("/add_theme/", view_func=views.add_theme, methods=["GET", "POST"])
    app.add_url_rule("/login/", view_func=views.login_page, methods=["GET", "POST"])
    app.add_url_rule("/signup/", view_func=views.signup, methods=["GET", "POST"])
    app.add_url_rule("/logout/", view_func=views.logout)

    return app
