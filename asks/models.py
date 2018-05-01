from django.utils import timezone
from django.db import models
from django.conf import settings

from topics.models import Topic


class Ask(models.Model):
    title = models.CharField(max_length=64, verbose_name='题目')
    content = models.TextField(verbose_name='问题描述', blank=True)
    clicks = models.IntegerField(default=0, verbose_name='访问量')
    create_time = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='asks',
                               on_delete=models.CASCADE, verbose_name='提问者')
    topics = models.ManyToManyField(Topic, related_name='asks', blank=True, verbose_name='话题')

    def __str__(self):
        return self.title

    def add_topics(self, topics):
        for t_name in topics:
            try:
                topic = Topic.objects.get(name=t_name)
            except Topic.DoesNotExist:
                topic = Topic(name=t_name)
                topic.save()
            self.topics.add(topic)

    def click(self):
        self.clicks += 1
        self.save()

