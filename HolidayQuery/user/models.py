from django.db import models
import jwt
from datetime import datetime, timedelta
from django.conf import settings


class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.username

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        token = jwt.encode({
            'exp': datetime.utcnow() + timedelta(days=1),
            'iat': datetime.utcnow(),
            'data': {
                'username': self.username
            }
        }, settings.SECRET_KEY, algorithm='HS256')
        return token.decode('utf-8')


class Holiday(models.Model):
    holiday_name = models.CharField(max_length=50)
    holiday_date = models.DateField(max_length=50)

    def __str__(self):
        return self.holiday_name
