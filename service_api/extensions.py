from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from passlib.context import CryptContext

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

