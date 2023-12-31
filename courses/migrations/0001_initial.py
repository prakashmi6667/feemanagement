# Generated by Django 3.1.3 on 2021-08-06 04:44

import datetime
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
            name='Duration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('total_month', models.IntegerField(default=0)),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('Franchise_point', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('is_active', models.BooleanField(default=True, editable=False)),
                ('created_on', models.DateField(default=datetime.datetime.now, editable=False)),
                ('modified_on', models.DateField(default=datetime.datetime.now, editable=False)),
                ('created_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Duration',
                'verbose_name_plural': 'Durations',
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('code', models.CharField(max_length=150, unique=True)),
                ('thubnail_image', models.ImageField(max_length=150, upload_to='course/')),
                ('short_content', models.TextField()),
                ('is_active', models.BooleanField(default=True, editable=False)),
                ('created_on', models.DateField(default=datetime.datetime.now, editable=False)),
                ('modified_on', models.DateField(default=datetime.datetime.now, editable=False)),
                ('created_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('duration', models.ForeignKey(limit_choices_to={'is_active': True}, on_delete=django.db.models.deletion.CASCADE, to='courses.duration')),
            ],
            options={
                'verbose_name': 'Course',
                'verbose_name_plural': 'Courses',
            },
        ),
        migrations.CreateModel(
            name='AssignCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fee', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('created_on', models.DateField(default=datetime.datetime.now, editable=False)),
                ('modified_on', models.DateField(default=datetime.datetime.now, editable=False)),
                ('course', models.ForeignKey(default=1, limit_choices_to={'is_active': True}, on_delete=django.db.models.deletion.CASCADE, to='courses.course')),
                ('created_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Assign Course',
                'verbose_name_plural': 'Assign Courses',
            },
        ),
    ]
