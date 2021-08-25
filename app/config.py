import os

try:
    print("trying dotenv...")
    from dotenv import load_dotenv
    load_dotenv()
    print("dotenv loaded")
    print(os.environ.get('DATABASE_URL'))
except:
    pass

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Should_I!really09Care?'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_EXTENSIONS = ['.md']
