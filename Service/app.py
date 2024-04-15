import config

from controller import auth_controller
from controller import eeg_controller
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager
from flask_mongoengine import MongoEngine

app = Flask(__name__)

# MongoDB、Redis 和 Flask-JWT-Extended 配置

config.config(app)
# code 为 0 表示成功，code 为 1 表示失败
db = MongoEngine(app)
jwt = JWTManager(app)

eeg_controller.hrv_controller(app)
auth_controller.authController(app)

# 可用于测试连通性
@app.route("/mental-connect/algorithm/api/test/hello")
def hello():
    return "Hello, Flask!"

if __name__ == '__main__':
    app.run(port=8090)