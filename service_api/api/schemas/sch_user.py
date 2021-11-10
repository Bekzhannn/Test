from service_api.extensions import ma, db
from service_api.models import TblUser


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TblUser
        sqla_session = db.session
        load_instance = True
        ordered = True
