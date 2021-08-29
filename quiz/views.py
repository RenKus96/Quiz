from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.list import MultipleObjectMixin

from .models import Exam, Question, Result
from .forms import ChoicesFormset


class ExamListView(LoginRequiredMixin, ListView):
    model = Exam
    template_name = 'exams/list.html'
    context_object_name = 'exams'
    paginate_by = 5


class ExamDetailView(LoginRequiredMixin, DetailView, MultipleObjectMixin):
    model = Exam
    template_name = 'exams/details.html'
    context_object_name = 'exam'
    pk_url_kwarg = 'uuid'
    paginate_by = 5

    def get_object(self, queryset=None):
        uuid = self.kwargs.get('uuid')
        # return self.get_queryset().get(uuid=uuid)
        return self.model.objects.get(uuid=uuid)

    def get_context_data(self, **kwargs):
        # context = super().get_context_data(**kwargs)
        # context['result_list'] = Result.objects.filter(
        #     exam=self.get_object(),
        #     user=self.request.user
        # ).order_by('state')
        context = super().get_context_data(object_list=self.get_queryset(), **kwargs)

        return context

    def get_queryset(self):
        return Result.objects.filter(
            exam=self.get_object(),
            user=self.request.user
        ).order_by('state')


class ExamResultCreateView(LoginRequiredMixin, CreateView):
    def post(self, request, *args, **kwargs):
        uuid = kwargs.get('uuid')
        result = Result.objects.create(
            user=request.user,
            exam=Exam.objects.get(uuid=uuid),
            state=Result.STATE.NEW,
            current_order_number = 0
        )

        result.save()

        return HttpResponseRedirect(reverse(
            'quizzes:question',
            kwargs={
                'uuid': uuid,
                'result_uuid': result.uuid,
                # 'order_number': 1,
            }
        ))


class ExamQuestionView(LoginRequiredMixin, UpdateView):
    def get(self, request, *args, **kwargs):
        uuid = kwargs.get('uuid')
        # order_number = kwargs.get('order_number')
        result = Result.objects.get(uuid=kwargs['result_uuid'])

        question = Question.objects.get(
            exam__uuid=uuid,
            # order_num=order_number
            order_num=result.current_order_number + 1
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
        result = Result.objects.get(uuid=result_uuid)
        # order_number = kwargs.get('order_number')
        order_number = result.current_order_number + 1

        question = Question.objects.get(
            exam__uuid=uuid,
            order_num=order_number
        )

        choices = ChoicesFormset(data=request.POST)
        selected_choices = ['is_selected' in form.changed_data for form in choices.forms]

        if not any(selected_choices):
            messages.error(self.request, f'Заполните хотя бы один ответ')
        elif all(selected_choices):
            messages.error(self.request, f'Все варианты ответов не могут быть правильными')
        else:
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
                # 'order_number': order_number + 1,
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


class ExamResultUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    # permission_required = ['accounts.view_statistics']

    def get(self, request, *args, **kwargs):
        uuid = kwargs['uuid']
        result_uuid = kwargs['result_uuid']
        user = request.user

        result = Result.objects.get(
            user=user,
            uuid=result_uuid
        )

        return HttpResponseRedirect(reverse(
            'quizzes:question',
            kwargs={
                'uuid': uuid,
                'result_uuid': result.uuid,
                # 'order_number': result.current_order_number + 1,
            }
        ))


class ExamResultDeleteView(LoginRequiredMixin, DeleteView):
    model = Result
    # success_url = reverse_lazy('quizzes:details')
    template_name = 'results/delete.html'
    context_object_name = 'result'
    pk_url_kwarg = 'uuid'

    def get_object(self, queryset=None):
        uuid = self.kwargs.get('result_uuid')
        return self.get_queryset().get(uuid=uuid)

    def get_success_url(self):
        success_url = reverse_lazy(
            'quizzes:details',
            kwargs={
                'uuid': self.kwargs.get('uuid'),
            }
        )
        return success_url


class ResultListView(LoginRequiredMixin, ListView):
    model = Result
    template_name = 'results/list.html'
    context_object_name = 'results'
    paginate_by = 10

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user).order_by('state')
