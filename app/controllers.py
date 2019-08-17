from manage import db
from flask import jsonify, request
from validators import validate_import, validate_edit_user
from app import app
from models import Import, User
from serializers import serialize_user_from_model, serialize_users, serialize_user_from_json, serialize_birthday_presents_data, serialize_towns_percentile

@app.route('/imports', methods=['POST'])
def imports():
    res = validate_import(request.json) # Результат проверки данных

    if res == 'OK': # Введенные данные корректны

        imp = Import() # Объект выгрузки
        db.session.add(imp) # Добавление выгрузки в БД
        db.session.commit()
        citizens = request.json['citizens']
        for citizen in citizens:

            new_user = serialize_user_from_json(citizen) # Создание жителя из JSON
            new_user.import_group = imp # Добавление жителя в выгрузку
            db.session.add(new_user) # Добавление жителя в БД

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
            relative_object = current_import.filter(User.citizen_id == relative).first() # Поиск родственника
            if relative_object is None: # Если родственник не был найден
                return jsonify({'data': {'error' : 'В выгрузке нет родственника с citizen_id = ' + str(relative)}}), 400

        old_relatives = set(user.relatives.split()) # Родственники до изменения
        new_relatives = set(str(item) for item in citizen['relatives']) # Родственники после изменения

        erase_citizen_from = old_relatives - new_relatives # Set из удаленных родственников
        add_citizen_to = new_relatives - old_relatives # Set из новых родственников

        for relative in erase_citizen_from:

            relative_object = current_import.filter(User.citizen_id == relative).first() # Поиск родственника в выгрузке

            # Удаление жителя из списка его бывших родственников

            temp = relative_object.relatives
            temp = temp.split()
            temp.remove(str(citizen_id))
            if len(temp) == 0:
                temp = ''
            else:
                temp = ' '.join(vl for vl in temp)

            relative_object.relatives = temp
        
        for relative in add_citizen_to:

            relative_object = current_import.filter(User.citizen_id == relative).first() # Поиск родственника в выгрузке

            # Добавление жителя к новым родственникам

            temp = relative_object.relatives 
            temp += (' ' + citizen_id)
            relative_object.relatives = temp
        
        # Добавление новых родственников жителю

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

        return jsonify({'data': serialize_user_from_model(user)}), 200

    return jsonify({'data': {'error' : res}}), 400
        
@app.route('/imports/<import_id>/citizens/', methods=['GET'])
def show_all_citizens(import_id):

    current_import = Import.query.get(import_id).users # Поиск нужной выгрузки

    if current_import is None: # Если не удалось найти выгрузку
        return jsonify({'data': {'error' : 'Не удалось найти выгрузку'}}), 404

    result = serialize_users(current_import)

    return jsonify({'data':result}), 200

@app.route('/imports/<import_id>/citizens/birthdays', methods=['GET'])
def show_presents(import_id):
    current_import = Import.query.get(import_id).users # Поиск нужной выгрузки

    if current_import is None: # Если не удалось найти выгрузку
        return jsonify({'data': {'error' : 'Не удалось найти выгрузку'}}), 404

    result = serialize_birthday_presents_data(current_import)

    return jsonify({'data' : result}), 200

@app.route('/imports/<import_id>/towns/percentile/age', methods=['GET'])
def show_towns_percentile(import_id):
    current_import = Import.query.get(import_id).users # Поиск нужной выгрузки

    if current_import is None: # Если не удалось найти выгрузку
        return jsonify({'data': {'error' : 'Не удалось найти выгрузку'}}), 404

    result = serialize_towns_percentile(current_import)
    
    return jsonify({'data' : result}), 200