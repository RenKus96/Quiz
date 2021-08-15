from django.forms import BaseInlineFormSet, ModelForm, modelformset_factory
from django.core.exceptions import ValidationError
from django import forms

from .models import Choice


class ChoiceInlineFormSet(BaseInlineFormSet):
    def clean(self):
        num_correct_answer = sum(1 for form in self.forms if form.cleaned_data['is_correct'])

        if num_correct_answer == 0:
            raise ValidationError('Необходимо выбрать как минимум 1 правильный ответ.')

        if num_correct_answer == len(self.forms):
            raise ValidationError('Не могут быть все ответы правильными')


class QuestionInlineFormSet(BaseInlineFormSet):
    def clean(self):
        if not (self.instance.QUESTION_MIN_LIMIT <= len(self.forms) <= self.instance.QUESTION_MAX_LIMIT):
            raise ValidationError('Кол-во вопросов должно быть в диапазоне от {} до {}'.format(
                self.instance.QUESTION_MIN_LIMIT,
                self.instance.QUESTION_MAX_LIMIT
            ))

        order_num_set = [ form.cleaned_data['order_num'] for form in self.forms ]

        if min(order_num_set) != 1:
            raise ValidationError('Нумерация вопросов должна начинаться с 1.')

        if max(order_num_set) != len(self.forms):
            raise ValidationError('Максимальный порядковый номер вопроса не должен превышать кол-во вопросов в тесте.')

        # Мы проверили минимальное и максимальное значение списка
        # и теперь, в принципе, достаточно проверить, что бы значения не повторялись
        if len(order_num_set) != len(set(order_num_set)):
            raise ValidationError('Нарушен порядок нумерации вопросов.')



class ChoiceForm(ModelForm):
    is_selected = forms.BooleanField(required=False)

    class Meta:
        model = Choice
        fields = ['text']


ChoicesFormset = modelformset_factory(
    model=Choice,
    form=ChoiceForm,
    extra=0
)
