# app/init.py
from flask import Flask, session, request, redirect
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, current_user
from flask_oauthlib.client import OAuth
from flask_restcountries import CountriesAPI
from flask_migrate import Migrate
from flask_babel import Babel
from .filters import mask_token
from .utils import get_tasks_for_user
from datetime import datetime

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

def get_locale():
    user_language = request.cookies.get('language')
    if user_language:
        return user_language
    return request.accept_languages.best_match(app.config['BABEL_SUPPORTED_LOCALES'])


def create_app(production=True):
    app = Flask(__name__)
    app.config.from_object(config['production'])
    config['production'].init_app(app)
    bootstrap.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    moment.init_app(app)
    login_manager.init_app(app)
    oauth.init_app(app)
    rapi.init_app(app)
    babel.init_app(app, locale_selector=get_locale)
    
    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)


    @app.route('/set_language', methods=['POST'])
    def set_language():
        language = request.form['language']
        response = redirect(request.referrer)
        response.set_cookie('language', language)
        return response

    @app.template_filter
    def _jinja2_filter_truncate(s, length=17):
        if len(s) > length:
            return s[:length] + '...'
        return s
    
    filters.register_filters(app)

    @app.context_processor
    def inject_current_year():
        return {'current_year': datetime.utcnow().year}

    @app.context_processor
    def inject_tasks():
        user_email = session.get('email')
        if user_email:
            tasks = get_tasks_for_user(user_email)
        else:
            tasks = []
        return dict(tasks=tasks)
    

    def get_latest_article():
        from .models import Article
        article = Article.query.order_by(Article.id.desc()).first()
        if article:
            return {
                'title': article.title,
                'content': article.content[:10] + '...' if len(article.content) > 30 else article.content,
                'img_url': article.img_url
            }
        return None

    @app.context_processor
    def inject_latest_article():
        return {'latest_article': get_latest_article()}

    @app.template_filter('strftime')
    def _jinja2_filter_strftime(dt, fmt=None):
        if dt:
            return dt.strftime(fmt)
        else:
            return None

    with app.app_context():
        from .models import Role
        db.create_all()
        Role.insert_roles()
        
    return app
