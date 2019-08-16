from manage import db
from flask import jsonify, request
from validators import validate_import
from app import app

@app.route('/imports', methods=['POST'])
def imports():
    citizens = request.json['citizens']
    res = validate_import(citizens)
    return jsonify({'result' : res})