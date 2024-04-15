from config import redis_client

from datetime import timedelta
from entity.AccountIdentity import AccountIdentity
from entity.TokenIdentity import TokenIdentity
from flask import jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from util.token_check import token_check

def authController(app): 
    # 以下为注册及登录接口
    @app.route('/mental-connect/algorithm/api/auth/register', methods=['POST'])
    def register():
        try:
            data = request.get_json()
            accountName = data.get('account')
            if AccountIdentity.objects(account=accountName).first():
                return jsonify(code = 1, message = "The account already exists.")
            accountIdentity = AccountIdentity(
                account=accountName,
                password=data.get('password'),
                role=data.get('role'),
                trueName=data.get('trueName'),
                email=data.get('email'),
                phone=data.get('phone'),
                status=data.get('status'),
                note=data.get('note'),
            )
            accountIdentity.save()
            expires = timedelta(hours=6)
            token = create_access_token(identity=accountIdentity.account, expires_delta=expires)
            tokenIdentity=TokenIdentity(account=accountName, token=token)
            tokenIdentity.save_to_redis(redis_client)
            responseDate = {
                "code": 0,
                "data": {
                    "token": token,
                    "accountIdentity": accountIdentity,
                }
            }
            return jsonify(responseDate)
        except Exception as e:
            return jsonify(code = 1, message=str(e))

    @app.route('/mental-connect/algorithm/api/auth/login', methods=['POST'])
    def login():
        data = request.get_json()
        account = AccountIdentity.objects(account=data.get('account')).first()
        if account is None:
            return jsonify(code=1, message="The account does not exist.")
        if account.password != data.get("password"):
            return jsonify(code=1, message="The password is wrong.")
        else:
            # 先删除旧的token, 不仅在登录时需要删除旧的token,在修改密码等操作后也要删除旧的token
            pattern = f"token:{account}:*"
            for token_key in redis_client.scan_iter(pattern):
                redis_client.delete(token_key)
            # 生成新的token
            expires = timedelta(hours=6)
            token = create_access_token(identity=account.account, expires_delta=expires)
            tokenIdentity=TokenIdentity(account=account.account, token=token)
            tokenIdentity.save_to_redis(redis_client)
            responseDate = {
                "code": 0,
                "data": {
                    "token": token,
                    "accountIdentity": account,
                }
            }
            return jsonify(responseDate)
        
    # 用于测试token校验，@tokenCheck和@jwt_required()必须要有
    @app.route('/mental-connect/algorithm/api/test/helloWithToken', methods=['GET'])
    @token_check
    @jwt_required()
    def helloWithToken():
        accountName = get_jwt_identity()
        account = AccountIdentity.objects(account=accountName).first()
        if account is None:
            return jsonify(code=1, message="The account does not exist.")
        responseDate = {
            "code": 0,
            "data": {
                "message": "hello",
                "accountIdentity": account,
            }
        }
        return jsonify(responseDate)