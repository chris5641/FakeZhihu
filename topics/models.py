from django.db import models


class Topic(models.Model):
    name = models.CharField(max_length=32, verbose_name='话题名', unique=True)
    info = models.CharField(max_length=256, verbose_name='话题描述', blank=True)

    def __str__(self):
        return self.name
