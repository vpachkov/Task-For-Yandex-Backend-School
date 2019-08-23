from manage import db
from flask import jsonify, request
from validators import validate_import, validate_edit_user
from app import app
from models import Import, User
from serializers import serialize_user_from_model, serialize_users, serialize_birthday_presents_data, serialize_towns_percentile
from citizen_controller import update_users, create_new_import_group

@app.route('/imports', methods=['POST'])
def imports():
    try:
        req = request.json
    except:
        return jsonify({'data': {'error' : 'В выгрузке отсутствуют данные / неверный формат'}}), 400

    res = validate_import(req) # Результат проверки данных

    if res == 'OK': # Введенные данные корректны
        return jsonify({'data': {'import_id' : create_new_import_group(req)}}), 201

    return jsonify({'data': {'error' : res}}), 400

@app.route('/imports/<import_id>/citizens/<citizen_id>', methods=['PATCH'])
def edit_user(import_id, citizen_id):
    # Проверка формата import_id и citizen_id
    try:
        int(import_id)
        int(citizen_id)
    except:
        return jsonify({'data': {'error' : 'В выгрузке отсутствуют данные / неверный формат'}}), 400

    current_import = Import.query.get(import_id) # Поиск нужной выгрузки

    if current_import is None: # Если не удалось найти выгрузку
        return jsonify({'data': {'error' : 'Не удалось найти выгрузку'}}), 400

    user = current_import.users.filter(User.citizen_id == citizen_id).first() # Поиск нужного жителя

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
            relative_object = current_import.users.filter(User.citizen_id == relative).first() # Поиск родственника
            if relative_object is None: # Если родственник не был найден
                return jsonify({'data': {'error' : 'В выгрузке нет родственника с citizen_id = ' + str(relative)}}), 400

        update_users(current_import, user, citizen) # Обновление жителя и его родственников

        return jsonify({'data': serialize_user_from_model(user)}), 200

    return jsonify({'data': {'error' : res}}), 400
        
@app.route('/imports/<import_id>/citizens', methods=['GET'])
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