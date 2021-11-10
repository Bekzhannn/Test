from flask import Flask, request, jsonify, make_response
from flask_restful import Resource
import jwt
import datetime
from service_api.extensions import db, pwd_context
from service_api.models import TblUser
from service_api.api.schemas import UserSchema
from service_api.commons.pagination import paginate
from service_api.config import SECRET_KEY


class UserResource(Resource):
    def get(self):
        user_id = request.args.get('user_id')

        if user_id:
            user = db.session.query(TblUser).get_or_404(user_id)

            return {'user': UserSchema().dump(user)}, 200

        return paginate(db.session.query(TblUser), UserSchema(many=True)), 200

    def post(self):
        schema = UserSchema()
        user_name = request.json.get("user_name", None)
        password = request.json.get("password", None)
        obj_result = TblUser(
            user_name=user_name
        )
        obj_result.password = password
        db.session.add(obj_result)
        db.session.commit()

        return {
            'msg': 'user created',
            'user': schema.dump(obj_result)
        }, 200

    def put(self):
        user_id = request.args.get('user_id')
        user = db.session.query(TblUser).filter_by(user_id=user_id).first()

        schema = UserSchema(partial=True)
        result = schema.load(request.json, instance=user)
        db.session.commit()

        return {
           'msg': 'user updated',
           'user': schema.dump(result)
        }, 200

    def delete(self):
        user_id = request.args.get('user_id')
        user = db.session.query(TblUser).filter_by(user_id=user_id).first()
        db.session.delete(user)
        db.session.commit()

        return {'msg': 'user deleted'}, 200

class UserToken(Resource):
    def post(self):
        username = request.json.get("user_name", None)
        password = request.json.get("password", None)
        if not username or not password:
            return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

        user = TblUser.query.filter_by(user_name=username).first()

        if not user:
            return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
        if pwd_context.verify(password, user.password):
            token = jwt.encode(
                 {'public_id': str(user.user_id), 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, SECRET_KEY)
            return {'token': token}, 200

        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

