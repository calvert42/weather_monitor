import smtplib
import utils
import os
from email.message import EmailMessage

# Logger configuration
logger = utils.make_console_logger("mail_bot")


class Mail_Bot:
    def __init__(self):
        # these need to be set by the user accordingly
        self.bot_mail = os.environ.get('BOT_MAIL')
        self.bot_pass = os.environ.get('BOT_GOOGLE_APP_PASS')

    @staticmethod
    # adds a signature to the end of the mail
    def bot_signature():
        return "\n\nI'm a bot and I love you:) you can see my source code @ https: // github.com/rpotierferry/weather_monitor"

    @ staticmethod
    def concatenate_body(elemnts):
        body = ""
        for e in elemnts:
            body += str(e)

        return body

    def write_mail(self, receiver, content):
        message = EmailMessage()
        message['To'] = receiver
        message['From'] = self.bot_mail
        message['Subject'] = content.pop(0)
        message.set_content(self.concatenate_body(
            content) + self.bot_signature())
        logger.debug(f"{message}")
        return message

    # send the email to the receiver
    def send_mail(self, receiver, message_content):
        message = self.write_mail(receiver, message_content)
        logger.info(f"Sending e-mail update")
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(self.bot_mail, self.bot_pass)
            logger.info("logged in successfuly...")
            smtp.send_message(message)
            logger.info("mail sent!")
