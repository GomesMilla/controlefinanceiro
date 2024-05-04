from django.db import models
from django.db.models import Q
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin


class UserManager(BaseUserManager):
    def get_or_create(self, defaults=None, **kwargs):
        try:
            user = self.get(**kwargs)
            if user.excluido or not user.is_active:
                user.excluido = False
                user.is_active = True
                user.save()
            return user, False
        except self.model.DoesNotExist:
            return self._create_user(**kwargs, defaults=defaults), True

    def _create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Usuário deve ter um email válido")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password, **extra_fields)

    def get_queryset(self):
        return super(UserManager, self).get_queryset().exclude(is_active=False).exclude(excluido=True)

    def todos_usuarios(self):
        return super(UserManager, self).get_queryset()

THEME = {
    "dark" : "Dark",
    "light" : "Light",
    "auto" : "Auto",
}

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        max_length=255,
        unique=True,
    )
    email = models.EmailField(verbose_name="Endereço de E-mail", max_length=255, unique=True, null=True, blank=True)
    image = models.ImageField("Foto de Perfil", upload_to="image/", blank=True, null=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    descreption = models.TextField(blank=True, null=True)
    theme = models.CharField(max_length=5, choices=THEME, default="dark")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    excluido = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def save(self, *args, **kwargs):
        if not self.pk:
            usuarios_qs = User.objects.todos_usuarios().filter(Q(excluido=True) | Q(is_active=False), username=self.username)
            if usuarios_qs:
                usuarios_qs.update(is_active=True, excluido=False)
                user = usuarios_qs.first()
                return usuarios_qs.first()

        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        inativar = kwargs.get("inativar", False)
        if not inativar:
            self.excluido = True
        self.is_active = False
        self.save()

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

class ProfileManager(BaseUserManager):
    def get_queryset(self):
        return super(ProfileManager, self).get_queryset().exclude(user__is_active=False).exclude(user__excluido=True)

    def todos_usuarios(self):
        return super(ProfileManager, self).get_queryset()

    def usuarios_inativos(self):
        return super(ProfileManager, self).get_queryset().filter(user__is_active=False)

    def usuarios_ativos(self):
        return super(ProfileManager, self).get_queryset().filter(user__is_active=True)


class Base(models.Model):
    data_created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name="created_by_user", on_delete=models.PROTECT)

    def __str__(self):
        return self.created_by

    
