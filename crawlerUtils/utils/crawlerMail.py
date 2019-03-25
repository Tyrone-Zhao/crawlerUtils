import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr


__all__ = [
    "Mail",
]


class Mail():

    def __init__(self, **kwargs):
        super().__init__()

    @classmethod
    def mailSend(self, recipients=[], account="", password="", subj="", text=""):
        """ 发送邮件 """
        smtp = smtplib.SMTP("smtp.qq.com")
        smtp.login(account, password)
        smtp.noop()
        smtp.login(account, password)
        sender = "亲爱的我"
        recipients = recipients.split()
        recipient = "亲爱的你"

        message = MIMEText(text, "html", "utf-8")
        message['From'] = formataddr([sender, account])
        message["Subject"] = Header(subj, "utf-8")
        message["To"] = Header(recipient, "utf-8")

        smtp.sendmail(account, recipients, message.as_string())
        smtp.quit()


    @classmethod
    def mailSendInput(self):
        ''' 接收发送邮件所需要的信息，返回recipients, account, password, subj, text '''
        recipients = input("请输入收件人列表，多个收件人以空格隔开：")
        account = input("请输入你的QQ邮箱账号：")
        password = input("请输入你的QQ邮箱授权码：")
        subj = input("请输入邮件主题：")
        text = input("请输入邮件内容：")

        return recipients, account, password, subj, text
