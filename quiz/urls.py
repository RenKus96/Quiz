from django.urls import path

from .views import ExamListView, ExamDetailView, ExamResultCreateView, ExamQuestionView, ExamResultDetailView

app_name = 'quizzes'

urlpatterns = [
    path('', ExamListView.as_view(), name='list'),
    path('<uuid:uuid>/', ExamDetailView.as_view(), name='details'),
    path('<uuid:uuid>/result/create/', ExamResultCreateView.as_view(), name='result_create'),
    path('<uuid:uuid>/results/<uuid:result_uuid>/details/', ExamResultDetailView.as_view(), name='result_details'),
    path('<uuid:uuid>/result/<uuid:result_uuid>/question/<int:order_number>/',
         ExamQuestionView.as_view(), name='question'),
]
