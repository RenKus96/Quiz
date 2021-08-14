from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Exam, Question, Result
from .forms import ChoicesFormset


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


class ExamResultCreateView(LoginRequiredMixin, CreateView):
    def post(self, request, *args, **kwargs):
        uuid = kwargs.get('uuid')
        result = Result.objects.create(
            user=request.user,
            exam=Exam.objects.get(uuid=uuid),
            state=Result.STATE.NEW
        )

        result.save()

        return HttpResponseRedirect(reverse(
            'quizzes:question',
            kwargs={
                'uuid': uuid,
                'result_uuid': result.uuid,
                'order_number': 1,
            }
        ))


class ExamQuestionView(LoginRequiredMixin, UpdateView):
    def get(self, request, *args, **kwargs):
        uuid = kwargs.get('uuid')
        order_number = kwargs.get('order_number')

        question = Question.objects.get(
            exam__uuid=uuid,
            order_num=order_number
        )

        choices = ChoicesFormset(queryset=question.choices.all())

        return render(
            request,
            'exams/question.html',
            context={
                'question': question,
                'choices': choices
            }
        )

    def post(self, request, *args, **kwargs):
        uuid = kwargs.get('uuid')
        result_uuid = kwargs.get('result_uuid')
        order_number = kwargs.get('order_number')

        question = Question.objects.get(
            exam__uuid=uuid,
            order_num=order_number
        )

        choices = ChoicesFormset(data=request.POST)
        selected_choices = ['is_selected' in form.changed_data for form in choices.forms]

        result = Result.objects.get(uuid=result_uuid)
        result.update_result(order_number, question, selected_choices)

        if result.state == Result.STATE.FINISHED:
            return HttpResponseRedirect(reverse(
                'quizzes:result_details',
                kwargs={
                    'uuid': uuid,
                    'result_uuid': result.uuid,
                }
            ))

        return HttpResponseRedirect(reverse(
            'quizzes:question',
            kwargs={
                'uuid': uuid,
                'result_uuid': result.uuid,
                'order_number': order_number + 1,
            }
        ))


class ExamResultDetailView(LoginRequiredMixin, DetailView):
    model = Result
    template_name = 'results/details.html'
    context_object_name = 'result'
    pk_url_kwarg = 'uuid'

    def get_object(self, queryset=None):
        uuid = self.kwargs.get('result_uuid')
        return self.get_queryset().get(uuid=uuid)
