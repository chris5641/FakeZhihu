import hashlib
from django.db import models
from django.contrib.auth.models import AbstractUser

from answers.models import Answer


class User(AbstractUser):
    email = models.EmailField(max_length=64, unique=True, verbose_name='邮箱')
    nickname = models.CharField(max_length=32, verbose_name='昵称')
    sex = models.CharField(max_length=2, choices=(('M', '男'), ('F', '女')), default='M', verbose_name='性别')
    intro = models.CharField(max_length=64, blank=True, verbose_name='简介')
    work = models.CharField(max_length=64, blank=True, verbose_name='工作行业')
    image_url = models.URLField(blank=True, verbose_name='头像')
    followings = models.ManyToManyField('self', related_name='funs', symmetrical=False, verbose_name='关注')
    vote_answers = models.ManyToManyField(Answer, related_name='vote_user', verbose_name='点赞答案')

    def __str__(self):
        return self.username

    def update(self, date):
        self.nickname = date.get('nickname')
        self.sex = date.get('sex')
        self.intro = date.get('intro')
        self.image_url = date.get('image_url')
        self.save()

    @property
    def get_image_url(self):
        if self.image_url is None or self.image_url is '':
            url = 'https://cdn.v2ex.com/gravatar/{id}?default=monsterid&size=256'
            image_id = hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()
            return url.format(id=image_id)
        else:
            return self.image_url

    def follow(self, user_id):
        try:
            follow_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return False
        if self.id != follow_user.id and not self.is_following(follow_user):
            self.followings.add(follow_user)
            return True

    def unfollow(self, user_id):
        try:
            follow_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return False
        if self.is_following(follow_user):
            self.followings.remove(follow_user)
            return True

    def is_following(self, user):
        return self.followings.filter(id=user.id).exists()

    def voteup(self, answer):
        if self.is_voted(answer):
            return False
        self.vote_answers.add(answer)
        answer.voteup()
        return True

    def votedown(self, answer):
        if not self.is_voted(answer):
            return False
        self.vote_answers.remove(answer)
        answer.votedown()
        return True

    def is_voted(self, answer):
        return self.vote_answers.filter(id=answer.id).exists()

    @staticmethod
    def _get_answer(votemap):
        return votemap.answer

