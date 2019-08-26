from models import Import, User
from database import db
from serializers import serialize_user_from_json
from utils import *

def update_users(current_import, user, citizen):
    old_relatives = set(convert_relatives_from_str_to_list(user.relatives)) # Родственники до изменения
    new_relatives = set(citizen['relatives']) # Родственники после изменения

    erase_citizen_from = old_relatives - new_relatives # Set из удаленных родственников
    add_citizen_to = new_relatives - old_relatives # Set из новых родственников

    all_relatives_list = list(erase_citizen_from.union(add_citizen_to)) # Список citizen_id всех родственников, к которым надо обратиться
    
    all_relatives_objects_list = current_import.users.filter(User.citizen_id.in_(all_relatives_list)).all() # Список объектов всех родственников, к которым надо обратиться

    if len(all_relatives_list) != len(all_relatives_objects_list): # Если какой-то из родственников не был найден
        return False

    for relative_object in all_relatives_objects_list:
        if relative_object.citizen_id in erase_citizen_from:
            relative_object.relatives = erase_citizen_from_relatives(relative_object.relatives, user.citizen_id) # Удаление жителя у его бывшего родственника
        else:
            relative_object.relatives = add_citizen_to_relatives(relative_object.relatives, user.citizen_id) # Добавление жителя к новому родственнику

    citizen['relatives'] = convert_relatives_from_list_to_str(citizen['relatives']) # Добавление новых родственников жителю

    for key, value in citizen.items():
        setattr(user, key, value) # Обновление полей жителя
        
    db.session.commit()

    return True

def create_new_import_group(req):
    imp = Import() # Объект выгрузки
    db.session.add(imp) # Добавление выгрузки в БД
    db.session.commit()

    citizens = req['citizens']

    for citizen in citizens:
        new_user = serialize_user_from_json(citizen) # Создание жителя из JSON
        new_user.import_group = imp # Добавление жителя в выгрузку
        db.session.add(new_user) # Добавление жителя в БД

    db.session.commit()

    return imp.id