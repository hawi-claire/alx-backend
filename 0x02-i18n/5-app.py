#!/usr/bin/env python3
"""Flask app with user login and internationalization"""
from flask import Flask, render_template, request, g
from flask_babel import Babel, gettext


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
        return users.get(int(user_id))
    return None


@app.before_request
def before_request():
    """Set user as global on flask.g.user"""
    g.user = get_user()


@babel.localeselector
def get_locale():
    """Determine the best match for supported languages"""
    # Check if locale parameter is in request
    locale = request.args.get('locale')
    if locale and locale in app.config['LANGUAGES']:
        return locale
    # Otherwise use the best match from accept-language header
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index():
    """Route for the home page"""
    return render_template('5-index.html')


if __name__ == '__main__':
    app.run(debug=True)
