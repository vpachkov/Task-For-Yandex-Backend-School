import unittest
from serializers import *
from validators import *
from models import User, Import

class TestSerializers(unittest.TestCase):
    def test_serialize_relatives_from_str(self):
        self.assertEqual(serialize_relatives_from_str(''), []) # Empty string
        self.assertEqual(serialize_relatives_from_str('1'), [1])
        self.assertEqual(serialize_relatives_from_str('1 2'), [1, 2])
        self.assertEqual(serialize_relatives_from_str('1211 211221'), [1211, 211221])

    def test_serialize_relatives_from_list(self):
        self.assertEqual(serialize_relatives_from_list([]), '') #Empty list
        self.assertEqual(serialize_relatives_from_list([1]), '1')
        self.assertEqual(serialize_relatives_from_list([1,211]), '1 211') #Empty list

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
    
    def test_check_town_street_building_name(self):
        self.assertTrue(check_town_street_building_name('Льва Толстого'))
        self.assertTrue(check_town_street_building_name('Простоимя'))
        self.assertTrue(check_town_street_building_name('11'))
        self.assertTrue(check_town_street_building_name('Eleven'))
        self.assertFalse(check_town_street_building_name(''))
        self.assertFalse(check_town_street_building_name(' '))
        self.assertFalse(check_town_street_building_name('  '))
        self.assertFalse(check_town_street_building_name(11))
        self.assertFalse(check_town_street_building_name(None))

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
                }
            ]
        }


        #Tests
        self.assertEqual(validate_import(not_enough_keys_json), not_enough_keys)
        self.assertEqual(validate_import(error_in_key_json_1), uncorrect_data)
        self.assertEqual(validate_import(error_in_key_json_2), uncorrect_data)
        self.assertEqual(validate_import(empty_citizens_json), uncorrect_json)
        self.assertEqual(validate_import(correct_json), correct_result)


if __name__ == '__main__':
    unittest.main()