import smtplib
import ssl

from email.mime.text import MIMEText


class Email:
    def __init__(self, sender_email, sender_password):
        self.__sender_email = sender_email
        self.__sender_pass = sender_password
        self.__head = '''
<!DOCTYPE html>
<html lang="en">
    <head>
        <title>Steam Spy Report</title>
        <style>
            body {background-color: #202020; color: #E0E0E0; text-align: center}
            a {color: #DAA520; text-decoration: none;} a:hover {color: #FFD700;}
            .off {text-decoration-line: line-through;}
            .platforms {display: block; justify-content: center; margin: 10px;}
            .linux {content: url('https://store.steampowered.com/public/images/v6/icon_platform_linux.png');}
            .mac {content: url('https://store.steampowered.com/public/images/v6/icon_platform_mac.png');}
            .win {content: url('https://store.steampowered.com/public/images/v6/icon_platform_win.png');}
        </style>
    </head>
    <body>'''
        self.__body = ''
        self.__end = '''
    </body>
</html>'''

    def add_body(self, item):
        item_price_discount = str(item['discount'])
        item_price_old = str(item['price_old'] / 100.0)
        item_price_new = str(item['price_new'] / 100.0)
        self.__body += '''
        <h1><a href="''' + item['url'] + '''">''' + item['name'] + '''</a></h1>
        <h2>''' + item_price_discount + '''% discount</h2>
        <h3>''' + item_price_new + '''€ / <span class="off">''' + item_price_old + '''€</span></h3>
        '''
        self.__add_platforms(item['win'], item['mac'], item['linux'])
        self.__body += '<a href="' + item['url'] + '"><img src="' + item['preview'] + '" alt="Preview Image"></a>'

    def clear_body(self):
        self.__body = ''

    def send(self, receivers):
        if self.__body:
            email = MIMEText(self.__head + self.__body + self.__end, 'html')
            email['Subject'] = 'Steam Spy'
            with smtplib.SMTP_SSL(host='smtp.gmail.com', port=465, context=ssl.create_default_context()) as server:
                try:
                    server.login(self.__sender_email, self.__sender_pass)
                except smtplib.SMTPAuthenticationError:
                    print('Invalid email address or password. (' + self.__sender_email + ' ' + self.__sender_pass + ')')
                else:
                    try:
                        server.sendmail(self.__sender_email, receivers, email.as_string())
                    except smtplib.SMTPRecipientsRefused:
                        print('The server rejected ALL recipients. ' + str(receivers))
                    else:
                        print('Report sent to the following addresses. ' + str(receivers))
                        return True

        return False

    def __add_platforms(self, win, mac, linux):
        self.__body += '<div class="platforms">'
        if win:
            self.__body += '<span class="win"></span>'
        if mac:
            self.__body += '<span class="mac"></span>'
        if linux:
            self.__body += '<span class="linux"></span>'
        self.__body += '''</div>
        '''
