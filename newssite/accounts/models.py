from django.db import models
from django.contrib.auth.models import (
    AbstractUser, BaseUserManager
)


# Create your models here.


class NewUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError("User must have an email!")
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class NewUser(AbstractUser):
    username = None
    email = models.EmailField(verbose_name="email", max_length=100, unique=True)
    first_name = models.CharField(verbose_name="Ім'я", max_length=150)
    last_name = models.CharField(verbose_name="Прізвище", max_length=150)

    objects = NewUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = "Користувачі"
        verbose_name_plural = "Користувачі"
