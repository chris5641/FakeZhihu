from django.shortcuts import render
from django.http import HttpResponseNotFound
from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from asks.models import Ask
from .models import Topic


class ListView(generic.ListView):
    model = Topic
    template_name = 'topics/index.html'
    context_object_name = 'topics'


class DetailView(generic.DetailView):
    model = Topic
    template_name = 'index.html'
    context_object_name = 'topic'

    def get_paginator(self):
        answer_union = []
        for ask in self.object.asks.all():
            answer_union.append(ask.answers.all())
        if len(answer_union) < 1:
            return None
        answers_list = answer_union[0].union(*answer_union[1:]).order_by('-create_time')
        paginator = Paginator(answers_list, 10)
        return paginator

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        asks = Ask.objects.order_by('-create_time')[:5]
        paginator = self.get_paginator()
        if self.request.user.is_authenticated:
            vote_list = []
            for answer in paginator.page(1):
                if self.request.user.is_voted(answer):
                    vote_list.append(answer)
            context['vote_list'] = vote_list
        context['answers'] = paginator.page(1)
        context['asks'] = asks
        return context

    def get(self, request, *args, **kwargs):
        super(DetailView, self).get(request, *args, **kwargs)
        page = request.GET.get('page', None)
        if page is None:
            context = self.get_context_data(**kwargs)
            return self.render_to_response(context)

        vote_list = []
        try:
            answers = self.get_paginator().page(page)
        except PageNotAnInteger or EmptyPage:
            return HttpResponseNotFound
        if self.request.user.is_authenticated:
            for answer in answers:
                if self.request.user.is_voted(answer):
                    vote_list.append(answer)
        context = dict(answers=answers, vote_list=vote_list)
        return render(request, 'answerslist.html', context)


