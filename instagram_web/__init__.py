from flask import render_template
from app import app
from flask import render_template, request
from instagram_web.blueprints.users.views import users_blueprint
from instagram_web.blueprints.sessions.views import sessions_blueprint
from instagram_web.blueprints.images.views import images_blueprint
from instagram_web.blueprints.donations.views import donations_blueprint
from instagram_web.blueprints.followers.views import followers_blueprint
from flask_assets import Environment, Bundle
from .util.assets import bundles
from flask_login import LoginManager
from models.user import User
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from instagram_web.util.google_oauth import oauth

assets = Environment(app)
assets.register(bundles)

app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(sessions_blueprint, url_prefix="/sessions")
app.register_blueprint(images_blueprint, url_prefix="/images")
app.register_blueprint(donations_blueprint, url_prefix="/donations")
app.register_blueprint(followers_blueprint, url_prefix="/followers")

login_manager = LoginManager()
login_manager.init_app(app)

oauth.init_app(app)

# sentry_sdk.init('YOUR_DSN_HERE', integrations=[FlaskIntegration()])


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(401)
def forbidden(e):
    return render_template('401.html'), 401


@app.route("/")
def home():
    return render_template('home.html')


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)
