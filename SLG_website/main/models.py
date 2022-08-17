import os  # Для создания пользовательской папки для хранения текстов
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserText(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    directory = models.CharField(max_length=255)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        new_directory = 'main/savedtexts/{}'.format(instance)
        os.mkdir(new_directory)
        UserText.objects.create(user=instance, directory=new_directory)
