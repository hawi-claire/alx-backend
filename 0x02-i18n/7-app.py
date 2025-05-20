#!/usr/bin/env python3
"""Flask app with timezone support"""
from flask import Flask, render_template, request, g
from flask_babel import Babel, gettext
import pytz
from pytz.exceptions import UnknownTimeZoneError


class Config:
    """Config class for Flask app"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user():
    """Returns a user dictionary or None if ID not found"""
    user_id = request.args.get('login_as')
    if user_id:
        try:
            return users.get(int(user_id))
        except ValueError:
            return None
    return None


@app.before_request
def before_request():
    """Set user as global on flask.g.user"""
    g.user = get_user()


@babel.localeselector
def get_locale():
    """Determine the best match for supported languages"""
    # 1. Locale from URL parameters
    locale = request.args.get('locale')
    if locale and locale in app.config['LANGUAGES']:
        return locale
    
    # 2. Locale from user settings
    if g.user and g.user['locale'] in app.config['LANGUAGES']:
        return g.user['locale']
    
    # 3. Locale from request header
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@babel.timezoneselector
def get_timezone():
    """Determine the best match for timezone"""
    try:
        # 1. Find timezone parameter in URL
        timezone = request.args.get('timezone')
        if timezone:
            return pytz.timezone(timezone).zone
        
        # 2. Find timezone from user settings
        if g.user and g.user['timezone']:
            return pytz.timezone(g.user['timezone']).zone
        
        # 3. Default to UTC
        return app.config['BABEL_DEFAULT_TIMEZONE']
    except UnknownTimeZoneError:
        return app.config['BABEL_DEFAULT_TIMEZONE']
