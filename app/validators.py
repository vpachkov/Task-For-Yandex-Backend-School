from datetime import date

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

# Функция проверки города, улицы, дома и имени 

def check_town_street_building_name(data):
    if type(data) == str:
        if len(data) == 0:
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
        'town' : check_town_street_building_name,
        'street': check_town_street_building_name,
        'building': check_town_street_building_name,
        'name': check_town_street_building_name,
        'apartment': check_citizen_id_apartment,
        'citizen_id': check_citizen_id_apartment,
        'birth_date': check_birth_date,
        'gender': check_gender,
        'relatives': check_relatives,
}

def validate_import(citizens):
    if len(citizens) == 0:
        return 'В выгрузке отсутствуют данные' # Проверка на пустой список

    required_keys = ["citizen_id", "town", "street", "building", "apartment", "name", "birth_date", "gender", "relatives"] # Обязательные ключи

    for citizen in citizens:

        # Проверка наличия ключей
    
        citizen_keys = set(citizen.keys())
        if not all(element in citizen_keys  for element in required_keys):
            return 'Не хватает данных о пользователе'
        
        # Проверка всех полей

        for key in citizen.keys():
            if not key_to_func[key](citizen[key]):
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
        


    

   
        

