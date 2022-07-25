from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
# MANEJA LAS OPERACIONES DE CREACIO DE USUARIOS


class MyAccountManager(BaseUserManager):
    # PERMITE LA CREACION DE UN USUARIO
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('el usuario debe tener un email')

        if not username:
            raise ValueError('el usuario debe tener un username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    # PERMITE LA CREACION DE UN SUPERUSUARIO

    def create_superuser(self, first_name, last_name, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        # ESTOS SON LOS CONFIGURACIONES QUE DIFERENCIAN UN USUARIOS
        # CON UN SUPERUSUARIO
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


# ADMINISTRA LOS DATOS  DE LOGUEO Y REGISTRO
class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=50)

    # campos atributos de django
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    # PARA CAMBIAR QUE NO SE AUTENTIQUE POR USERNAME SINO CON EMAIL
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    # HACE LA REFERENCIA PARA PODER CREAR USUARIOS
    objects = MyAccountManager()

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    # PARA QUE EL EL GRUPO DE USUARIOS MARQUE EL EMAIL
    def __str__(self):
        return self.email

    # PARA VALIDAR SI ES ADMIN
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # PARA VALIDR QUE TENGA ACCESO A LOS MODULOS
    def has_module_perms(self, add_label):
        return True
