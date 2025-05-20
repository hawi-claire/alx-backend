#!/usr/bin/env python3
"""Flask app with force locale from URL parameter"""
from flask import Flask, render_template, request
from flask_babel import Babel, gettext


class Config:
    """Config class for Flask app"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


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
    return render_template('4-index.html')


if __name__ == '__main__':
    app.run(debug=True)
