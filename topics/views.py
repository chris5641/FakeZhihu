from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from fakeZhihu.settings import logger
from asks.models import Ask
from .models import Topic
from answers.models import Answer


class ListView(generic.ListView):
    model = Topic
    template_name = 'topics/index.html'
    context_object_name = 'topics'

