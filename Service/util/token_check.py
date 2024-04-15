from flask import request, jsonify
from functools import wraps
from redis import Redis

def token_check(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')[7:]
        if not token:
            return jsonify({'code':1, 'message': 'Token is missing!'}), 403
        redis_client = Redis(host='112.124.48.213', port=6379, db=1, password="313521996")
        # 从Redis中检查Token
        token_data = redis_client.hgetall(f"token:{token}")
        if not token_data:
            return jsonify({'message': 'Token is invalid!'}), 403
        return f(*args, **kwargs)
    return decorated_function