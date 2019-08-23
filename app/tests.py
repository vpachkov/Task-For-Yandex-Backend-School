import unittest
from serializers import *
from validators import *
from utils import *
from models import User, Import

class TestSerializers(unittest.TestCase):
    def test_convert_relatives_from_str_to_list(self):
        self.assertEqual(convert_relatives_from_str_to_list(''), []) # Empty string
        self.assertEqual(convert_relatives_from_str_to_list('1'), [1])
        self.assertEqual(convert_relatives_from_str_to_list('1 2'), [1, 2])
        self.assertEqual(convert_relatives_from_str_to_list('1211 211221'), [1211, 211221])

    def test_convert_relatives_from_list_to_str(self):
        self.assertEqual(convert_relatives_from_list_to_str([]), '') #Empty list
        self.assertEqual(convert_relatives_from_list_to_str([1]), '1')
        self.assertEqual(convert_relatives_from_list_to_str([1,211]), '1 211') #Empty list
    
    def test_serialize_birthday_presents_data(self):
        import_group = Import()
        #citizen_id, town, street, building, apartment, name, birth_date, gender, relatives
        user_1 = User(1,'Москва', 'Улица', '11', 1, 'Имя1', '21.10.1998', 'male', '1 2 3')
        user_2 = User(2,'Москва', 'Улица', '11', 1, 'Имя2', '21.09.1998', 'male', '1')
        user_3 = User(3,'Москва', 'Улица', '11', 1, 'Имя3', '21.11.1998', 'male', '1 2')
        user_4 = User(4,'Москва', 'Улица', '11', 1, 'Имя4', '21.03.1998', 'male', '')
        user_5 = User(5,'Москва', 'Улица', '11', 1, 'Имя5', '21.02.1998', 'male', '6')
        user_6 = User(6,'Москва', 'Улица', '11', 1, 'Имя6', '21.11.1998', 'male', '5 7')
        user_7 = User(7,'Москва', 'Улица', '11', 1, 'Имя7', '21.02.1998', 'male', '6')

        user_1.import_group = import_group
        user_2.import_group = import_group
        user_3.import_group = import_group
        user_4.import_group = import_group
        user_5.import_group = import_group
        user_6.import_group = import_group
        user_7.import_group = import_group

        correct = {
            '1' : [],
            '2' : [
                {
                    'citizen_id' : 6,
                    'presents' : 2
                }
            ],
            '3' : [],
            '4' : [],
            '5' : [],
            '6' : [],
            '7' : [],
            '8' : [],
            '9' : [
                {
                    'citizen_id': 1,
                    'presents': 1
                }
            ],
            '10' : [
                {
                    'citizen_id' : 1,
                    'presents' : 1
                },
                {
                    'citizen_id' : 2,
                    'presents' : 1
                },
                {
                    'citizen_id' : 3,
                    'presents' : 1
                }
            ],
            '11' : [
                {
                    'citizen_id' : 1,
                    'presents' : 1
                },
                {
                    'citizen_id' : 2,
                    'presents' : 1
                },
                {
                    'citizen_id' : 5,
                    'presents' : 1
                },
                {
                    'citizen_id' : 7,
                    'presents' : 1
                }
            ],
            '12' : []
        }
        self.assertEqual(serialize_birthday_presents_data(import_group.users), correct)

class TestValidators(unittest.TestCase):
    #check auxiliary functions in validators
    def test_check_birth_date(self):
        self.assertTrue(check_date('16.10.2001'))
        self.assertTrue(check_date('16.10.0001'))
        self.assertTrue(check_date('01.01.2001'))
        self.assertFalse(check_date('16.13.2001'))
        self.assertFalse(check_date('16.13.0000'))
        self.assertFalse(check_date('46.11.2001'))

    def test_check_gender(self):
        self.assertTrue(check_gender('male'))
        self.assertTrue(check_gender('female'))
        self.assertFalse(check_gender('transformer'))
        self.assertFalse(check_gender(''))
        self.assertFalse(check_gender('  '))
        self.assertFalse(check_gender(0))
        self.assertFalse(check_gender(None))

    def test_check_citizen_id_apartment(self):
        self.assertTrue(check_citizen_id_apartment(21))
        self.assertTrue(check_citizen_id_apartment(1))
        self.assertTrue(check_citizen_id_apartment(101))
        self.assertTrue(check_citizen_id_apartment(0))
        self.assertFalse(check_citizen_id_apartment(-1))
        self.assertFalse(check_citizen_id_apartment(-111))
        self.assertFalse(check_citizen_id_apartment('21'))
        self.assertFalse(check_citizen_id_apartment(None))
    
    def test_check_town_street_building(self):
        self.assertTrue(check_town_street_building('Льва Толстого'))
        self.assertFalse(check_town_street_building(''))
        self.assertFalse(check_town_street_building(' '))
        self.assertFalse(check_town_street_building('  '))
        self.assertFalse(check_town_street_building(11))
        self.assertFalse(check_town_street_building(None))

    def test_check_name(self):
        self.assertTrue(check_name('Простоимя'))
        self.assertTrue(check_name('11'))
        self.assertTrue(check_name('Eleven'))
        self.assertFalse(check_name(''))
        self.assertTrue(check_name('@'))

    def test_check_relatives(self):
        self.assertTrue(check_relatives([1,2,3]))
        self.assertTrue(check_relatives([])) # Empty list
        self.assertFalse(check_relatives(1))
        self.assertFalse(check_relatives(None))

    #check major functions in validators
    def test_validate_import(self):
        uncorrect_json = 'В выгрузке отсутствуют данные / неверный формат'
        not_enough_keys = 'Не хватает данных о пользователе'
        uncorrect_data = 'Ошибка в данных о пользователе'
        correct_result = 'OK'
        self.assertEqual(validate_import(''), uncorrect_json)
        self.assertEqual(validate_import(None), uncorrect_json)
        self.assertEqual(validate_import([]), uncorrect_json)
        self.assertEqual(validate_import([{'haha': 'hahaaha'}]), uncorrect_json)

        #some JSONs
        not_enough_keys_json = {
            "citizens": [
                {
                    "citizen_id": 1,
                    "town": "Москва",
                    "street": "Льва Толстого",
                    "building": "16к7стр5",
                    "apartment": 7,
                    "name": "Иванов Иван Иванович"
                }
            ]
        }

        error_in_key_json_1 = {
            "citizens": [
                {
                    "citizen_id": 1,
                    "town": "Москва",
                    "street": "Льва Толстого",
                    "building": "16к7стр5",
                    "apartment": 7,
                    "name": "Иванов Иван Иванович",
                    "birth_date": "46.12.1986", # Here
                    "gender": "male",
                    "relatives": [2]
                }
            ]
        }

        error_in_key_json_2 = {
            "citizens": [
                {
                    "citizen_id": 2,
                    "town": "Москва",
                    "street": "Льва Толстого",
                    "building": "16к7стр5",
                    "apartment": 7,
                    "name": "Иванов Иван Иванович",
                    "birth_date": "26.12.1986",
                    "gender": "male",
                    "relatives": 'fdd' #Here
                }
            ]
        }

        empty_citizens_json = {
            "citizens": []
        }

        correct_json = {
            "citizens": [
                {
                    "citizen_id": 1,
                    "town": "Москва",
                    "street": "Льва Толстого",
                    "building": "16к7стр5",
                    "apartment": 7,
                    "name": "Иванов Иван Иванович",
                    "birth_date": "26.12.1986",
                    "gender": "male",
                    "relatives": [2]
                },
                {
                    "citizen_id": 2,
                    "town": "Москва",
                    "street": "Льва Толстого",
                    "building": "16к7стр5",
                    "apartment": 7,
                    "name": "Иванов Иван Иван",
                    "birth_date": "26.12.1986",
                    "gender": "male",
                    "relatives": [1]
                }
            ]
        }


        #Tests
        self.assertEqual(validate_import(not_enough_keys_json), not_enough_keys)
        self.assertEqual(validate_import(error_in_key_json_1), uncorrect_data)
        self.assertEqual(validate_import(error_in_key_json_2), uncorrect_data)
        self.assertEqual(validate_import(empty_citizens_json), uncorrect_json)
        self.assertEqual(validate_import(correct_json), correct_result)

    def test_validate_edit_user(self):
        empty_error = 'В запросе должно быть указано хотя бы одно поле'
        extra_error = 'В запросе присутствуют лишние поля'
        key_error = 'Ошибка в данных о пользователе'
        correct_result = 'OK'

        # Some JSONs
        json_with_citizen_id = {
            "citizen_id": 1, #citizen_id is not allowed
            "town": "Москва",
            "street": "Льва Толстого",
            "building": "16к7стр5",
            "apartment": 7,
            "name": "Иванов Иван Иванович",
            "birth_date": "26.12.1986",
            "gender": "male",
            "relatives": [2]
        }

        empty_json_1 = {
            
        }

        extra_error_json = {
            'random_key' : 'random_value'
        }

        key_error_json = {
            "town": "Москва",
            "street": "Льва Толстого",
            "building": "16к7стр5",
            "apartment": 7,
            "name": "", # Here
            "birth_date": "26.12.1986",
            "gender": "male",
            "relatives": [2]
        }

        correct_json = {
            "town": "Москва",
            "street": "Льва Толстого",
            "building": "16к7стр5",
            "apartment": 7,
            "name": "Иванов Иван Иванович",
            "birth_date": "26.12.1986",
            "gender": "male",
            "relatives": [2]
        }
        # Tests

        self.assertEqual(validate_edit_user(json_with_citizen_id), extra_error)
        self.assertEqual(validate_edit_user(empty_json_1), empty_error)
        self.assertEqual(validate_edit_user(extra_error_json), extra_error)
        self.assertEqual(validate_edit_user(key_error_json), key_error)
        self.assertEqual(validate_edit_user(correct_json), correct_result)

class TestUtils(unittest.TestCase):
    def test_erase_citizen_from_relatives(self):
        self.assertEqual(erase_citizen_from_relatives('1 2 3', 1), '2 3')
        self.assertEqual(erase_citizen_from_relatives('1 2 3', 3), '1 2')
        self.assertEqual(erase_citizen_from_relatives('1', 1), '')

    def test_add_citizen_to_relatives(self):
        self.assertEqual(add_citizen_to_relatives('2 3', 1), '2 3 1')
        self.assertEqual(add_citizen_to_relatives('', 1), '1')
        self.assertEqual(add_citizen_to_relatives('1', 3), '1 3')
if __name__ == '__main__':
    unittest.main()