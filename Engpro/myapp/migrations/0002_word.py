# Generated by Django 3.0.5 on 2020-06-07 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.CharField(max_length=128)),
                ('word', models.CharField(max_length=128)),
            ],
            options={
                'db_table': 'myapp_word',
            },
        ),
    ]
