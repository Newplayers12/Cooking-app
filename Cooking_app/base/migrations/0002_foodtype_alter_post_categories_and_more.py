# Generated by Django 4.1.4 on 2022-12-28 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='categories',
            field=models.CharField(choices=[('Vietnam', 'Vietnam'), ('Laos', 'Laos'), ('Cambodia', 'Cambodia')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='description',
            field=models.TextField(max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='ingredients',
            field=models.TextField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='instructions',
            field=models.TextField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=2000, null=True),
        ),
    ]
