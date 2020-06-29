import os

from flask import Flask
from flask_migrate import Migrate

from models import db, User, Meal, Category, Order


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.secret_key = os.environ.get("SECRET_KEY")


app.app_context().push()
db.init_app(app)
migrate = Migrate(app, db)


from views import *


if __name__ == "__main__":
    app.run(debug=True)

