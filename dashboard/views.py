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

        context = {
            'title': 'Upload Codes',
        }
        return render(request, 'upload_csv.html', context)


    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponse('Unauthorized', status=401)

        decoded_file = request.FILES['csvfile'].read().decode('UTF-8').splitlines()
        reader = csv.DictReader(decoded_file)

        keys = ['code', 'gm_note', 'reward_text', 'valid_from']
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
                new_codes.append(' | '.join([str(getattr(token, key)) for key in keys]))
            else:
                updated_codes.append(' | '.join([str(getattr(token, key)) for key in keys]))


        context = {
            'title': 'Upload Codes',
            'heading': ' | '.join(keys),
            'sections': [
                {
                    'title': 'New Codes',
                    'values': new_codes,
                },
                {
                    'title': 'Updated Codes',
                    'values': updated_codes,
                },
            ]
        }
        return render(request, 'upload_csv.html', context)

class UploadRewardsView(View):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponse('Unauthorized', status=401)

        context = {
            'title': 'Upload Rewards',
        }
        return render(request, 'upload_csv.html', context)


    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponse('Unauthorized', status=401)

        decoded_file = request.FILES['csvfile'].read().decode('UTF-8').splitlines()
        reader = csv.DictReader(decoded_file)

        keys = ['name', 'gm_note count', 'required_tokens', 'reward_text', 'valid_from']
        new_rewards = []
        updated_rewards = []
        for row in reader:
            valid_from = None if len(row['valid_from']) == 0 else row['valid_from']
            required_tokens = [item.strip() for item in row['required_tokens'].split(',')]

            reward, created = Reward.objects.get_or_create(
                name=row['name'],
                defaults={
                    'gm_note': row['gm_note'],
                    'reward_text': row['reward_text'],
                    'valid_from': valid_from,
                    'count': row['count'],
                    'required_tokens': required_tokens,
                }
            )

            if created:
                new_rewards.append(' | '.join([str(getattr(token, key)) for key in keys]))
            else:
                updated_rewards.append(' | '.join([str(getattr(token, key)) for key in keys]))

        context = {
            'title': 'Upload Rewards',
            'heading': ' | '.join(keys),
            'sections': [
                {
                    'title': 'New Rewards',
                    'values': new_codes,
                },
                {
                    'title': 'Updated Rewards',
                    'values': updated_codes,
                },
            ]
        }
        return render(request, 'upload_csv.html', context)
