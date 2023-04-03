# Generated by Django 4.1.7 on 2023-03-30 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserNote',
            fields=[
                ('id', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=32)),
                ('category', models.CharField(max_length=16)),
                ('status', models.CharField(max_length=16)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'user_notes',
            },
        ),
    ]