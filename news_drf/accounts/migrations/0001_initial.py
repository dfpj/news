# Generated by Django 3.2.13 on 2022-04-18 10:50

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100, null=True)),
                ('last_name', models.CharField(max_length=100, null=True)),
                ('birthday', models.DateField(default=django.utils.timezone.now)),
                ('avatar', models.ImageField(default='1.jpg', upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Verify',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('code', models.PositiveSmallIntegerField()),
                ('send_date', models.DateTimeField(auto_now_add=True)),
                ('allow_update_pass', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('is_active', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('profile', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.profile')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]