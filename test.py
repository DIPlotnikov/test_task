from tinydb import TinyDB
from os import path
import requests
import unittest

# for tests

comment_form = {"name": "CommentForm",
                "user_email": "email",
                "user_phone": "phone_number",
                "publication_date": "date",
                "text_field": "text"
                }

order_form = {"name": "OrderForm",
              "user_name": "text",
              "order_date": "date",
              "user_phone": "phone_number"
              }
user_reg = {"name": "UserRegistration",
            "user": 'phone_number'}
test_form_1 = {'name': 'test_form_1', 'A': 'text', 'B': 'text'}
test_form_2 = {'name': 'test_form_2', 'C': 'text', 'B': 'text'}

if not path.exists('db.json'):
    print('--== create test db ==--')
    db = TinyDB('db.json')
    db.insert_multiple([comment_form, order_form, user_reg, test_form_1, test_form_2])
    db.close()


def send_test_post(url, data_dict):
    response = requests.post(url, data=data_dict)
    return response.text.strip()


class TestForms(unittest.TestCase):
    def test_correct_cases(self):
        url = 'http://localhost:5000/get_form'
        self.assertEqual(
            send_test_post(url, {"somekey": "text",
                                 "somephonenum": "+71234567890",
                                 "someemail": "text@mail.ru",
                                 "somedate": '01.01.2023'
                                 }),
            '{"somedate":"date",'
            '"someemail":"email",'
            '"somekey":"text",'
            '"somephonenum":"phone_number"}'
        )
        self.assertEqual(
            send_test_post(url, {"user": "+71234567890"}),
            'UserRegistration'
        )
        self.assertEqual(
            send_test_post(url, {"user_name": "NAME",
                                 "order_date": "2022-03-28",
                                 "user_phone": "89892483408"}),
            'OrderForm'
        )
        self.assertEqual(
            send_test_post(url, {"user_email": "1@sdf.safd",
                                 "user_phone": "+7 999 888 77 66",
                                 "publication_date": "01.11.1111",
                                 "text_field": "some text"}),
            'CommentForm'
        )
        self.assertEqual(
            send_test_post(url, {'A':1, 'B':2, 'C':3}),
            'test_form_1 test_form_2'
        )

    def test_uncorrect_cases(self):
        url = 'http://localhost:5000/get_form'
        self.assertEqual(
            send_test_post(url, {}),
            '{}'
        )
        self.assertEqual(
            send_test_post(url, ''),
            '{}'
        )
        self.assertEqual(
            send_test_post(url, {'key': 987, 456: '64', 'sdf': True, 'sdf2': ''}),
            '{"456":"text","key":"text","sdf":"text","sdf2":"text"}'
        )


if __name__ == '__main__':
    unittest.main()
