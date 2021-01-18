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

from dashboard.domain import process_csv_codes
from dashboard.models import CollectedReward, CollectedToken, Token, Reward


class SignupView(View):

    def get(self, request, *args, **kwargs):
        form = UserCreationForm()

        # This is odd, but we're using email as the username
        # And this keeps historic data inline. Just relabeling the default field
        # to "email."  Email-address is correctly validated below.
        # If we rebuild this next year, we should go with a custom user creation
        # form.
        form.fields['username'].label = "Email Address"

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

        keys, new_codes, updated_codes = process_csv_codes(reader)

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

        keys, new_rewards, updated_rewards = process_csv_rewards(reader)

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
