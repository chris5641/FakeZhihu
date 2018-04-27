import random

from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker

from ...models import User
from asks.models import Ask
from answers.models import Answer
from comments.models import Comment

fake = Faker('zh_CN')


class Command(BaseCommand):
    help = '生成测试数据'

    def add_arguments(self, parser):
        parser.add_argument('-o', dest='o', default=False, nargs='+')

    def handle(self, *args, **options):
        tzone = timezone.get_current_timezone()
        if not options['o'] or (options['o'] and 'user' in options['o']):
            # 生成用户数据
            print('正在生成用户数据...')
            for i in range(50):
                User.objects.create_user(username=('test'+str(i)),
                                         nickname=fake.name(),
                                         password='test1234',
                                         email=fake.free_email(),
                                         sex=random.choice(['F', 'M']),
                                         intro=fake.sentence(),
                                         work=fake.company())
            print('用户数据生成完成！')

        if not options['o'] or (options['o'] and 'relationship' in options['o']):
            # 生成关注关系
            print('正在生成用户关系...')
            user_count = User.objects.count()
            for i in range(user_count):
                try:
                    u = User.objects.get(id=i)
                except User.DoesNotExist:
                    continue
                follow_limit = random.randint(5, 10)
                for _ in range(follow_limit):
                    u.follow(random.randint(1, user_count))
            print('用户关系生成完成！')

        if not options['o'] or (options['o'] and 'ask' in options['o']):
            # 生成问题
            print('正在生成问题...')
            user_count = User.objects.count()
            topic_list = ['互联网', 'Python', '编程', '游戏', '金融', '信息', '健身', 'NBA', '深圳市',
                          '科技', '芯片', '电脑', '电影', '音乐', '法律', '大学', '中国']
            for i in range(user_count):
                try:
                    u = User.objects.get(id=i)
                except User.DoesNotExist:
                    continue
                ask_limit = random.randint(1, 10)
                for _ in range(ask_limit):
                    topics = random.sample(topic_list, random.randint(1, 3))
                    ask = Ask.objects.create(title=fake.sentence(),
                                             content=fake.text(),
                                             author=u,
                                             create_time=fake.past_datetime(start_date="-2y", tzinfo=tzone),
                                             )
                    ask.add_topics(topics)
            print('问题生成完成！')

        if not options['o'] or (options['o'] and 'answer' in options['o']):
            # 生成答案
            print('正在生成答案...')
            user_count = User.objects.count()
            ask_count = Ask.objects.count()
            answer_list = []
            for i in range(user_count):
                try:
                    u = User.objects.get(id=i)
                except User.DoesNotExist:
                    continue
                ask_limit = random.randint(5, 30)
                for _ in range(ask_limit):
                    content = fake.text(max_nb_chars=1000)
                    ask = Ask.objects.get(id=random.randint(1, ask_count))
                    answer_list.append(Answer(author=u,
                                              content_text=content,
                                              content=content,
                                              ask=ask,
                                              create_time=fake.past_datetime(start_date="-2y", tzinfo=tzone),))
                Answer.objects.bulk_create(answer_list)
                answer_list = []
            print('答案生成完成！')

        if not options['o'] or (options['o'] and 'comment' in options['o']):
            # 生成评论
            print('正在生成评论...')
            user_count = User.objects.count()
            answer_count = Answer.objects.count()
            comment_list = []
            for i in range(user_count):
                try:
                    u = User.objects.get(id=i)
                except User.DoesNotExist:
                    continue
                answer_limit = 100
                for _ in range(answer_limit):
                    try:
                        answer = Answer.objects.get(id=random.randint(1, answer_count))
                    except Answer.DoesNotExist:
                        continue
                    comment_list.append(Comment(content=fake.sentence(),
                                                author=u,
                                                answer=answer,
                                                create_time=fake.past_datetime(start_date="-2y", tzinfo=tzone),))
                Comment.objects.bulk_create(comment_list)
                comment_list = []
            print('评论生成完成！')

        if not options['o'] or (options['o'] and 'vote' in options['o']):
            # 生成点赞数据
            print('正在点赞...')
            user_count = User.objects.count()
            answer_count = Answer.objects.count()
            answer_limit = 200
            vote_list = []
            for i in range(user_count):
                try:
                    u = User.objects.get(id=i)
                except User.DoesNotExist:
                    continue
                answer_list = random.sample(range(answer_count), answer_limit)
                for answer_id in answer_list:
                    try:
                        answer = Answer.objects.get(id=answer_id)
                    except Answer.DoesNotExist:
                        continue
                    # u.voteup(answer)
                    if u.is_voted(answer) is False:
                        vote_list.append(answer)
                        answer.voteup()
                u.vote_answers.add(*vote_list)
                vote_list = []
            print('点赞完成！')

        if not options['o'] or (options['o'] and 'collection' in options['o']):
            # 生成点赞数据
            print('正在收藏...')
            user_count = User.objects.count()
            answer_count = Answer.objects.count()
            collection_list = []
            for i in range(user_count):
                try:
                    u = User.objects.get(id=i)
                except User.DoesNotExist:
                    continue
                answer_list = random.sample(range(answer_count), random.randint(5, 30))
                for answer_id in answer_list:
                    try:
                        answer = Answer.objects.get(id=answer_id)
                    except Answer.DoesNotExist:
                        continue
                    if u.is_collected(answer) is False:
                        collection_list.append(answer)
                u.collections.add(*collection_list)
                collection_list = []
            print('收藏完成！')





