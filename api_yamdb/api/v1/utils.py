from django.contrib.auth.tokens import default_token_generator
from django.conf.global_settings import DEFAULT_FROM_EMAIL
from django.core.mail import send_mail


def send_message_to_user(username, recepient_email, confirmation_code):
    send_mail(
        subject='Код подтверждения YAMDb',
        message=f'Здравствуйте, {username} \n\n'
                f'Вы получили это сообщение, '
                f'так как на адрес электронной почты: \n'
                f' {recepient_email}\n'
                f'происходит регистрация на сайте "API_yamdb". \n  \n'
                f'Ваш код подтверждения : {confirmation_code} \n \n'
                f'Если Вы не пытались зарегистрироваться - \n'
                f'просто не отвечайте на данное сообщение и \n'
                f'не производите никаких действий',
        from_email=DEFAULT_FROM_EMAIL,
        recipient_list=(recepient_email,),
    )


def make_confirmation_code(data):
    confirmation_code = default_token_generator.make_token(data)
    return confirmation_code
