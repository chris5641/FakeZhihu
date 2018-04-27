from django.utils import timezone
from django.db import models
from django.conf import settings

from asks.models import Ask


class Answer(models.Model):
    content_text = models.TextField(verbose_name='答案文本')
    content = models.TextField(verbose_name='答案')
    create_time = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='answers',
                               on_delete=models.CASCADE, verbose_name='回答者')
    ask = models.ForeignKey(Ask, related_name='answers', on_delete=models.CASCADE, verbose_name='问题')
    votes = models.IntegerField(default=0, verbose_name='赞同数')

    def __str__(self):
        return self.content_text[:50]

    def voteup(self):
        self.votes += 1
        self.save()

    def votedown(self):
        self.votes -= 1
        self.save()

