from django.core.mail import EmailMessage,send_mail
from django.template.loader import render_to_string
from django.conf import settings
from celery import task

