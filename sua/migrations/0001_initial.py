# Generated by Django 3.1.2 on 2021-06-25 13:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import sua.storage


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.TimeField(auto_now_add=True)),
                ('created', models.DateTimeField(auto_now=True, verbose_name='创建日期')),
                ('title', models.CharField(max_length=100)),
                ('detail', models.CharField(max_length=400)),
                ('is_valid', models.BooleanField(default=False)),
                ('is_created_by_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StudentInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.TimeField(auto_now_add=True)),
                ('number', models.CharField(max_length=10)),
                ('suahours', models.FloatField(default=0)),
                ('classtype', models.CharField(default='一班', max_length=100)),
                ('grade', models.IntegerField(choices=[(2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021)], default=2021)),
                ('phone', models.CharField(default='000', max_length=100)),
                ('power', models.IntegerField(default=0)),
                ('name', models.CharField(max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Sua',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.TimeField(auto_now_add=True)),
                ('suahours', models.FloatField(default=0.0)),
                ('is_valid', models.BooleanField(default=False)),
                ('added', models.BooleanField(default=False)),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='suas', to='sua.activity')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='suas', to='sua.studentinfo')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Proof',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.TimeField(auto_now_add=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('is_offline', models.BooleanField(default=False)),
                ('proof_file', models.FileField(blank=True, storage=sua.storage.FileStorage(), upload_to='proofs')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proofs', to='sua.studentinfo')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.TimeField(auto_now_add=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建日期')),
                ('contact', models.CharField(blank=True, max_length=100)),
                ('is_checked', models.BooleanField(default=False)),
                ('status', models.IntegerField(default=0)),
                ('feedback', models.CharField(blank=True, max_length=400)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='sua.studentinfo')),
                ('proof', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='sua.proof')),
                ('sua', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='application', to='sua.sua')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='activity',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activity', to='sua.studentinfo'),
        ),
    ]
