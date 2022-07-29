from django.urls import path, include
from .views import whether
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_default

app_name="wheather"

urlpatterns = [

    path('', whether, name="wheather"),



]
