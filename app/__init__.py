from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flaskext.markdown import Markdown
from flask_login import LoginManager

from app.config import Config

app = Flask(__name__)
conf = Config
print(conf['SQLALCHEMY_DATABASE_URI'])
app.config.from_object(conf)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
markdown = Markdown(app)
login = LoginManager(app)
login.login_view = 'login'

from app import models
from app import routes