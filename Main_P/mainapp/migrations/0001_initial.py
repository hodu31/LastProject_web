# Generated by Django 4.0.1 on 2023-09-20 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('post_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('post_no', models.IntegerField(max_length=5)),
                ('post_date', models.DateField()),
                ('post_title', models.CharField(max_length=100)),
                ('post_content', models.CharField(max_length=500)),
            ],
            options={
                'db_table': 'post',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Security',
            fields=[
                ('sec_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('sec_pw', models.CharField(max_length=20)),
                ('sec_nm', models.CharField(max_length=20)),
                ('sec_bir', models.CharField(max_length=20)),
                ('sec_add', models.CharField(max_length=100)),
                ('sec_hp', models.CharField(max_length=20)),
                ('sec_area', models.CharField(max_length=20)),
                ('sec_reason', models.CharField(max_length=500)),
            ],
            options={
                'db_table': 'security',
                'managed': False,
            },
        ),
    ]
