from django.shortcuts import render
from django.views.decorators.http import require_GET
from rest_framework.decorators import (api_view, permission_classes)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_400_BAD_REQUEST)
import threading
import requests
from json import loads
from uuid import uuid4
from zipfile import ZipFile
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


@require_GET
def home_view(request):
    return render(request, 'api/home.html')


@api_view(['POST'])
@permission_classes([AllowAny])
def scrape_view(request):
    try:
        urls = request.POST.get('urls')
        email = request.POST.get('email')

        if None not in (urls, email):
            p = threading.Thread(target=process_request, args=(urls, email))
            p.start()
            return Response(data={'success': True, 'message': 'The file(s) will be sent to your email!'})
        else:
            raise Exception('Invalid Email or URLs!')

    except Exception as e:
        return Response(data={'success': False, 'message': str(e)}, status=HTTP_400_BAD_REQUEST)


def process_request(urls, email):
    file_names = download_urls(urls)
    zip_file = generate_zip(file_names, email)
    send_email(zip_file, email)


def download_urls(urls):
    urls = loads(urls)
    if len(urls) > 3:
        urls = urls[:3]

    file_names = []
    for url in urls:
        print(url)
        r = requests.get(url)
        file_name = f'{str(uuid4())}.html'
        file_names.append(file_name)
        with open(file_name, 'wb') as f:
            f.write(r.content)

    return file_names


def generate_zip(file_names, email):
    zip_name = f'{email}.zip'
    with ZipFile(zip_name, 'w') as zf:
        for file in file_names:
            zf.write(file)
            os.remove(file)

    return zip_name


def send_email(zip_file, email):
    FROM_EMAIL = os.environ.get('FROM_EMAIL')
    FROM_EMAIL_PASSWORD = os.environ.get('FROM_EMAIL_PASSWORD')
    TO_EMAIL = email
    SMTP_SERVER = os.environ.get('SMTP_SERVER')
    SMTP_PORT = int(os.environ.get('SMTP_PORT'))
    print(type(SMTP_PORT))

    msg = MIMEMultipart()

    msg['From'] = FROM_EMAIL
    msg['To'] = TO_EMAIL
    msg['Subject'] = 'Scraping Project - Compressed HTML Files'

    body = 'We have recevied your request. Files have been zipped and attached!'

    msg.attach(MIMEText(body, 'plain'))
    attachment = open(zip_file, "rb")

    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', f"attachment; filename= {zip_file}")
    msg.attach(p)

    s = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    s.starttls()
    s.login(FROM_EMAIL, FROM_EMAIL_PASSWORD)
    text = msg.as_string()
    s.sendmail(FROM_EMAIL, TO_EMAIL, text)
    s.quit()

    os.remove(zip_file)
    return None