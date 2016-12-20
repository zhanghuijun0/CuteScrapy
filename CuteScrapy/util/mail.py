# coding:utf8
__author__ = 'modm'
import smtplib
import email.MIMEMultipart
import email.MIMEText
import email.MIMEBase
import os.path

# email server
MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
# MAIL_USERNAME = 'qazxhouse@126.com'
# MAIL_PASSWORD = 'zhjzhj2613?'
MAIL_USERNAME = '2248657487@qq.com'
MAIL_PASSWORD = 'vmjwpbgghqihecgh'
MAIL_NAME = '爬虫'
# administrator list
ADMINS = ['modongming@souche.com']

def __format_addr(self, s):
    name, addr = email.Utils.parseaddr(s)
    return email.Utils.formataddr((email.header.Header(name, 'utf-8').encode(),addr.encode('utf-8') if isinstance(addr, unicode) else addr))


def sendEmail(html, subject, mail_to_name, mail_to, files=[]):
    server = smtplib.SMTP(MAIL_SERVER)
    server.login(MAIL_USERNAME, MAIL_PASSWORD)  # 仅smtp服务器需要验证时
    # 构造MIMEMultipart对象做为根容器
    main_msg = email.MIMEMultipart.MIMEMultipart()

    # 构造MIMEText对象做为邮件显示内容并附加到根容器
    text_msg = email.MIMEText.MIMEText(html, 'html')
    # text_msg.add_header('Content-Type','application/html')
    main_msg.attach(text_msg)

    # 构造MIMEBase对象做为文件附件内容并附加到根容器
    contype = 'application/octet-stream'
    maintype, subtype = contype.split('/', 1)

    ## 读入文件内容并格式化
    for file in files:
        file_msg = email.MIMEBase.MIMEBase(maintype, subtype)
        file_msg.set_payload(file.read())
        file.close()
        email.Encoders.encode_base64(file_msg)
        ## 设置附件头
        basename = os.path.basename(file.name)
        file_msg.add_header('Content-Disposition',
                            'attachment', filename=basename)
        main_msg.attach(file_msg)
    # 设置根容器属性
    main_msg['From'] = email.Utils.formataddr((MAIL_NAME, MAIL_USERNAME))
    main_msg['To'] = ','.join(mail_to)
    main_msg['Subject'] = subject
    main_msg['Date'] = email.Utils.formatdate()

    # 得到格式化后的完整文本
    fullText = main_msg.as_string()
    server.set_debuglevel(1)
    # 用smtp发送邮件
    try:
        server.sendmail(MAIL_USERNAME, mail_to, fullText)
    finally:
        server.quit()


if __name__ == '__main__':
    sendEmail(html='<h1>hello</h1><h2> world!</h2>',
              subject='test',
              mail_to_name='test',
              mail_to=['2248657487@qq.com'], files=[open('mail.py', 'r')])
