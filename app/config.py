import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    TESTING=True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Should_I!really09Care?'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
            'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY') or 'public'
    RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY') or 'private'
    RECAPTCHA_OPTIONS = {'theme': 'white'}
    UPLOAD_EXTENSIONS = ['.md']
