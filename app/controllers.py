from manage import db
from flask import jsonify, request
from validators import validate_import
from app import app
from models import Import, User

@app.route('/imports', methods=['POST'])
def imports():
    citizens = request.json['citizens']
    res = validate_import(citizens)
    if res == 'OK':
        imp = Import()
        db.session.add(imp)
        ["citizen_id", "town", "street", "building", "apartment", "name", "birth_date", "gender", "relatives"]
        for citizen in citizens:

            #Collect data

            citizen_id = citizen['citizen_id']
            town = citizen['town']
            street = citizen['street']
            building = citizen['building']
            apartment = citizen['apartment']
            name = citizen['name']
            birth_date = citizen['birth_date']
            gender = citizen['gender']
            relatives = citizen['relatives']
            relatives = ' '.join(str(item) for item in relatives)
            new_user = User(citizen_id, town, street, building, apartment, name, birth_date, gender, relatives)
            new_user.import_group = imp
            db.session.add(new_user)
        db.session.commit()


    return jsonify({'result' : res})