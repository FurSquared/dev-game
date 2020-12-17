import csv

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
        except Token.DoesNotExist:
            pass

        return redirect("index")

class UploadCodesView(View):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponse('Unauthorized', status=401)

        return render(request, 'upload_codes.html')


    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponse('Unauthorized', status=401)

        decoded_file = request.FILES['csvfile'].read().decode('UTF-8').splitlines()
        reader = csv.DictReader(decoded_file)

        new_codes = []
        updated_codes = []
        for row in reader:
            valid_from = None if len(row['valid_from']) == 0 else row['valid_from']

            token, created = Token.objects.get_or_create(
                code=row['code'],
                defaults={
                    'gm_note': row['gm_note'],
                    'reward_text': row['reward_text'],
                    'valid_from': valid_from,
                }
            )
            if created:
                new_codes.append(token)
            else:
                updated_codes.append(token)
        context = {
            'new_codes': new_codes,
            'updated_codes': updated_codes,
        }
        return render(request, 'upload_codes.html', context)

class UploadRewardsView(View):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponse('Unauthorized', status=401)

        return render(request, 'upload_rewards.html')


    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponse('Unauthorized', status=401)
        return HttpResponse(status=204)
