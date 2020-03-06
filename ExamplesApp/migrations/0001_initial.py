# Generated by Django 3.0.4 on 2020-03-06 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProductModel',
            fields=[
                ('no', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30, unique=True)),
                ('price', models.FloatField()),
                ('quantity', models.IntegerField()),
            ],
        ),
    ]
