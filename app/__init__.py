from flask import Flask, render_template
from flask import redirect, flash, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config

bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    # Register Blueprint
    from .main import user_bp, book_bp, auth_bp, manager_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(book_bp)
    app.register_blueprint(manager_bp)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.errorhandler(404)
    def page_not_found(error):
        message = "Page Not Found"
        return render_template(
            'response/wrong.html',
            error=error,
            message=message), 404

    @app.errorhandler(500)
    def server_down(error):
        message = "宕宕宕宕..机了"
        return render_template(
            'response/wrong.html',
            error=error,
            message=message), 500

    @app.errorhandler(401)
    def not_authenticated(error):
        flash('用户未登入', 'danger')
        return redirect(url_for('auth.login'))

    @app.errorhandler(403)
    def permission_denied(error):
        flash('权限不足', 'danger')
        return redirect(url_for('auth.login'))

    return app
