from django.urls import path

from .views import index, EnterCodeView

urlpatterns = [
    path('', index, name='index'),
    path('enter_code', EnterCodeView.as_view(), name='enter_code'),
]
