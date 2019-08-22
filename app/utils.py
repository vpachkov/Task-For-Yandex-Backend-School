from datetime import date

def calculate_age(citizen_birth_date):
    today = date.today()
    parsed_citizen_birth_date = citizen_birth_date.split('.')
    born = date(int(parsed_citizen_birth_date[2]), int(parsed_citizen_birth_date[1]), int(parsed_citizen_birth_date[0]))
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def erase_citizen_from_relatives(relatives, citizen_id):
    relatives = relatives.split()
    relatives.remove(str(citizen_id))
    if len(relatives) == 0:
        relatives = ''
    else:
        relatives = ' '.join(relative for relative in relatives)
    return relatives

def add_citizen_to_relatives(relatives, citizen_id):
    return relatives + ' ' + citizen_id