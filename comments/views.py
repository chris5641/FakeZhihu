from django.shortcuts import redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from fakeZhihu.settings import logger
from .models import Comment
from answers.models import Answer


class CreatCommentView(LoginRequiredMixin, generic.CreateView):
    model = Comment
    fields = ['content']

    def form_valid(self, form):
        try:
            answer = Answer.objects.filter(id=self.kwargs['pk']).first()
        except Answer.DoesNotExist:
            logger.error('评论错误: 答案 {} 不存在'.format(self.kwargs['pk']))
            return redirect(self.request.META.get('HTTP_REFERER', '/'))
        comment = form.save(commit=False)
        comment.author = self.request.user
        comment.answer = answer
        reply_id = self.request.POST.get('reply_id', 0)
        try:
            reply = Comment.objects.filter(id=reply_id).first()
        except ValueError:
            logger.error('回复评论错误： reply_id = {}'.format(reply_id))
            return redirect(self.request.META.get('HTTP_REFERER', '/'))
        comment.reply_to = reply
        comment.save()
        logger.info('{} 评论了 {} 的回答'.format(comment.author, answer.author))
        return redirect(self.request.META.get('HTTP_REFERER', '/'))

    def form_invalid(self, form):
        logger.error('comment error')
        return redirect(self.request.META.get('HTTP_REFERER', '/'))


class CommentsListView(generic.ListView):
    template_name = 'commentslist.html'
    model = Comment
    context_object_name = 'comments'

    def get_queryset(self):
        answer_id = self.kwargs['pk']
        queryset = Comment.objects.all().filter(answer_id=answer_id).order_by('-create_time')
        return queryset


class DeleteCommentView(LoginRequiredMixin, generic.DeleteView):
    model = Comment

    def get_success_url(self):
        logger.info('评论：{} 删除成功'.format(self.object.id))
        return self.request.META.get('HTTP_REFERER', '/')


