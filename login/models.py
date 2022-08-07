from django.db import models


class User(models.Model):
    user_id = models.PositiveIntegerField(unique=True)
    user_name = models.CharField(unique=True, max_length=100)
    user_email = models.EmailField(verbose_name="email", unique=True, max_length=100)
    user_password = models.CharField(max_length=100)

    def __str__(self):
        return self.user_name
