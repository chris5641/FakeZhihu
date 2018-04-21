from django.shortcuts import render, redirect, reverse, HttpResponse
from django.http import HttpResponseNotFound
from django.contrib import auth
from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from fakeZhihu.settings import logger
from .models import User, FollowShip
from .forms import LoginForm, RegisterForm
from asks.models import Ask


class IndexView(LoginRequiredMixin, generic.DetailView):
    template_name = 'index.html'

    def get_object(self, queryset=None):
        union_list = []
        for followship in self.request.user.follow_list.all():
            union_list.append(followship.follow.answers.all())
        answers_list = self.request.user.answers.all().union(*union_list).order_by('-create_time')
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
            for answer in answers:
                if self.request.user.is_voted(answer):
                    vote_list.append(answer)
        context = dict(answers=answers, vote_list=vote_list)
        return render(request, 'answerslist.html', context)

    def handle_no_permission(self):
        return redirect('explore')


class DetailView(generic.DetailView):
    model = User
    context_object_name = 'people'
    template_name = 'users/detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['is_following'] = self.request.user.is_following(self.object)
        return context


class AnswerView(DetailView):

    def get_context_data(self, **kwargs):
        context = super(AnswerView, self).get_context_data(**kwargs)
        vote_list = []
        answer_list = self.object.answers.order_by('-votes', '-create_time')
        paginator = Paginator(answer_list, 5)
        context['AnswerView'] = True
        context['answers'] = paginator.page(1)
        if self.request.user.is_authenticated:
            for answer in paginator.page(1):
                if self.request.user.is_voted(answer):
                    vote_list.append(answer)
            context['vote_list'] = vote_list
        return context

    def get(self, request, *args, **kwargs):
        super(AnswerView, self).get(request, *args, **kwargs)
        vote_list = []
        page = request.GET.get('page', None)
        if page is None:
            context = self.get_context_data(**kwargs)
            return self.render_to_response(context)

        answer_list = self.object.answers.order_by('-votes', '-create_time')
        paginator = Paginator(answer_list, 5)
        try:
            answers = paginator.page(page)
        except PageNotAnInteger or EmptyPage:
            return HttpResponseNotFound
        if self.request.user.is_authenticated:
            for answer in answers:
                if self.request.user.is_voted(answer):
                    vote_list.append(answer)
        context = dict(answers=answers, vote_list=vote_list)
        return render(request, 'answerslist.html', context)


class AskView(DetailView):

    def get_context_data(self, **kwargs):
        context = super(AskView, self).get_context_data(**kwargs)
        context['AskView'] = True
        return context


class CollectionView(DetailView):

    def get_context_data(self, **kwargs):
        context = super(CollectionView, self).get_context_data(**kwargs)
        context['CollectionView'] = True
        return context


class FollowingView(DetailView):

    def get_context_data(self, **kwargs):
        context = super(FollowingView, self).get_context_data(**kwargs)
        user = self.request.user
        following_list = []
        followship_list = self.object.follow_list.all()
        for followship in followship_list:
            if user.is_authenticated:
                followship.follow.is_followed = user.is_following(followship.follow)
            following_list.append(followship.follow)
        context['following_list'] = following_list
        context['FollowingView'] = True
        return context


class FollowerView(DetailView):

    def get_context_data(self, **kwargs):
        context = super(FollowerView, self).get_context_data(**kwargs)
        user = self.request.user
        followers_list = []
        followship_list = self.object.fun_list.all()
        for followship in followship_list:
            if user.is_authenticated:
                followship.fun.is_followed = user.is_following(followship.fun)
            followers_list.append(followship.fun)
        context['followers_list'] = followers_list
        context['FollowerView'] = True
        return context


class ProfileView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'users/profile.html'
    context_object_name = 'user'
    fields = ['nickname', 'sex', 'intro', 'work', 'image_url']

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        user = self.object
        user.update(form.cleaned_data)
        logger.info('{} 修改了资料'.format(user))
        return redirect('users:detail', pk=user.id)

    def form_invalid(self, form):
        logger.error('{} 修改资料格式错误'.format(self.object))


class PasswordView(PasswordChangeView):
    template_name = 'users/setting.html'

    def get_success_url(self):
        logger.info('{} 修改密码成功'.format(self.request.user))
        return reverse('users:detail', kwargs={'pk': self.request.user.id})

    def form_invalid(self, form):
        return redirect('users:setting')


def login(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            logger.info('login: {}'.format(user))
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})


@login_required
def logout(request):
    auth.logout(request)
    return redirect(request.META.get('HTTP_REFERER', '/'))


def register(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            logger.info('register: {}'.format(user))
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def follow(request, pk):
    user = request.user
    if user.follow(pk):
        logger.info('{} follow: {}'.format(user, User.objects.get(id=pk)))
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def unfollow(request, pk):
    user = request.user
    if user.unfollow(pk):
        logger.info('{} unfollow: {}'.format(user, User.objects.get(id=pk)))
    return redirect(request.META.get('HTTP_REFERER', '/'))


def detail(request, pk):
    return redirect('users:answers', pk=pk)




