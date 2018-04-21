import hashlib
from django.db import models
from django.contrib.auth.models import AbstractUser

from answers.models import Answer, VoteMap


class User(AbstractUser):
    email = models.EmailField(max_length=64, unique=True, verbose_name='邮箱')
    nickname = models.CharField(max_length=32, verbose_name='昵称')
    sex = models.CharField(max_length=2, choices=(('M', '男'), ('F', '女')), default='M', verbose_name='性别')
    intro = models.CharField(max_length=64, blank=True, verbose_name='简介')
    work = models.CharField(max_length=64, blank=True, verbose_name='工作行业')
    image_url = models.URLField(blank=True, verbose_name='头像')

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
        if follow_user is not None and not self.is_following(follow_user) and self.id != follow_user.id:
            follow_ship = FollowShip(follow=follow_user, fun=self)
            follow_ship.save()
            return True

    def unfollow(self, user_id):
        try:
            follow_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return False
        if follow_user is not None and self.is_following(follow_user):
            follow_ship = self.follow_list.get(follow=follow_user)
            follow_ship.delete()
            return True

    def is_following(self, user):
        return True if self.follow_list.filter(follow=user).first() else False

    def voteup(self, answer):
        if self.is_voted(answer):
            return '{} 已经点赞过了: {}'.format(self, answer.id)
        vote = VoteMap(user=self, answer=answer)
        vote.save()
        answer.voteup()
        return vote

    def votedown(self, answer):
        if not self.is_voted(answer):
            return False
        vote = VoteMap.objects.filter(user=self, answer=answer).first()
        vote.delete()
        answer.votedown()
        return True

    def is_voted(self, answer):
        if VoteMap.objects.filter(user=self, answer=answer).first():
            return True
        else:
            return False

    @staticmethod
    def _get_answer(votemap):
        return votemap.answer

    @property
    def vote_list(self):
        vote_map = VoteMap.objects.filter(user=self)
        if vote_map is not None:
            vote_list = list(map(self._get_answer, vote_map.all()))
            return vote_list
        else:
            return []


class FollowShip(models.Model):
    follow = models.ForeignKey(User, related_name='fun_list', on_delete=models.CASCADE, verbose_name='被关注者')
    fun = models.ForeignKey(User, related_name='follow_list', on_delete=models.CASCADE, verbose_name='粉丝')

    def __str__(self):
        return '{fun} 关注: {follow}'.format(fun=self.fun.username, follow=self.follow.username)
