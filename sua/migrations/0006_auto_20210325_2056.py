# Generated by Django 3.1.2 on 2021-03-25 12:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sua', '0005_auto_20210323_2203'),
    ]

    operations = [
        migrations.AddField(
            model_name='sua',
            name='is_valid',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='application',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='sua.studentinfo'),
        ),
        migrations.AlterField(
            model_name='application',
            name='proof',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='sua.proof'),
        ),
        migrations.AlterField(
            model_name='proof',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proofs', to='sua.studentinfo'),
        ),
    ]