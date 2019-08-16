from manage import db
from flask import jsonify, request
from validators import validate_import, validate_edit_user
from app import app
from models import Import, User
from serializers import serialize_user

@app.route('/imports', methods=['POST'])
def imports():
    citizens = request.json['citizens']
    res = validate_import(citizens)
    if res == 'OK':
        imp = Import()
        db.session.add(imp)
        #["citizen_id", "town", "street", "building", "apartment", "name", "birth_date", "gender", "relatives"]
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

        return jsonify({'data': {'import_id' : imp.id}}), 201


    return jsonify({'data': {'error' : res}}), 400

@app.route('/imports/<import_id>/citizens/<citizen_id>', methods=['PATCH'])
def edit_user(import_id, citizen_id):

    current_import = Import.query.get(import_id).users # Поиск нужной выгрузки
    user = current_import.filter(User.citizen_id == citizen_id).first() # Поиск нужного жителя

    if user is None: # Если не удалось найти жителя
        return jsonify({'data': {'error' : 'Житель не был найден'}}), 404

    citizen = request.json # Информация о жителе
    res = validate_edit_user(citizen) # Результат проверки данных

    if res == 'OK':
        # Проверка на наличие родственников в выгрузке
        for relative in citizen['relatives']:
            relative_object = current_import.filter(User.citizen_id == relative).first() #Поиск родственника
            if relative_object is None: # Если родственник не был найден
                return jsonify({'data': {'error' : 'В выгрузке нет родственника с citizen_id = ' + str(relative)}}), 400
        old_relatives = set(user.relatives.split()) # Родственники до изменения
        new_relatives = set(str(item) for item in citizen['relatives']) # Родственники после изменения

        erase_citizen_from = old_relatives - new_relatives # Set из удаленных родственников
        add_citizen_to = new_relatives - old_relatives # Set из новых родственников

        for relative in erase_citizen_from:

            relative_object = current_import.filter(User.citizen_id == relative).first()
            temp = relative_object.relatives
            print(temp)
            temp = temp.split()
            temp.remove(str(citizen_id))
            if len(temp) == 0:
                temp = ''
            else:
                temp = ' '.join(vl for vl in temp)

            relative_object.relatives = temp
        
        for relative in add_citizen_to:
            relative_object = current_import.filter(User.citizen_id == relative).first()
            temp = relative_object.relatives
            temp += (' ' + citizen_id)

            relative_object.relatives = temp
        
        relatives = ' '.join(str(item) for item in citizen['relatives'])
        user.relatives = relatives

        for key in citizen:
            if key == 'name':
                user.name = citizen['name']
            elif key == 'gender':
                user.gender = citizen['gender']
            elif key == 'birth_date':
                user.birth_date = citizen['birth_date']
            elif key == 'town':
                user.town = citizen['town']
            elif key == 'street':
                user.street = citizen['street']
            elif key == 'building':
                user.building = citizen['building']
            elif key == 'apartment':
                user.apartment = citizen['apartment']
            
        db.session.commit()

        return jsonify({'data': serialize_user(user)}), 200

    return jsonify({'data': {'error' : res}}), 400
        
        
