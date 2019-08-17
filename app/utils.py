from datetime import date

def calculate_age(citizen_birth_date):
    today = date.today()
    parsed_citizen_birth_date = citizen_birth_date.split('.')
    born = date(int(parsed_citizen_birth_date[2]), int(parsed_citizen_birth_date[1]), int(parsed_citizen_birth_date[0]))
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))