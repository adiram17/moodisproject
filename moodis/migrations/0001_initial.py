# Generated by Django 2.2.5 on 2021-03-04 07:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(blank=True, max_length=100, null=True)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=10)),
                ('age', models.IntegerField(default=0)),
                ('is_self', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='PatientMoodEpisode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True)),
                ('episode_score', models.FloatField()),
                ('episode_category', models.CharField(max_length=50)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moodis.Patient')),
            ],
            options={
                'verbose_name': 'Patient Mood Episode',
                'verbose_name_plural': 'Patient Mood Episode',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_code', models.CharField(max_length=10)),
                ('question_type', models.CharField(choices=[('Questionaire 1', 'Mood Questionaire'), ('Questionaire 2', 'Closing Questionaire')], max_length=100)),
                ('question_section', models.CharField(max_length=255)),
                ('question_number', models.IntegerField(default=0)),
                ('prompt', models.TextField(max_length=255)),
            ],
            options={
                'verbose_name': 'Question',
                'verbose_name_plural': 'Questions',
            },
        ),
        migrations.CreateModel(
            name='ResponseOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255)),
                ('score', models.IntegerField(default=0)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moodis.Question')),
            ],
            options={
                'verbose_name': 'Response Option',
                'verbose_name_plural': 'Response Options',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(blank=True, max_length=100, null=True)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=10)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('age', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PatientMoodResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_score', models.IntegerField(default=0)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moodis.Patient')),
                ('patient_mood_episode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moodis.PatientMoodEpisode')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moodis.Question')),
            ],
            options={
                'verbose_name': 'Patient Mood Response',
                'verbose_name_plural': 'Patient Mood Responses',
            },
        ),
        migrations.AddField(
            model_name='patient',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moodis.Profile'),
        ),
    ]
