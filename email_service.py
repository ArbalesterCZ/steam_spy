import smtplib
import ssl

from email.mime.text import MIMEText


class Email:
    def __init__(self, sender_email, sender_password, receivers):
        self.__sender_email = sender_email
        self.__sender_password = sender_password
        self.__receivers = receivers

        self.__head = '''
        <html>
        <head>
        <style>
        body {background-color: #202020; color: #E0E0E0; text-align: center}
        a {color: #DAA520; text-decoration: none;} a:hover {color: #FFD700;}
        span {text-decoration-line: line-through;}
        </style>
        </head>
        <body>
        '''

        self.__body = ''

        self.__end = '''
        </body>
        </html>
        '''

    def add_body(self, title, preview, url, discount, price_final, price_original):
        self.__body += '''
        <h1><a href="''' + url + '''">''' + title + '''</a></h1>
        <h2>''' + str(discount) + '''% discount</h2>
        <h3>''' + price_original + ''' / <span>''' + price_final + '''</span></h3>
        <a href="''' + url + '''"><img src="''' + preview + '''"></a>
        '''

    def clear_body(self):
        self.__body = ''

    def send(self):
        if self.__body:
            email = MIMEText(self.__head + self.__body + self.__end, 'html')
            email['Subject'] = 'Steam Spy'

            with smtplib.SMTP_SSL(host='smtp.gmail.com', port=465, context=ssl.create_default_context()) as server:
                server.login(self.__sender_email, self.__sender_password)
                server.sendmail(self.__sender_email, self.__receivers, email.as_string())
