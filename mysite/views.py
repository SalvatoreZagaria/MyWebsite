from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import render


def index(request):
    return render(request, 'mysite/base.html')


def download(request):
    from django.conf import settings
    import os
    file_path = os.path.join(settings.BASE_DIR, 'mysite', 'static', 'mysite', 'salvatore_zagaria_cv.pdf')
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/pdf")
            response['Content-Disposition'] = 'attachment; filename=salvatore_zagaria_resume.pdf'
            return response
    raise HttpResponseServerError


def send_email(request):
    import re
    import smtplib
    from email.mime.text import MIMEText
    from boto.s3.connection import S3Connection
    import os
    toaddr = ['s.zagaria9@gmail.com', 's.zaga@hotmail.it']
    email_regex = re.compile(r'^.+@([?)[a-zA-Z0-9-.]+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$)')
    if request.method == 'POST':
        name = request.POST.get('contactName')
        email = request.POST.get('contactEmail')
        subject = request.POST.get('contactSubject')
        message = request.POST.get('contactMessage')
        if name and email and subject and message:
            if email_regex.match(email):
                message = MIMEText(message)

                message['From'] = name + '  <' + email + '>'
                message['Subject'] = subject
                msg_full = message.as_string()
                try:
                    server = smtplib.SMTP('smtp.gmail.com:587')
                    server.starttls()
                    server.login('zagaria.services@gmail.com', S3Connection(os.environ['PASSW']))
                    # server.login('zagaria.services@gmail.com', os.environ['PASSW'])
                    server.sendmail(email,
                                    toaddr,
                                    msg_full)
                    server.quit()

                    response = HttpResponse()
                    response.status_code = 200
                    return response
                except:
                    response = HttpResponse()
                    error = "Server error"
                    response.status_code = 500
                    response.reason_phrase = error
                    return response
            else:
                response = HttpResponse()
                error = "The email address is not valid"
                response.status_code = 400
                response.reason_phrase = error
                return response
        else:
            response = HttpResponse()
            error = "One or more fields missing"
            response.status_code = 400
            response.reason_phrase = error
            return response
