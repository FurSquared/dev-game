from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from dashboard.models import CollectedReward, CollectedToken, Token

@login_required
def index(request):
  data = {
    'user': request.user,
    'collected_tokens': CollectedToken.objects.filter(user=request.user),
    'collected_rewards': CollectedReward.objects.filter(user=request.user),
  }
  return render(request, 'dashboard.html', data)

class EnterCodeView(View):

  @method_decorator(login_required)
  def get(self, request, *args, **kwargs):
    return HttpResponse(status=204)

  @method_decorator(login_required)
  def post(self, request, *args, **kwargs):
    try:
      code = request.POST.get('code', '').upper().replace("-", "_").strip()
      token = Token.objects.get(code=code)

      CollectedToken.objects.get_or_create(user=request.user, token=token)
    except Token.DoesNotExist as e:
      pass

    return redirect("index")
