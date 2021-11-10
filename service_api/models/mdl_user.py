import uuid
from pytz import timezone
from datetime import datetime
from service_api.extensions import db,  pwd_context
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_property


UTC = timezone('Asia/Almaty')


def time_now():
    return datetime.now(UTC)


class TblUser(db.Model):

    __tablename__ = 'tbl_user'

    user_id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid.uuid4)
    user_name = db.Column(db.String, nullable=False)
    _password = db.Column("password", db.String(255))
    created_at = db.Column(db.DateTime(timezone=True, ), default=time_now)
    updated_at = db.Column(db.DateTime(timezone=True, ), default=time_now, onupdate=time_now)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = pwd_context.hash(value)

    def __repr__(self):
        return f'user_name: {self.user_name}'


