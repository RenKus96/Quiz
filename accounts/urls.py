from django.urls import path

from .views import AccountPasswordChangeView, AccountRegistrationView

app_name = 'accounts'

urlpatterns = [
    path('registration/', AccountRegistrationView.as_view(), name='registration'),
    path('password/', AccountPasswordChangeView.as_view(), name='password'),
]