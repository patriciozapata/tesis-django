from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)




class UserManager(BaseUserManager):
    def create_user(self, email, nombre, apellido, perfil, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
        )
        user.nombre = nombre
        user.apellido = apellido
        perfil = Perfil.objects.get(pk=perfil)
        user.perfil = perfil
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nombre, apellido, perfil,staff,admin, password):
        user = self.create_user(email, nombre, apellido, perfil,password=password)
        user.staff = staff
        user.admin = admin
        user.save(using=self._db)
        return user


class Perfil(models.Model):
    perfil = models.CharField(max_length=50)

    def __str__(self):              # __unicode__ on Python 2
        return '{}'.format(self.perfil)


# hook in the New Manager to our Model
class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) #Necesario para administrador debido a que pregunta "is_staff"
    admin = models.BooleanField(default=False) # a superuser
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    imagen = models.ImageField(upload_to='perfil_image',blank=True)
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre', 'apellido','perfil','staff','admin'] # Email & Password are required by default.


    def __str__(self):              # __unicode__ on Python 2
        return self.perfil

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin
    objects = UserManager()
