# Generated by Django 3.1.3 on 2020-11-28 00:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Token',
            fields=[
                ('code', models.CharField(max_length=25, primary_key=True, serialize=False)),
                ('gm_note', models.TextField(blank=True)),
                ('reward_text', models.TextField(blank=True)),
                ('valid_from', models.DateTimeField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reward',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveIntegerField(default=0)),
                ('valid_from', models.DateTimeField(blank=True)),
                ('gm_note', models.TextField(blank=True)),
                ('reward_text', models.TextField(blank=True)),
                ('required_tokens', models.ManyToManyField(to='dashboard.Token')),
            ],
        ),
        migrations.CreateModel(
            name='CollectedToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('read', models.BooleanField(default=False)),
                ('collected_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('token', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='dashboard.token')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CollectedReward',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('read', models.BooleanField(default=False)),
                ('collected_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('reward', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='dashboard.reward')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
