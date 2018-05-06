def send_email(user, address, key):
    """Send an email to the passed address.

    This could later be improved to send other types of emails but right
    now it will only send a reset email.
    """

    sender = "elthran.online@no-reply.ca"
    receivers = [address]

    # url = 'https://mydomain.com/reset=' + token_urlsafe()
    # if server:
    # link = "https://elthran.pythonanywhere.com/reset?user={}&&key={}".format(user, key)
    # Gets generic url that should work on server or local machine.
    link = "{}reset?user={}&&key={}".format(request.url_root, user, key)

    from_email = Email("Elthran Online <{sender}>".format(sender=sender))
    to_email = Email("Owner of account '{user}' <{address}>".format(user=user, address=address))
    subject = "Reset link for ElthranOnline"

    message = Content("text/html", """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
 <head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
  <title>Reset Password Email</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
</head>
<body style="margin: 0; padding: 0;">
 <table border="0" cellpadding="0" cellspacing="0" width="100%">
  <tr>
   <td>
    <p>Hi Owner of account '{user}',</p>
    <p>&#9;Please click this link <a clicktracking=off href="{link}">{link}</a> to reset your account.</p>
    <p>You will be prompted to enter a new account password.</p>
   </td>
  </tr>
 </table>
</body>
</html>
""".format(user=user, link=link))

    mail = Mail(from_email, subject, to_email, message)
    try:
        response = sg.client.mail.send.post(request_body=mail.get())
        print("Successfully sent email")
    except Exception as ex:
        print("Error: unable to send email")
        print("You need to setup your sendgrid server correctly.")
        print(ex)  # Fail gracefully ... should probably send error to user
