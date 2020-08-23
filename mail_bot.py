import smtplib
import utils
import os

# Logger configuration
logger = utils.make_console_logger("mail_bot")


class Mail_Bot:
    def __init__(self):
        self.bot_mail = os.environ.get('BOT_MAIL')
        self.bot_pass = os.environ.get('BOT_GOOGLE_APP_PASS')

    @staticmethod
    def bot_signature():
        return '''I'm a bot :)
            you can see my source code @ https://github.com/rpotierferry/weather_monitor'''

    def send_mail(self, receiver, message):
        message += Mail_Bot.bot_signature()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(self.bot_mail, self.bot_pass)
            logger.info("logged in successfuly...")
            smtp.sendmail(self.bot_mail, receiver, message)
            logger.info("mail sent!")
