from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from fakeZhihu.settings import logger
from asks.models import Ask
from .models import Answer
from .forms import AnswerForm
from users.models import User


class IndexView(generic.DetailView):
    template_name = 'users/index.html'

    def get_object(self, queryset=None):
        answers_list = Answer.objects.order_by('-create_time')
        paginator = Paginator(answers_list, 10)
        return paginator

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        asks = Ask.objects.all().order_by('-create_time')[:5]
        vote_list = []
        context['asks'] = asks
        context['answers'] = self.object.page(1)
        if self.request.user.is_authenticated:
            for answer in self.object.page(1):
                if self.request.user.is_voted(answer):
                    vote_list.append(answer)
            context['vote_list'] = vote_list
        return context

    def get(self, request, *args, **kwargs):
        super(IndexView, self).get(request, *args, **kwargs)
        page = request.GET.get('page', None)
        if page is None:
            context = self.get_context_data(**kwargs)
            return self.render_to_response(context)

        vote_list = []
        try:
            answers = self.object.page(page)
        except PageNotAnInteger or EmptyPage:
            return HttpResponseNotFound
        if self.request.user.is_authenticated:
            for answer in self.object.page(page):
                if self.request.user.is_voted(answer):
                    vote_list.append(answer)
        context = dict(answers=answers, vote_list=vote_list)
        return render(request, 'answerslist.html', context)


class CreateAnswerView(LoginRequiredMixin, generic.CreateView):
    model = Answer
    fields = ['content', 'content_text']

    def form_valid(self, form):
        ask_id = self.kwargs['pk']
        ask = Ask.objects.filter(id=ask_id).first()
        user = self.request.user
        if ask is not None:
            answer = form.save(commit=False)
            answer.ask = ask
            answer.author = user
            answer.save()
            logger.info('{} 回答了问题 : {}'.format(self.request.user, answer))
        return redirect(self.request.META.get('HTTP_REFERER', '/'))

    def form_invalid(self, form):
        logger.error('answer error')
        return redirect(self.request.META.get('HTTP_REFERER', '/'))


class DeleteAnswerView(LoginRequiredMixin, generic.DeleteView):
    model = Answer

    def get_success_url(self):
        logger.info('答案：{} 删除成功'.format(self.object.id))
        return self.request.META.get('HTTP_REFERER', '/')


class ShowAnswerView(generic.DetailView):
    model = Answer

    def get(self, request, *args, **kwargs):
        data = dict(r=1)
        try:
            answer = Answer.objects.get(id=kwargs['pk'])
        except Answer.DoesNotExist:
            return JsonResponse(data)
        data['r'] = 0
        data['content'] = answer.content
        data['create_time'] = answer.create_time.date()
        return JsonResponse(data)


@login_required
@csrf_exempt
def vote_up(request, pk):
    data = dict(
        r=1,
    )
    if request.method == 'POST':
        user = request.user
        answer = Answer.objects.filter(id=pk).first()
        if answer is not None:
            vote = user.voteup(answer)
            logger.info(vote)
            data['r'] = 0
            data['count'] = answer.votes
    return JsonResponse(data)


@login_required
@csrf_exempt
def vote_down(request, pk):
    data = dict(
        r=1,
    )
    if request.method == 'POST':
        user = request.user
        answer = Answer.objects.filter(id=pk).first()
        if answer is not None:
            vote = user.votedown(answer)
            if vote is True:
                data['r'] = 0
                data['count'] = answer.votes
                logger.info('{} 取消了赞： {}'.format(user, answer.id))
            else:
                logger.error('{} 取消赞失败: {}'.format(user, answer.id))
    return JsonResponse(data)


