from django.urls import path, include
from .views import RegisterUser, LoginUser, LogoutUser, UserAccountInformation, activate_user
from django.conf import settings
from django.conf.urls.static import static

app_name="accounts"

urlpatterns = [

    path('register/', RegisterUser.as_view(), name="register"),
    path('login/', LoginUser.as_view(), name="login"),
    path('logout/', LogoutUser.as_view(), name="logout"),
    path('info/', UserAccountInformation.as_view(), name="info"),
    path('activate/<uidb64>/<token>/', activate_user, name="activate"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
