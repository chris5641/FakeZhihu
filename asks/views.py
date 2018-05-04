from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound, JsonResponse
from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from fakeZhihu.settings import logger
from answers.forms import AnswerForm
from .models import Ask


class CreateAskView(LoginRequiredMixin, generic.CreateView):
    model = Ask
    fields = ['title', 'topics', 'content']

    def form_valid(self, form):
        ask = form.save(commit=False)
        ask.author = self.request.user
        ask.save()
        logger.info('{} 提了问题：{}'.format(self.request.user, ask))
        topics = self.request.POST.get('topics_list', '')
        topics = topics.split(',')
        ask.add_topics(topics)
        return redirect('asks:detail', pk=ask.id)

    def form_invalid(self, form):
        logger.error('提问题错误')
        return redirect('index')


class DetailView(generic.FormView, generic.DetailView):
    model = Ask
    form_class = AnswerForm
    template_name = 'asks/detail.html'
    context_object_name = 'ask'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        asks = Ask.objects.all().order_by('-create_time')[:5]
        vote_list = []
        collection_list = []
        answers_list = self.object.answers.order_by('-votes', '-create_time')
        paginator = Paginator(answers_list, 5)
        topics_list = self.object.topics.all()
        if self.request.user.is_authenticated:
            for answer in answers_list:
                if self.request.user.is_voted(answer):
                    vote_list.append(answer)
                if self.request.user.is_collected(answer):
                    collection_list.append(answer)
        context['vote_list'] = vote_list
        context['collection_list'] = collection_list
        context['asks'] = asks
        context['answers'] = paginator.page(1)
        context['topics_list'] = topics_list
        return context

    def get(self, request, *args, **kwargs):
        super(DetailView, self).get(request, *args, **kwargs)
        vote_list = []
        collection_list = []
        self.object.click()
        page = request.GET.get('page', None)
        if page is None:
            context = self.get_context_data(**kwargs)
            return self.render_to_response(context)

        answers_list = self.object.answers.order_by('-votes', '-create_time')
        paginator = Paginator(answers_list, 5)
        try:
            answers = paginator.page(page)
        except PageNotAnInteger or EmptyPage:
            return HttpResponseNotFound
        if self.request.user.is_authenticated:
            for answer in answers_list:
                if self.request.user.is_voted(answer):
                    vote_list.append(answer)
                if self.request.user.is_collected(answer):
                    collection_list.append(answer)
        context = dict(answers=answers, vote_list=vote_list, collection_list=collection_list, is_ask_index=True)
        return render(request, 'answerslist.html', context)


class AnswerDetailView(generic.FormView, generic.DetailView):
    model = Ask
    form_class = AnswerForm
    template_name = 'asks/detail.html'
    context_object_name = 'ask'

    def get_context_data(self, **kwargs):
        context = super(AnswerDetailView, self).get_context_data(**kwargs)
        asks = Ask.objects.all().order_by('-create_time')[:5]
        topics_list = self.object.topics.all()
        answer = self.object.answers.filter(id=self.kwargs['answer_id']).first()
        vote_list = []
        collection_list = []
        if self.request.user.is_authenticated:
            if self.request.user.is_voted(answer):
                vote_list.append(answer)
            if self.request.user.is_collected(answer):
                collection_list.append(answer)
        context['vote_list'] = vote_list
        context['collection_list'] = collection_list
        context['answer'] = answer
        context['topics_list'] = topics_list
        context['asks'] = asks
        context['answer_view'] = True
        self.object.click()
        return context


@login_required
def follow_ask(request, pk):
    data = dict(
        r=1,
    )
    if request.method == 'POST':
        user = request.user
        ask = Ask.objects.filter(id=pk).first()
        if ask is not None:
            ret = user.follow_ask(ask)
            if ret is True:
                data['r'] = 0
                logger.info('{} 关注了问题： {}'.format(user, ask.id))
            else:
                logger.error('{} 关注问题失败: {}'.format(user, ask.id))
    return JsonResponse(data, status=201)


@login_required
def unfollow_ask(request, pk):
    data = dict(
        r=1,
    )
    if request.method == 'POST':
        user = request.user
        ask = Ask.objects.filter(id=pk).first()
        if ask is not None:
            ret = user.unfollow_ask(ask)
            if ret is True:
                data['r'] = 0
                logger.info('{} 取消关注了问题： {}'.format(user, ask.id))
            else:
                logger.error('{} 取消关注问题失败: {}'.format(user, ask.id))
    return JsonResponse(data, status=201)


