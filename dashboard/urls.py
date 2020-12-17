from django.urls import path

from .views import index, EnterCodeView, UploadCodesView

urlpatterns = [
    path('', index, name='index'),
    path('enter_code', EnterCodeView.as_view(), name='enter_code'),
    path('upload_codes', UploadCodesView.as_view(), name='upload_codes'),
]
