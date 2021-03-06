# Generated by Django 3.1.3 on 2020-11-28 03:31

from django.conf import settings
import django.core.validators
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
                ('code', models.CharField(max_length=25, primary_key=True, serialize=False, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z_-]*$', 'Only alphanumeric, underscore, and dash are allowed.')])),  # noqa
                ('gm_note', models.TextField(blank=True)),
                ('reward_text', models.TextField(blank=True)),
                ('valid_from', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reward',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('count', models.PositiveIntegerField(default=0)),
                ('valid_from', models.DateTimeField(blank=True, null=True)),
                ('gm_note', models.TextField(blank=True)),
                ('reward_text', models.TextField(blank=True)),
                ('required_tokens', models.ManyToManyField(blank=True, to='dashboard.Token')),
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
        migrations.AddIndex(
            model_name='reward',
            index=models.Index(fields=['count'], name='dashboard_r_count_b40b99_idx'),
        ),
        migrations.AddIndex(
            model_name='collectedtoken',
            index=models.Index(fields=['user', 'token'], name='dashboard_c_user_id_656949_idx'),
        ),
        migrations.AddIndex(
            model_name='collectedtoken',
            index=models.Index(fields=['user'], name='dashboard_c_user_id_1b23c5_idx'),
        ),
        migrations.AddIndex(
            model_name='collectedtoken',
            index=models.Index(fields=['token'], name='dashboard_c_token_i_6c5100_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='collectedtoken',
            unique_together={('user', 'token')},
        ),
        migrations.AddIndex(
            model_name='collectedreward',
            index=models.Index(fields=['user'], name='dashboard_c_user_id_f1a2c1_idx'),
        ),
        migrations.AddIndex(
            model_name='collectedreward',
            index=models.Index(fields=['user', 'reward'], name='dashboard_c_user_id_8af52a_idx'),
        ),
        migrations.AddIndex(
            model_name='collectedreward',
            index=models.Index(fields=['reward'], name='dashboard_c_reward__7d24aa_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='collectedreward',
            unique_together={('user', 'reward')},
        ),
    ]
