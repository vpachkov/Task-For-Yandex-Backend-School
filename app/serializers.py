from models import Import, User
from utils import calculate_age
from numpy import array, percentile
from utils import convert_relatives_from_list_to_str, convert_relatives_from_str_to_list

def serialize_user_from_model(user):
    result = {}
    result['citizen_id'] = user.citizen_id
    result['town'] = user.town
    result['street'] = user.street
    result['building'] = user.building
    result['apartment'] = user.apartment
    result['name'] = user.name
    result['birth_date'] = user.birth_date
    result['gender'] = user.gender
    result['relatives'] = convert_relatives_from_str_to_list(user.relatives)
    return result

def serialize_users(import_group):
    result = []
    for user in import_group:
        result.append(serialize_user_from_model(user))
    return result

def serialize_user_from_json(citizen):
    citizen_id = citizen['citizen_id']
    town = citizen['town']
    street = citizen['street']
    building = citizen['building']
    apartment = citizen['apartment']
    name = citizen['name']
    birth_date = citizen['birth_date']
    gender = citizen['gender']
    relatives = convert_relatives_from_list_to_str(citizen['relatives'])
    return User(citizen_id, town, street, building, apartment, name, birth_date, gender, relatives)

def serialize_birthday_presents_data(import_group):
    dt = {}
    for i in range(1,13):
        dt[i] = {}
    
    for citizen in import_group:
        citizen_birth_month = int(citizen.birth_date.split('.')[1])
        citizen_relatives = convert_relatives_from_str_to_list(citizen.relatives)
        for relative in citizen_relatives:
            if not (relative in dt[citizen_birth_month].keys()):
                dt[citizen_birth_month][relative] = 1
            else:
                dt[citizen_birth_month][relative] += 1
    
    result = {}

    for month in dt.keys():
        str_month = str(month)
        result[str_month] = []
        for citizen in dt[month].keys():
            result[str_month].append(
                {
                    'citizen_id' : citizen,
                    'presents' : dt[month][citizen]
                }
            )

    return result

def serialize_towns_percentile(import_group):
    towns = {}

    for citizen in import_group:
        citizen_town = citizen.town
        citizen_age = calculate_age(citizen.birth_date)
        if not (citizen_town in towns.keys()):
            towns[citizen_town] = []
        towns[citizen_town].append(citizen_age)
    
    result = []
    for town in towns.keys():
        new_stat = {}
        np_ages = array(towns[town])
        new_stat['town'] = town
        new_stat['p50'] = round(percentile(np_ages, 50, interpolation='linear'), 2)
        new_stat['p75'] = round(percentile(np_ages, 75, interpolation='linear'), 2)
        new_stat['p99'] = round(percentile(np_ages, 99, interpolation='linear'), 2)
        result.append(new_stat)
    return result