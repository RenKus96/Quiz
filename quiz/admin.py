from django.contrib import admin

from .models import Exam, Question, Choice, Result
from .forms import ChoiceInlineFormSet, QuestionInlineFormSet


class ChoiceInline(admin.TabularInline):
    model = Choice
    fields = ('text', 'is_correct')
    show_change_link = True
    extra = 0
    formset = ChoiceInlineFormSet


class QuestionAdmin(admin.ModelAdmin):
    inlines = (ChoiceInline, )


class QuestionInline(admin.TabularInline):
    model = Question
    fields = ('text', 'order_num')
    show_change_link = True
    extra = 0
    formset = QuestionInlineFormSet
    ordering = ('order_num', )


class ExamAdmin(admin.ModelAdmin):
    readonly_fields = ['uuid']
    inlines = (QuestionInline, )


admin.site.register(Exam, ExamAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Result)
