from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from datetime import datetime, timedelta, timezone
from django.conf import settings
from Systeme_Alerte.settings import *
import jwt

# Create your models here.
class UserManager(BaseUserManager):

    def create_user(self,username,email,role,nom,prenom,telephone=None,password=None):
       
        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(
            nom=nom,
            prenom=prenom,
            username=username, 
            email=self.normalize_email(email),
            role=role,
            telephone=telephone,
            )
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email,password):
        
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email,"ADMIN","","","",password=password,)
        user.is_superuser = True
        user.is_staff = True
        user.admin = True
        user.save(using=self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):
    
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
   
    # More fields required by Django when specifying a custom user model.
    nom = models.CharField(max_length=255,null=False, blank=False)
    prenom = models.CharField(max_length=255,null=True, blank=True)
    password = models.CharField(max_length=255, blank=False, null=False)
    role = models.CharField(max_length = 255, null=False, choices=(("ADMIN","ADMIN"),("AGRICULTEUR","AGRICULTEUR"),("GESTIONNAIRE","GESTIONNAIRE")))
    telephone = models.CharField(max_length=15,null=True, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    
    objects = UserManager()

    def __str__(self):
        return self.nom
    
    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        ordering = ['nom']

    @property
    def token(self):
        
        return self._generate_jwt_token()
    
    def get_full_name(self):
        
        return self.username

    def get_short_name(self):
       
        return self.username
    
    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'role': self.role,
            'iat': datetime.now(tz=timezone.utc),  # Timestamp de création
            'nbf': datetime.now(tz=timezone.utc),  # Ne peut être utilisé avant maintenant
            'exp': datetime.now(tz=timezone.utc) + timedelta(days=3)
        }, settings.SECRET_KEY, algorithm='HS256')

        return token
