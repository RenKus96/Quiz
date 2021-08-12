from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Exam


class ExamListView(LoginRequiredMixin, ListView):
    model = Exam
    template_name = 'exams/list.html'
    context_object_name = 'exams'


class ExamDetailView(LoginRequiredMixin, DetailView):
    model = Exam
    template_name = 'exams/details.html'
    context_object_name = 'exam'
    pk_url_kwarg = 'uuid'

    def get_object(self, queryset=None):
        uuid = self.kwargs.get('uuid')
        return self.get_queryset().get(uuid=uuid)
