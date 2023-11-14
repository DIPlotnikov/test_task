import re
import settings
from datetime import datetime
from tinydb import TinyDB, Query
from flask import Flask, request


def email_address_is_valid(email: str):
    """ pattern: sometext@yandex.ru """
    pattern = r'\w+@\w+\.\w+'
    result = re.fullmatch(pattern, email)
    return bool(result)


def clear_num(num: str):
    unsupported_ch = [" ", "-", "(", ")"]
    for ch in unsupported_ch:
        num = num.replace(ch, '')
    return num


def phone_num_is_valid(num: str):
    """ pattern: +7/8 xxx xxx xx xx (x - int)"""
    pattern = r'(?:\+7|8)\d{10}'
    result = re.fullmatch(pattern, clear_num(num))
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
        elif email_address_is_valid(data):
            return 'email'
        elif text_is_valid(data):
            return 'text'
        else:
            raise Exception
    except:
        return 'unsupported type'


def create_form_template(form: dict):
    """the function will create a new form template based on the submitted form"""
    new_form_template = {}
    for key in form.keys():
        new_form_template[key] = get_data_type(form[key])
    return new_form_template  # return dict with new form template


def template_is_valid(form: dict, template: dict):
    for key in template.keys():
        if key == "name":
            continue
        if key not in form or template[key] != form[key]:
            return False
    return True


def get_suitable_form_template(form: dict):
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
    return result  # return list of template names


app = Flask(__name__)


@app.route('/get_form', methods=['POST'])
def receive_data():
    raw_form = dict(request.form)
    form = create_form_template(raw_form)
    s_template_list = get_suitable_form_template(form)

    if s_template_list:  # we have found a suitable form
        if settings.return_all_matching_templates:
            return " ".join(s_template_list)  # return string with tempates names
        else:
            return s_template_list[0]  # return first template name
    else:
        return form


if __name__ == '__main__':
    app.run()



