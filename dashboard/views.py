import csv

from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import validate_email
from django.forms import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from dashboard.models import CollectedReward, CollectedToken, Token, Reward


class SignupView(View):

    def get(self, request, *args, **kwargs):
        form = UserCreationForm()

        return render(request, 'signup.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = UserCreationForm(request.POST)
        try:
            validate_email(form.data['username'])
        except ValidationError as e:
            form.add_error('username', e)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')

        return render(request, 'signup.html', {'form': form})

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

        keys = ['name', 'gm_note', 'count', 'required_tokens', 'reward_text', 'valid_from']
        new_rewards = []
        updated_rewards = []
        for row in reader:
            valid_from = None if len(row['valid_from']) == 0 else row['valid_from']
            required_tokens = [item.strip() for item in row['required_tokens'].split(',')] if len(row['required_tokens']) > 0 else []

            reward, created = Reward.objects.get_or_create(
                name=row['name'],
                defaults={
                    'gm_note': row['gm_note'],
                    'reward_text': row['reward_text'],
                    'valid_from': valid_from,
                    'count': int(row['count']) if len(row['count']) > 0 else 0,
                }
            )

            if created:
                reward.required_tokens.set(required_tokens)
                reward.save()
                new_rewards.append(' | '.join([str(getattr(reward, key)) for key in keys]))
            else:
                updated_rewards.append(' | '.join([str(getattr(reward, key)) for key in keys]))

        context = {
            'title': 'Upload Rewards',
            'heading': ' | '.join(keys),
            'sections': [
                {
                    'title': 'New Rewards',
                    'values': new_rewards,
                },
                {
                    'title': 'Updated Rewards',
                    'values': updated_rewards,
                },
            ]
        }
        return render(request, 'upload_csv.html', context)
