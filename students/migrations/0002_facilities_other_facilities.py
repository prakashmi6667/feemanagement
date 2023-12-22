# Generated by Django 3.1.3 on 2021-08-09 10:43

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Facilities',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('is_active', models.BooleanField(default=True, editable=False)),
                ('created_on', models.DateField(default=datetime.datetime.now, editable=False)),
                ('modified_on', models.DateField(default=datetime.datetime.now, editable=False)),
                ('created_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Facilities',
                'verbose_name_plural': 'Facilities',
            },
        ),
        migrations.CreateModel(
            name='Other_Facilities',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, editable=False)),
                ('created_on', models.DateField(default=datetime.datetime.now, editable=False)),
                ('modified_on', models.DateField(default=datetime.datetime.now, editable=False)),
                ('created_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('facilities', models.ForeignKey(limit_choices_to={'is_active': True}, on_delete=django.db.models.deletion.CASCADE, to='students.facilities')),
                ('student', models.ForeignKey(limit_choices_to={'is_active': True}, on_delete=django.db.models.deletion.CASCADE, to='students.student')),
            ],
            options={
                'verbose_name': 'Other Facilities',
                'verbose_name_plural': 'Other Facilities',
            },
        ),
    ]
