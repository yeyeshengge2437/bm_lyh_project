
import smtplib
from email.mime.text import MIMEText
from email.header import Header

_user = "2347948121@qq.com"
_pwd = "oytdejvazxljecgf"
_to = "3648147420@qq.com"

msg = MIMEText("www.baidu.com")
msg["Subject"] = "Python 发送邮件测试"
msg["From"] = _user
msg["To"] = _to

i = 0
while i < 1:
    try:
        s = smtplib.SMTP_SSL("smtp.qq.com", 25)
        s.login(_user, _pwd)
        s.sendmail(_user, _to, msg.as_string())
        s.quit()
        print("Success!")
    except smtplib.SMTPException as e:
        print("Falied,%s" % e)

    i = i + 1
