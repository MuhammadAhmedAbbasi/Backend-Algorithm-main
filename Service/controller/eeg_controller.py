import json

from flask import jsonify, request
from service import eeg_service
from util.token_check import token_check

def hrv_controller(app):
    @app.route('/mental-connect/algorithm/api/eeg/depression', methods=['POST'])
    def depression():
        try:
            data = request.get_json()
            eeg_datas = data.get('hrv')
            ans = eeg_service.eeg_depression(eeg_datas)
            tensor_list = ans.tolist()
            json_data = json.dumps(tensor_list)
            responseDate = {
                "code": 0,
                "data": json_data
            }
            return jsonify(responseDate)
        except Exception as e:
            return jsonify(code = 1, message=str(e))