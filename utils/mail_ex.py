import logging
import smtplib
from email.mime.text import MIMEText

# 第三方 SMTP 服务
mail_host = "smtp.qq.com"  # SMTP服务器
mail_user = "313970187@qq.com"  # 用户名
mail_pass = "vjpzbwdiodvobifj"  # 密码(这里的密码不是登录邮箱密码，而是授权码)

sender = '313970187@qq.com'  # 发件人邮箱
receivers = ['liaoyizs@163.com']  # 接收人邮箱


class mail_ex:
    @staticmethod
    def send_mail(sender=None, title=None, content=None):
        message = MIMEText(content, 'plain', 'utf-8')  # 内容, 格式, 编码
        message['From'] = "{}".format(sender)
        message['To'] = ",".join(receivers)
        message['Subject'] = title

        try:
            smtpObj = smtplib.SMTP_SSL(mail_host, 465)  # 启用SSL发信, 端口一般是465
            smtpObj.login(mail_user, mail_pass)         # 登录验证
            smtpObj.sendmail(sender, receivers, message.as_string())  # 发送
        except smtplib.SMTPException as e:
            logging.debug("send info failed")


if __name__ == "__main__":
    mail_ex.send_mail('313970187@qq.com', 'title test', 'content test')