from manage import db
from flask import jsonify, request
from validators import validate_import, validate_edit_user
from app import app
from models import Import, User
from serializers import serialize_user_from_model, serialize_users, serialize_user_from_json, serialize_birthday_presents_data, serialize_towns_percentile

@app.route('/imports', methods=['POST'])
def imports():
    try:
        req = request.json
    except:
        return jsonify({'data': {'error' : 'В выгрузке отсутствуют данные / неверный формат'}}), 400

    res = validate_import(req) # Результат проверки данных

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
    # Проверка формата import_id и citizen_id
    try:
        int(import_id)
        int(citizen_id)
    except:
        return jsonify({'data': {'error' : 'В выгрузке отсутствуют данные / неверный формат'}}), 400

    current_import = Import.query.get(import_id).users # Поиск нужной выгрузки
    user = current_import.filter(User.citizen_id == citizen_id).first() # Поиск нужного жителя

    if user is None: # Если не удалось найти жителя
        return jsonify({'data': {'error' : 'Житель не был найден'}}), 400
    try:
        citizen = request.json # Информация о жителе
    except:
        return jsonify({'data': {'error' : 'В выгрузке отсутствуют данные / неверный формат'}}), 400

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
        citizen['relatives'] = relatives

        for key, value in citizen.items():
            setattr(user, key, value) # Обновление полей жителя
            
        db.session.commit()

        return jsonify({'data': serialize_user_from_model(user)}), 200

    return jsonify({'data': {'error' : res}}), 400
        
@app.route('/imports/<import_id>/citizens/', methods=['GET'])
def show_all_citizens(import_id):
    # Проверка формата import_id
    try:
        int(import_id)
    except:
        return jsonify({'data': {'error' : 'Неверный формат import_id'}}), 400

    current_import = Import.query.get(import_id) # Поиск нужной выгрузки

    if current_import is None: # Если не удалось найти выгрузку
        return jsonify({'data': {'error' : 'Не удалось найти выгрузку'}}), 400

    result = serialize_users(current_import.users)

    return jsonify({'data':result}), 200

@app.route('/imports/<import_id>/citizens/birthdays', methods=['GET'])
def show_presents(import_id):
    # Проверка формата import_id
    try:
        int(import_id)
    except:
        return jsonify({'data': {'error' : 'Неверный формат import_id'}}), 400

    current_import = Import.query.get(import_id) # Поиск нужной выгрузки

    if current_import is None: # Если не удалось найти выгрузку
        return jsonify({'data': {'error' : 'Не удалось найти выгрузку'}}), 400

    result = serialize_birthday_presents_data(current_import.users)

    return jsonify({'data' : result}), 200

@app.route('/imports/<import_id>/towns/stat/percentile/age', methods=['GET'])
def show_towns_percentile(import_id):
    # Проверка формата import_id
    try:
        int(import_id)
    except:
        return jsonify({'data': {'error' : 'Неверный формат import_id'}}), 400

    current_import = Import.query.get(import_id) # Поиск нужной выгрузки

    if current_import is None: # Если не удалось найти выгрузку
        return jsonify({'data': {'error' : 'Не удалось найти выгрузку'}}), 400

    result = serialize_towns_percentile(current_import.users)
    
    return jsonify({'data' : result}), 200