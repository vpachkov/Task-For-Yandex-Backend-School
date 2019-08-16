
def serialize_user(user):
    result = {}
    result['citizen_id'] = user.citizen_id
    result['town'] = user.town
    result['street'] = user.street
    result['building'] = user.building
    result['apartment'] = user.apartment
    result['name'] = user.name
    result['birth_date'] = user.birth_date
    result['gender'] = user.gender
    result['relatives'] = [int(item) for item in user.relatives.split()]

    return result