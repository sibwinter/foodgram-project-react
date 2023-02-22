from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin,
                                        UserManager,BaseUserManager)

from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from users.validators import SelfValidate


class CustomUserManager(BaseUserManager):
    def create_superuser(
            self, email, username, first_name, last_name,
            password, **extra_fields
    ):
        
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if not extra_fields.get("is_staff"):
            raise ValueError("Отказано в доступе")

        if not extra_fields.get("is_superuser"):
            raise ValueError("Отказано в доступе")

        superuser = self.create_user(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        return superuser
        

    def create_user(self, first_name, last_name,
                    email, password, **extra_fields):

        if not email:
            raise ValueError("Укажите email!")

        email = self.normalize_email(email)
        user = self.model(
            email=email, first_name=first_name,
            last_name=last_name, **extra_fields
        )

        user.set_password(password)
        
        user.save()

        return user
    

class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    ADMIN = 'admin'
    USER = 'user'
    ROLE_POOL = [
        (ADMIN, 'Администратор'),
        (USER, 'Пользователь'),
    ]

    username = models.CharField(
        'Логин',
        max_length=150,
        unique=True,
        validators=[SelfValidate, username_validator]
    )
    email = models.EmailField(
        'Электронная почта',
        max_length=254,
        unique=True
    )
    first_name = models.CharField(
        'Имя пользователя',
        max_length=150
    )
    last_name = models.CharField(
        'Фамилия пользователя',
        max_length=150
    )
    role = models.CharField(
        'Роль пользователя',
        max_length=40,
        choices=ROLE_POOL,
        default=USER
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True


    def __str__(self):
        return self.email

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'

        constraints = [
            models.CheckConstraint(
                check=~models.Q(username__iexact='me'),
                name='username_is_not_me'
            )
        ]


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follower')

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique following'
            )
        ]
