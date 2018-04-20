from django.utils import timezone
from django.db import models
from django.conf import settings

from answers.models import Answer


class Comment(models.Model):
    content = models.TextField(verbose_name='评论内容')
    create_time = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comments',
                               on_delete=models.CASCADE, verbose_name='评论者')
    answer = models.ForeignKey(Answer, related_name='comments', on_delete=models.CASCADE, verbose_name='答案')
    reply_to = models.ForeignKey('self', related_name='replies',
                                 blank=True, null=True, on_delete=models.CASCADE, verbose_name='回复')
