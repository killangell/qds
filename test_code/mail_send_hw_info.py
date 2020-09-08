import smtplib
from email.mime.text import MIMEText
import wmi

c = wmi.WMI()

# 第三方 SMTP 服务
mail_host = "smtp.qq.com"  # SMTP服务器
mail_user = "313970187@qq.com"  # 用户名
mail_pass = "vjpzbwdiodvobifj"  # 密码(这里的密码不是登录邮箱密码，而是授权码)

sender = '313970187@qq.com'  # 发件人邮箱
receivers = ['liaoyizs@163.com']  # 接收人邮箱

content = 'Python Send Mail !'
content = "first_disk_serial_num:{0} master_board_serial_num:{1}".format(
    c.Win32_DiskDrive()[0].SerialNumber, c.Win32_BaseBoard()[0].SerialNumber)
title = 'lixiaoguang'  # 邮件主题
message = MIMEText(content, 'plain', 'utf-8')  # 内容, 格式, 编码
message['From'] = "{}".format(sender)
message['To'] = ",".join(receivers)
message['Subject'] = title

try:
    smtpObj = smtplib.SMTP_SSL(mail_host, 465)  # 启用SSL发信, 端口一般是465
    smtpObj.login(mail_user, mail_pass)  # 登录验证
    smtpObj.sendmail(sender, receivers, message.as_string())  # 发送
    print("mail has been send successfully.")
except smtplib.SMTPException as e:
    print(e)