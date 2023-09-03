# Generated by Django 4.2.4 on 2023-09-01 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatgptapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_message', models.TextField()),
                ('bot_response', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
