from datetime import date


def check_date(dt):
    try:
        parsed_dt = dt.split('.')
        date(int(parsed_dt[2]), int(parsed_dt[1]), int(parsed_dt[0]))
        return True
    except:
        return False

def validate_import(citizens):
    #Проверка на пустой список

    if len(citizens) == 0:
        return 'Нет данных'
    required_keys = ["citizen_id", "town", "street", "building", "apartment", "name", "birth_date", "gender", "relatives"]
    for citizen in citizens:

        #Проверка наличия ключей
    
        citizen_keys = set(citizen.keys())
        if not all(element in citizen_keys  for element in required_keys):
            return 'Не хватает данных о пользователе'

        #Проверка идентификатора жителя

        if type(citizen['citizen_id']) == int:
            if citizen['citizen_id'] < 0:
                return 'Ошибка в данных о пользователе'
        else:
            return 'Ошибка в данных о пользователе'
        
        #Проверка города

        if type(citizen['town']) == str:
            if len(citizen['town']) == 0:
                return 'Ошибка в данных о пользователе'
        else:
            return 'Ошибка в данных о пользователе'

        #Проверка улицы

        if type(citizen['street']) == str:
            if len(citizen['street']) == 0:
                return 'Ошибка в данных о пользователе'
        else:
            return 'Ошибка в данных о пользователе'

        #Проверка дома

        if type(citizen['building']) == str:
            if len(citizen['building']) == 0:
                return 'Ошибка в данных о пользователе'
        else:
            return 'Ошибка в данных о пользователе'

        #Проверка номера квартиры

        if type(citizen['apartment']) == int:
            if citizen['apartment'] < 0:
                return 'Ошибка в данных о пользователе'
        else:
            return 'Ошибка в данных о пользователе'

        #Проверка имени
        
        if type(citizen['name']) == str:
            if len(citizen['name']) == 0:
                return 'Ошибка в данных о пользователе'
        else:
            return 'Ошибка в данных о пользователе'
        
        #Проверка даты рождения
        
        if type(citizen['birth_date']) == str:
            if len(citizen['birth_date']) == 0:
                return 'Ошибка в данных о пользователе'
            if not check_date(citizen['birth_date']):
                return 'Ошибка в данных о пользователе'
        else:
            return 'Ошибка в данных о пользователе'

        #Проверка пола
        
        if type(citizen['gender']) == str:
            if not (citizen['gender'] == 'male' or citizen['gender'] == 'female'):
                return 'Ошибка в данных о пользователе'
        else:
            return 'Ошибка в данных о пользователе'
        
        #Проверка родственников

        if not (type(citizen['relatives']) == list):
            return 'Ошибка в данных о пользователе'
    
    return 'OK'

        
        

