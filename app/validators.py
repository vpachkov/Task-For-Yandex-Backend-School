from datetime import date
from flask import jsonify, request

# Функция проверки формата даты

def check_date(dt):
    try:
        parsed_dt = dt.split('.')
        date(int(parsed_dt[2]), int(parsed_dt[1]), int(parsed_dt[0]))
        return True
    except:
        return False

# Функция проверки идентификатора жителя и номера квартиры

def check_citizen_id_apartment(data):
    if type(data) == int:
        if data < 0:
            return False
    else:
        return False

    return True

# Функция проверки города, улицы и дома 

def check_town_street_building(data):
    if type(data) == str:
        if len(data) == 0:
            return False
        if len(data) > 256:
            return False
        for symb in data:
            if symb.isalpha() or symb.isdigit():
                return True
        return False

    else:
        return False

    return True

# Функция проверки имени

def check_name(data):
    if type(data) == str:
        if len(data) == 0:
            return False
        if len(data) > 256:
            return False
    else:
        return False

    return True

# Функция проверки даты рождения

def check_birth_date(data):
    if type(data) == str:
        if len(data) == 0:
            return False
        if not check_date(data):
            return False
    else:
        return False

    return True

# Функция проверки пола

def check_gender(data):
    if type(data) == str:
        if not (data == 'male' or data == 'female'):
            return False
    else:
        return False

    return True

# Функция проверки списка родственников

def check_relatives(data):
    if not (type(data) == list):
        return False

    return True

key_to_func = {
        'town' : check_town_street_building,
        'street': check_town_street_building,
        'building': check_town_street_building,
        'name': check_name,
        'apartment': check_citizen_id_apartment,
        'citizen_id': check_citizen_id_apartment,
        'birth_date': check_birth_date,
        'gender': check_gender,
        'relatives': check_relatives,
}

def validate_import(req):

    if not(type(req) is dict) or not ('citizens' in req.keys()): # Проверка на пустой список
        return 'В выгрузке отсутствуют данные / неверный формат'

    citizens = req['citizens']

    if not (type(citizens) is list):
        return 'В выгрузке отсутствуют данные / неверный формат'

    if len(citizens) == 0: # Проверка на пустой список
        return 'В выгрузке отсутствуют данные / неверный формат'

    required_keys = ["citizen_id", "town", "street", "building", "apartment", "name", "birth_date", "gender", "relatives"] # Обязательные ключи

    check_relatives = {}
    for citizen in citizens:

        # Проверка наличия ключей
    
        citizen_keys = set(citizen.keys())
        if not all(element in citizen_keys  for element in required_keys):
            return 'Не хватает данных о пользователе'
        
        # Проверка всех полей

        for key in citizen.keys():
            if not key_to_func[key](citizen[key]):
                return 'Ошибка в данных о пользователе'
        
        # Проверка двухсторонних связей
        
        if not (citizen['citizen_id'] in check_relatives.keys()):
            check_relatives[citizen['citizen_id']] = len(set(citizen['relatives']))
        else:
            check_relatives[citizen['citizen_id']] += len(set(citizen['relatives']))
        
        for relative in set(citizen['relatives']):
            if not (relative in check_relatives.keys()):
                check_relatives[relative] = -1
            else:
                check_relatives[relative] -= 1
        
        
    for key, value in check_relatives.items():
        if value != 0:
            return 'Ошибка в данных о пользователе'
            
    return 'OK' # OK, если ошибки в запросе не были найдены

def validate_edit_user(citizen):

    #Проверка на пустоту

    if len(citizen) == 0:
        return 'В запросе должно быть указано хотя бы одно поле'
    
    allowed_keys = {"town", "street", "building", "apartment", "name", "birth_date", "gender", "relatives"} # Разрешенные ключи
    for key in citizen.keys():
        if not key in allowed_keys:
            return 'В запросе присутствуют лишние поля'

        # Проверка поля на корректность

        if not key_to_func[key](citizen[key]):
            return 'Ошибка в данных о пользователе'
    
    return 'OK' # OK, если ошибки в запросе не были найдены
        


    

   
        

