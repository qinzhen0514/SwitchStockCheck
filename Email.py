import smtplib

gmail_user = 'xxx@gmail.com'
gmail_password = 'xxx'

sent_from = gmail_user
to = ['xxx@gmail.com']
subject = 'Switch Stock'
body = 'Available Online'

email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, ", ".join(to), subject, body)


def email():

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()

        print('Email sent!')

    except:
        print('Error Occurred')