from django.urls import path, include
from .views import RegisterUser, LoginUser, LogoutUser, UserAccountInformation, activate_user, UserUpdateInformation
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_default

app_name="accounts"

urlpatterns = [

                  path('register/', RegisterUser.as_view(), name="register"),
                  path('login/', LoginUser.as_view(), name="login"),
                  path('logout/', LogoutUser.as_view(), name="logout"),
                  path('info/', UserAccountInformation.as_view(), name="info"),
                  path('activate/<uidb64>/<token>/', activate_user, name="activate"),
                  path('update_user/<int:pk>/', UserUpdateInformation.as_view(), name="update_info_user"),




              ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
