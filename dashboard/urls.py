from django.urls import path

from .views import index, EnterCodeView, UploadCodesView, UploadRewardsView, SignupView

urlpatterns = [
    path('', index, name='index'),
    path('enter_code', EnterCodeView.as_view(), name='enter_code'),
    path('upload_codes', UploadCodesView.as_view(), name='upload_codes'),
    path('upload_rewards', UploadRewardsView.as_view(), name='upload_rewards'),
    path('signup', SignupView.as_view(), name='signup'),
]
