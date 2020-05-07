from django.db import models


class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.user_name


class Holiday(models.Model):
    holiday_name = models.CharField(max_length=50)
    holiday_date = models.DateField(max_length=50)

    def __str__(self):
        return self.holiday_name
