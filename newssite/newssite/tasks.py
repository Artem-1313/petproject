from django.core.mail import EmailMessage,send_mail
from django.template.loader import render_to_string
from django.conf import settings
from celery import task


@task(bind=True, ignore_result=True, name="newssite.tasks.debug_task")
def debug_task(self):
    print(f'Request: {self.request!r}')

@task(name="tez")
def schedule_mail():
  #  from newsapp.models import Article, Subscriber
    #mailreceivers = [i for i in Subscriber.objects.all()]
  send_mail(
    'Subject here',
    'Here is the message.',
    'from@example.com',
    ['artemthfc@gmail.com'],
    fail_silently=False,
  )
  """  
  for i in Subscriber.objects.all():
        message = render_to_string("newsapp/email_crontab.html",{
            "domain": settings.SITE_URL,
            "article": Article.objects.latest('id').id


        })
        mail_subject = 'Розсилка новин!'
        email = EmailMessage(
            mail_subject,
            message,
            from_email=settings.EMAIL_HOST_USER,
            to=["artemthfc@gmail.com"])
        email.send()
"""