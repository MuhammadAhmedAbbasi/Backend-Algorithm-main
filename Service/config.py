import os
from redis import Redis

# 连接字符串
databaseHost = 'mongodb://mdd:313521996@112.124.48.213:27017/flask?authSource=admin'
# redis连接配置
redis_host = '112.124.48.213'
redis_port = 6379
redis_db = 1
redis_password = 313521996
# 认证字符串
jwt_secret_key = '404E635266556A586E3272357538782F413F4428472B4B6250645367566B5970'

redis_client = Redis(host=redis_host, port=redis_port, db=redis_db, password=redis_password)

service_folder = os.path.dirname(__file__)
project_folder = os.path.dirname(service_folder)

def config(app):
    mongodb_config = {
    'db': 'flask',
    'host': databaseHost
    }

    # MongoDB、Redis 和 Flask-JWT-Extended 配置
    app.config['MONGODB_SETTINGS'] = mongodb_config
    app.config['JWT_SECRET_KEY'] = jwt_secret_key