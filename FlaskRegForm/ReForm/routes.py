# -*- coding: utf-8 -*-
from ReForm import ReForm
from flask import render_template
from ReForm.forms import LoginForm
import telnetlib
import re

myIP = ' 91.202.131.121 '
ProxyIP = '91.202.128.107'
ProxyPort = 4100
error_answer = ''


@ReForm.route('/')
def index():
    form = LoginForm()
    compare_string = send_commands(ProxyIP, ProxyPort, myIP)
    if compare_format(compare_string.decode('ascii'), r'^[0-9]{1,10}\s[0-9A-Za-z\-_]{1,30}\s[0-9]{1,2}\s[0-9]{1,2}\s'):
        agree_auth = "Вітаємо з успішною авторизацією в AuthProxy. Правила реєстрації: \n\r" \
                    "1) Ім\'я повинно складатись тільки з українських букв \n\r" \
                    "2) Фамілія повинна складатись з укранських букв, а також символів \' та - які " \
                     "використовуються не більше 1 разу"
        return render_template('/index.html', form=form, agreeAuth=agree_auth, submitAuth=form.agreeSubmit)
    else:
        error_auth_var = "Увага!"
        error_auth = "Запустіть клієнт та виконайте вхід в систему Authproxy перед регістрацією поштової скриньки."
        return render_template('/index.html', form=form, errorAuth=error_auth, errorAuthWar=error_auth_var,
                               submitAuth=form.errorSubmit)


@ReForm.route('/inform', methods=['POST'])
def my_inform():
    if verify_inform_page():
        return render_template('/inform.html', errorCode="", informMessege="Вітаємо з реєстрацією.")
    return render_template('/inform.html', errorCode="403", informMessege="Виникла помилка. Спробуйте, ще раз.",
                           error_answer=error_answer)


def send_commands(ip_address, port, ip):
    global error_answer
    try:
        tn = telnetlib.Telnet()
        tn.open(ip_address, port, 10)
        try:
            tn.write(ip.encode('ascii') + 'login dept_id admin_level \n'.encode('ascii'))
            answer = tn.read_all()
        except:
            error_answer = "COMMAND EXECUTION ERROR WHEN SERVER CONNECT WITH AUTHPROXY"
    except:
        error_answer = "CONNECT ERROR WITH AUTHPROXY"
    finally:
        tn.close()
        return answer


def compare_format(comp, pattern):
    global error_answer
    re.UNICODE
    compare_bool_value = False
    result_ = re.search(pattern, comp)
    try:
        if result_.group(0) == comp:
            compare_bool_value = True
    except:
        error_answer = "ERROR COMPARE FORMAT"
    finally:
        return compare_bool_value


def verify_inform_page():
    global error_answer
    form = LoginForm()
    if not compare_format(form.firstName.data, r'^[А-ЯЙЇІЄ][А-яЙЇІЄйїіє]{1,128}$'):
        error_answer = "BAD FIRST NAME"
        return False
    if not compare_format(form.lastName.data,
                          r'^[А-ЯЙЇІЄ][А-яЙЇІЄйїіє \' - і І]{0,128}[А-яЙЇІЄйїіє \' -]{0,128}[а-яйїіє]$'):
        error_answer = "BAD LAST NAME"
        return False
    if not compare_format(form.username.data, r'[A-Za-z0-9@#$%^&+=]{1,128}'):
        error_answer = "BAD USERNAME"
        return False
    if not compare_format(form.password.data, r'[A-Za-z0-9@#$%^&+=]{8,16}'):
        error_answer = "BAD PASSWORD"
        return False
    if not compare_format(form.cPassword.data, r'[A-Za-z0-9@#$%^&+=]{8,16}'):
        error_answer = "BAD CONFIRM PASSWORD"
        return False
    if form.password.data != form.cPassword.data:
        error_answer = "WRONG CONFIRM PASSWORD"
        return False
    if not form.agreeVer.data:
        error_answer = "CHECKBOX IS FALSE"
        return False
    compare_string = send_commands(ProxyIP, ProxyPort, myIP)
    if not compare_format(compare_string.decode('ascii'),
                          r'^[0-9]{1,10}\s[0-9A-Za-z\-_]{1,30}\s[0-9]{1,2}\s[0-9]{1,2}\s'):
        error_answer = "YOU DON`T CONNECT WITH AUTHPROXY"
        return False
    return True
