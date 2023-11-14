import re
from datetime import datetime
from tinydb import TinyDB, Query
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/data', methods=['POST'])
def receive_data():
    data = request.form
    print(data)
    print('='*10)
    print(jsonify(data))
    return jsonify(data)


comment_form = {"user_email": "email",
                "user_phone": "phone_number",
                "publication _date": "date",
                "text_field": "text"
                }

order_form = {
    "user_name": "text",
    "order_date": "date",
    "user_phone": "phone"
}


def email_adress_is_valid(email: str):
    """ pattern: sometext@yandex.ru """
    pattern = r'\w+@\w+\.\w+'
    result = re.fullmatch(pattern, email)
    return bool(result)


def phone_num_is_valid(num: str):
    """ pattern: +7 xxx xxx xx xx (x - int)"""
    pattern = r'\+7 \d{3} \d{3} \d{2} \d{2}'
    result = re.fullmatch(pattern, num)
    return bool(result)


def date_is_valid(date_str: str):
    """pattern: DD.MM.YYYY or YYYY-MM-DD"""
    try:
        if '.' in date_str:
            date = datetime.strptime(date_str, '%d.%m.%Y')
        else:
            date = datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except:
        return False


def text_is_valid(text: str):
    return isinstance(text, str)


def get_data_type(data: str):
    """
    Return of the types: email, phone_number, date or text.
    If type is unsupported, return 'unsupported type'
    """
    try:
        if date_is_valid(data):
            return 'date'
        elif phone_num_is_valid(data):
            return 'phone_number'
        elif email_adress_is_valid(data):
            return 'email'
        elif text_is_valid(data):
            return 'text'
        else:
            raise Exception
    except:
        return 'unsupported type'


def template_is_valid(form: dict, template: dict):
    for key in template.keys():
        if key == "name":
            continue
        if key not in form or template[key] != form[key]:
            return False
    return True


def get_suitable_form_template(form):
    db = TinyDB('db.json')

    # primary search - If all the passed fields are included in the form template
    templates = db.search(Query().fragment(form))

    # secondary search - If there are more fields passed than the fields in the form template (exceptional case)
    if not templates:
        templates = db.all()

    result = []
    for template in templates:
        if template_is_valid(form, template):
            result.append(template['name'])
    return result




#post = {"user": "phone_number", "user_name": "text", "order_date": "date", "user_phone": "phone_number"}
#print(get_suitable_form_template(post))
# print(email_adress_validation('som123etext@ya.com'))
# print(phone_num_validation('+7 982 248 34 08'))
# print(date_validation('2023-02-01'))
# print(text_validation("123"))
if __name__ == '__main__':
    app.run()
# print(get_data_type(True))
# dict1 = {'name': 'John', 'age': 30, 'city': 'New York'}
# dict2 = {'name': 'John', 'age': 30}
# print(template_validation(dict1, dict2))
