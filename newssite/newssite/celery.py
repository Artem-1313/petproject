from __future__ import absolute_import, unicode_literals
from django.core.mail import EmailMessage,send_mail
from django.template.loader import render_to_string
from django.conf import settings
from celery.schedules import crontab
import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newssite.settings")

app = Celery("newssite")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.timezone = 'UTC'
#app.autodiscover_tasks()
app.conf.timezone = 'Europe/London'

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    from newsapp.models import Article, Subscriber
    for subscriber in Subscriber.objects.all():
        message = render_to_string("newsapp/email_crontab.html", {
            "domain": settings.SITE_URL,
            "article": Article.objects.latest('id').id

        })
        mail_subject = 'Розсилка новин!'
        email = EmailMessage(
            mail_subject,
            message,
            from_email=settings.EMAIL_HOST_USER,
            to=[subscriber.email])
        email.send()


app.conf.beat_schedule = {
    'email_notifications': {
        'task': 'newssite.celery.debug_task',
        'schedule': crontab(minute="*/15")
    },
}





