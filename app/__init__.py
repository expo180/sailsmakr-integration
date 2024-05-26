from flask import Flask
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_oauthlib.client import OAuth
from flask_restcountries import CountriesAPI
from flask_migrate import Migrate
from flask_babel import Babel
from .role_helpers import inject_role_helpers
from .filters import mask_token

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
bootstrap = Bootstrap()
mail = Mail()
db = SQLAlchemy()
moment = Moment()
oauth = OAuth()
rapi = CountriesAPI()
migrate = Migrate()
babel = Babel()

def create_app(development=True):
    app = Flask(__name__)
    app.config.from_object(config['development'])
    config['development'].init_app(app)
    inject_role_helpers(app)
    bootstrap.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    moment.init_app(app)
    login_manager.init_app(app)
    oauth.init_app(app)
    rapi.init_app(app)
    babel.init_app(app)
    
    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    @app.template_filter
    def _jinja2_filter_truncate(s, length=17):
        if len(s) > length:
            return s[:length] + '...'
        return s
    
    filters.register_filters(app)

    
    @app.template_filter('strftime')
    def _jinja2_filter_strftime(dt, fmt=None):
        if dt:
            return dt.strftime(fmt)
        else:
            return None

    with app.app_context():
        db.create_all()
        from .models import Role
        Role.insert_roles()
        

    return app
