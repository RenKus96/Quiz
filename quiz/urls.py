from django.urls import path

from .views import ExamListView, ExamDetailView

app_name = 'quizzes'

urlpatterns = [
    path('', ExamListView.as_view(), name='list'),
    path('<uuid:uuid>/', ExamDetailView.as_view(), name='details'),
]
